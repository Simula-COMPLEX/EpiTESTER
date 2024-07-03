#!/usr/bin/env python

# Copyright (c) 2018-2020 Intel Corporation
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

"""
This module provides the ScenarioManager implementations.
It must not be modified and is for reference only!
"""

from __future__ import print_function

import math
import pickle
import signal
import sys
import time

import py_trees
import carla
from sympy.solvers import solve
from sympy import Symbol

from srunner.scenariomanager.carla_data_provider import CarlaDataProvider
from srunner.scenariomanager.timer import GameTime
from srunner.scenariomanager.watchdog import Watchdog

from leaderboard.autoagents.agent_wrapper import AgentWrapper, AgentError
from leaderboard.envs.sensor_interface import SensorReceivedNoData
from leaderboard.utils.result_writer import ResultOutputProvider


class ScenarioManager(object):
    """
    Basic scenario manager class. This class holds all functionality
    required to start, run and stop a scenario.

    The user must not modify this class.

    To use the ScenarioManager:
    1. Create an object via manager = ScenarioManager()
    2. Load a scenario via manager.load_scenario()
    3. Trigger the execution of the scenario manager.run_scenario()
       This function is designed to explicitly control start and end of
       the scenario execution
    4. If needed, cleanup with manager.stop_scenario()
    """

    def __init__(self, timeout, debug_mode=False):
        """
        Setups up the parameters, which will be filled at load_scenario()
        """
        self.input_path = None
        self.elapsed_time = None
        self.count_tick = None
        self.scenario = None
        self.scenario_tree = None
        self.scenario_class = None
        self.ego_vehicles = None
        self.other_actors = None

        self._debug_mode = debug_mode
        self._agent = None
        self._running = False
        self._timestamp_last_run = 0.0
        self._timeout = float(timeout)

        # Used to detect if the simulation is down
        watchdog_timeout = max(5, self._timeout - 2)
        self._watchdog = Watchdog(watchdog_timeout)

        # Avoid the agent from freezing the simulation
        agent_timeout = watchdog_timeout - 1
        self._agent_watchdog = Watchdog(agent_timeout)

        self.scenario_duration_system = 0.0
        self.scenario_duration_game = 0.0
        self.start_system_time = None
        self.end_system_time = None
        self.end_game_time = None

        self.tag = None
        self.uq = []

        # Register the scenario tick as callback for the CARLA world
        # Use the callback_id inside the signal handler to allow external interrupts
        signal.signal(signal.SIGINT, self.signal_handler)

    def signal_handler(self, signum, frame):
        """
        Terminate scenario ticking when receiving a signal interrupt
        """
        self._running = False

    def cleanup(self):
        """
        Reset all parameters
        """
        self._timestamp_last_run = 0.0
        self.scenario_duration_system = 0.0
        self.scenario_duration_game = 0.0
        self.start_system_time = None
        self.end_system_time = None
        self.end_game_time = None

    def load_scenario(self, scenario, agent, rep_number):
        """
        Load a new scenario
        """

        GameTime.restart()
        self._agent = AgentWrapper(agent)
        self.scenario_class = scenario
        self.scenario = scenario.scenario
        self.scenario_tree = self.scenario.scenario_tree
        self.ego_vehicles = scenario.ego_vehicles
        self.other_actors = scenario.other_actors
        self.repetition_number = rep_number

        # To print the scenario tree uncomment the next line
        # py_trees.display.render_dot_tree(self.scenario_tree)

        self._agent.setup_sensors(self.ego_vehicles[0], self._debug_mode)

    def run_scenario(self, input_path):
        """
        Trigger the start of the scenario and wait for it to finish/fail
        """
        self.start_system_time = time.time()
        self.start_game_time = GameTime.get_time()

        self._watchdog.start()
        self._running = True
        self.count_tick = 0
        min_dis_npc = 1000
        min_dis_ped = 1000
        self.uq = []
        self.input_path = input_path

        # print(CarlaDataProvider.get_world().get_actors().filter('vehicle*'), len(CarlaDataProvider.get_world().get_actors().filter('vehicle*')))
        # print(CarlaDataProvider.get_world().get_actors().filter('walker*'), len(CarlaDataProvider.get_world().get_actors().filter('walker*')))
        self.elapsed_time = 0
        while self._running:
            # if time.time() - s > 35:
            #     break
            timestamp = None
            world = CarlaDataProvider.get_world()
            if world:
                snapshot = world.get_snapshot()
                if snapshot:
                    timestamp = snapshot.timestamp
            if timestamp:
                self.elapsed_time = timestamp.elapsed_seconds
                # if timestamp.elapsed_seconds > 12:
                #     self._running = False
                if self.count_tick > 155:
                    print(self.count_tick, timestamp.elapsed_seconds)
                    self._running = False

                dis_npc, dis_ped = self._tick_scenario(timestamp)
                min_dis_npc = dis_npc if dis_npc < min_dis_npc else min_dis_npc
                min_dis_ped = dis_ped if dis_ped < min_dis_ped else min_dis_ped

        print('number of ticks: ', self.count_tick)
        print('timestamp.elapsed_seconds', self.elapsed_time)

        return 0.2 * min_dis_ped + 0.8 * min_dis_npc, min(min_dis_npc, min_dis_ped)

    def _tick_scenario(self, timestamp):
        """
        Run next tick of scenario and the agent and tick the world.
        """
        if self._timestamp_last_run < timestamp.elapsed_seconds and self._running:
            self._timestamp_last_run = timestamp.elapsed_seconds
            self.count_tick += 1

            self._watchdog.update()
            # Update game time and actor information
            GameTime.on_carla_tick(timestamp)
            CarlaDataProvider.on_carla_tick()

            try:
                agent_out = self._agent()
                ego_action, tag, uq = agent_out[0], agent_out[1], agent_out[2]

                input_file = int(time.time())
                with open('{}input_data/input_data_{}.pkl'.format(self.input_path, input_file), 'wb') as fp:
                    pickle.dump(uq[0], fp)
                with open('{}global_plan/global_plan_{}.pkl'.format(self.input_path, input_file), 'wb') as fp:
                    pickle.dump(uq[2], fp)
                self.uq.append(['input_data_{}.pkl'.format(input_file), 'global_plan_{}.pkl'.format(input_file), uq[1]])
                if tag is not None:
                    self.tag = tag

            # Special exception inside the agent that isn't caused by the agent
            except SensorReceivedNoData as e:
                raise RuntimeError(e)

            except Exception as e:
                raise AgentError(e)

            self.ego_vehicles[0].apply_control(ego_action)

            # Tick scenario
            self.scenario_tree.tick_once()

            if self._debug_mode:
                print("\n")
                py_trees.display.print_ascii_tree(
                    self.scenario_tree, show_status=True)
                sys.stdout.flush()

            if self.scenario_tree.status != py_trees.common.Status.RUNNING:
                self._running = False

            spectator = CarlaDataProvider.get_world().get_spectator()
            ego_trans = self.ego_vehicles[0].get_transform()
            spectator.set_transform(carla.Transform(ego_trans.location + carla.Location(z=40),
                                                    carla.Rotation(pitch=-90)))

            # spectator.set_transform(carla.Transform(ego_trans.location + carla.Location(x=0, y=-8, z=3),
            #                                         ego_trans.rotation))

        if self._running and self.get_running_status():
            CarlaDataProvider.get_world().tick(self._timeout)

        try:
            min_dis_npc, dis_ped = self._calculate_distance()
        except:
            min_dis_npc, dis_ped = 20, 20
        # return self._calculate_distance()
        return min_dis_npc, dis_ped

    @staticmethod
    def stop_walker(walker, vehicle):
        dis = math.sqrt(
            (vehicle.get_location().x - walker.get_location().x) ** 2 + (
                    vehicle.get_location().y - walker.get_location().y) ** 2)
        # print('walker distance ...', dis)
        if dis < 5:
            # print('stop walker ...')
            walker_control = carla.WalkerControl()
            walker_control.direction = carla.Vector3D(0, 1, 0)
            walker_control.speed = 0  # {0.94,1.43} https://www.fhwa.dot.gov/publications/research/safety/pedbike/05085/chapt8.cfm
            walker_control.jump = False
            walker.apply_control(walker_control)
            return True
        return False

    def calculate_min_ttc(self):
        world = CarlaDataProvider.get_world()
        actors = world.get_actors().filter('vehicle*')
        ego = self.ego_vehicles[0]
        min_ttc = 1000
        for actor in actors:
            if actor.id == ego.id:
                continue
            ttc = self._calculate_ttc(ego, actor)
            print('time to collision: ', ttc)
            min_ttc = ttc if ttc < min_ttc else min_ttc

    @staticmethod
    def _calculate_ttc(ego, npc):
        TTC = Symbol('TTC')
        result = solve(((ego.get_location().x + ego.get_velocity().x * TTC +
                         1 / 2 * ego.get_acceleration().x * TTC ** 2) -
                        (npc.get_location().x + npc.get_velocity().x * TTC +
                         1 / 2 * npc.get_acceleration().x * TTC ** 2) ** 2) +

                       ((npc.get_location().y + npc.get_velocity().y * TTC +
                         1 / 2 * npc.get_acceleration().y * TTC ** 2) -
                        (npc.get_location().y + npc.get_velocity().y * TTC +
                         1 / 2 * npc.get_acceleration().y * TTC ** 2) ** 2) -

                       ((ego.get_location().x - npc.get_location().x) ** 2 +
                       (ego.get_location().y - npc.get_location().y) ** 2)
                       )
        return min(result)

    def _calculate_distance(self):
        world = CarlaDataProvider.get_world()
        actors = world.get_actors().filter('vehicle*')
        walkers = world.get_actors().filter('walker*')[0]
        ego_location = self.ego_vehicles[0].get_location()
        min_dis_npc = 1000

        stopped = False
        for actor in actors:
            if not stopped:
                stopped = self.stop_walker(walkers, actor)

            if actor.id == self.ego_vehicles[0].id:
                continue
            actor_location = actor.get_location()
            dis = math.sqrt(
                (ego_location.x - actor_location.x) ** 2 + (ego_location.y - actor_location.y) ** 2)
            # print(dis)
            min_dis_npc = dis if dis < min_dis_npc else min_dis_npc

        dis_ped = math.sqrt(
            (ego_location.x - walkers.get_location().x) ** 2 + (ego_location.y - walkers.get_location().y) ** 2)
        # if dis < min_dis:
        #     min_dis = dis
        # print(min_dis)
        return min_dis_npc, dis_ped

    def get_running_status(self):
        """
        returns:
           bool: False if watchdog exception occured, True otherwise
        """
        return self._watchdog.get_status()

    def stop_scenario(self):
        """
        This function triggers a proper termination of a scenario
        """
        self._watchdog.stop()

        self.end_system_time = time.time()
        self.end_game_time = GameTime.get_time()

        self.scenario_duration_system = self.end_system_time - self.start_system_time
        self.scenario_duration_game = self.end_game_time - self.start_game_time

        if self.get_running_status():
            if self.scenario is not None:
                self.scenario.terminate()

            if self._agent is not None:
                self._agent.cleanup()
                self._agent = None

            self.analyze_scenario()

    def analyze_scenario(self):
        """
        Analyzes and prints the results of the route
        """
        global_result = '\033[92m' + 'SUCCESS' + '\033[0m'

        for criterion in self.scenario.get_criteria():
            if criterion.test_status != "SUCCESS":
                global_result = '\033[91m' + 'FAILURE' + '\033[0m'

        if self.scenario.timeout_node.timeout:
            global_result = '\033[91m' + 'FAILURE' + '\033[0m'

        ResultOutputProvider(self, global_result)
