#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 06.09.2023 20:34
# @Author  : Chengjie
# @File    : strategy_random.py
# @Software: PyCharm
import argparse
import os
import random
import subprocess
import time
import traceback

import torch

from leaderboard.leaderboard_evaluator_2 import LeaderboardEvaluator
import pandas as pd
import gc
import numpy as np

from leaderboard.utils.route_indexer import RouteIndexer
from leaderboard.utils.statistics_manager import StatisticsManager
from path_utils import get_project_root

PATH = get_project_root()

os.environ["CUDA_VISIBLE_DEVICES"] = "0"


class RandomGeneration:
    def __init__(self, n_variables, evaluator, args):
        """
        Problem Initialization.

        :param int n_variables: the problem size. The number of float numbers in the solution vector (list).
        """
        self.config = None
        self.route_indexer = None

        title = ['state_image', 'state_bev', 'npc_vertical', 'npc_horizontal', 'npc_behavior', 'pedestrian_vertical',
                 'pedestrian_horizontal', 'pedestrian_direction_x', 'pedestrian_direction_y',
                 'pedestrian_speed', 'weather_sun_angle', 'weather_fog_density', 'min_dis']
        self.scenario_n = args.scenarios.split('/')[-1].split('.')[0]

        self.path = 'logs/random/'
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        self.log_file_name = self.path + self.scenario_n + '.csv'
        # pd.DataFrame([title]).to_csv(self.log_file_name, mode='w', header=False, index=False)

        open('./logs/{}.txt'.format(self.scenario_n), mode='w', encoding='utf-8')

        """
        NPC: {vertical: [-20, 20], horizontal: [-20, 20], behavior: [0,0.3]}

        Pedestrian: {vertical: [-20, 20], horizontal: [-20, 20], direction_x: [-1, 1],
         direction_y: [-1, 1], speed: [0.94, 1.43]}

        Weather: {sun_altitude_angle: [-90, 90], fog_density: [0, 100]}
        """
        self.lower_bounds = [0] * n_variables
        self.upper_bounds = [1] * n_variables

        self.evaluations = 1
        self.evaluator = evaluator
        self.args = args
        self.set_route()

    def generate_solution(self):
        solution = []
        for i in range(len(self.lower_bounds)):
            solution.append(np.random.uniform(self.lower_bounds[i], self.upper_bounds[i]))

        # solution = [0.40848411053049494, 0.8680738786279684, 0.11936958073478766, 0.5687805236319589,
        #             0.04751147672321509,
        #             0.3531664222834868, 0, 0.5093679625480069, 0.6184932884337676, 0.8491408184997938]

        return solution

    @staticmethod
    def calculate_solution(solution):
        lower_bounds_real = [-20, -20, 0, -10, -10, -1, -1, 0.94, -90, 0]
        upper_bounds_real = [20, 20, 0.3, 10, 10, 1, 1, 1.43, 90, 100]

        solution_real = []
        for i in range(len(solution)):
            solution_real.append(solution[i] * (upper_bounds_real[i] - lower_bounds_real[i]) + lower_bounds_real[i])
        return solution_real

    def set_route(self):
        self.route_indexer = RouteIndexer(self.args.routes, self.args.scenarios, self.args.repetitions)

        if self.args.resume:
            self.route_indexer.resume(self.args.checkpoint)
            self.evaluator.statistics_manager.resume(self.args.checkpoint)
        else:
            self.evaluator.statistics_manager.clear_record(self.args.checkpoint)
            self.route_indexer.save_state(self.args.checkpoint)

        self.config = self.route_indexer.next()

    def _get_fitness(self, solution):
        """
        Implements the Fitness calculation.
        Evaluates the solution made of a list of float numbers of length equal to the problem size.

        :param list[float] solution: the solution vector. A list of float numbers.
        :return: the fitness value.
        :rtype: float
        """

        print('Evaluation Step: {}'.format(self.evaluations))
        solution = self.calculate_solution(solution)

        # run
        self.evaluator._load_and_run_scenario(self.args, self.config, solution)
        min_dis = self.evaluator.min_dis
        objective = self.evaluator.objective

        print(min_dis, objective)

        if self.evaluator.collision:
            objective = 0
            min_dis = 0

        pd.DataFrame(
            [['rgb_{}'.format(self.evaluator.tag), 'bev_{}'.format(self.evaluator.tag)] + solution + [min_dis]]).to_csv(
            self.log_file_name, mode='a', header=False,
            index=False)

        gc.collect()

        # if min_dis == 0:
        #     f = open('{}/{}.txt'.format(self.path, self.scenario_n), mode='a', encoding='utf-8')
        #     f.writelines(str(solution).replace('[', '').replace(']', '').replace("'", '').replace(",", '') + '\n')

        self.evaluations += 1

        return objective

    def run(self, repetition):
        while self.evaluations < repetition:
            self._get_fitness(self.generate_solution())

    def run_solutions(self, solution):
        solution = self.calculate_solution(solution)
        self.evaluator._load_and_run_scenario(self.args, self.config, solution)
        min_dis = self.evaluator.min_dis
        objective = self.evaluator.objective

        print(min_dis, objective)
        min_dis_ = min_dis

        print('score_route: ', self.evaluator.score_route)
        print('score_penalty: ', self.evaluator.score_penalty)
        print('score_composed: ', self.evaluator.score_composed)

        sr = self.evaluator.score_route
        sp = self.evaluator.score_penalty
        sc = self.evaluator.score_composed

        elapsed_seconds = self.evaluator.elapsed_seconds
        ticks = self.evaluator.ticks
        checkpoint = self.evaluator.checkpoint_file
        uq = self.evaluator.uncertainty_quantification

        if self.evaluator.collision:
            min_dis = 0

        gc.collect()
        return objective, min_dis_, min_dis, sr, sp, sc, elapsed_seconds, ticks, checkpoint, uq


def main(args):
    """
    start
    """
    statistics_manager = StatisticsManager()

    L = 10

    try:
        leaderboard_evaluator = LeaderboardEvaluator(args, statistics_manager)

        random_alg = RandomGeneration(L, evaluator=leaderboard_evaluator, args=args)
        random_alg.run(repetition=args.evaluations)

    except Exception as e:
        traceback.print_exc()
    finally:
        del leaderboard_evaluator


if __name__ == '__main__':
    description = "CARLA AD Leaderboard Evaluation: evaluate your Agent in CARLA scenarios\n"

    # general parameters
    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--host', default='localhost',
                        help='IP of the host server (default: localhost)')
    parser.add_argument('--port', default='7000', required=False, help='TCP port to listen to (default: 2000)')
    parser.add_argument('--trafficManagerPort', required=False, default='7050',
                        help='Port to use for the TrafficManager (default: 8000)')
    parser.add_argument('--trafficManagerSeed', default='1',
                        help='Seed used by the TrafficManager (default: 0)')
    parser.add_argument('--carlaProviderSeed', default='2000',
                        help='Seed used by the CarlaProvider (default: 2000)')
    parser.add_argument('--debug', type=int, help='Run with debug output', default=0)
    parser.add_argument('--record', type=str, default='',
                        help='Use CARLA recording feature to create a recording of the scenario')
    parser.add_argument('--timeout', default="120.0",
                        help='Set the CARLA client timeout value in seconds')

    # simulation setup
    parser.add_argument('--routes',
                        default='{}/leaderboard/data/42routes/Scenario4_Town4.xml'.format(PATH),
                        help='Name of the route to be executed. Point to the route_xml_file to be executed.',
                        # required=True
                        )
    parser.add_argument('--scenarios',
                        default='{}/leaderboard/data/42routes/Scenario4_Town4.json'.format(PATH),
                        help='Name of the scenario annotation file to be mixed with the route.',
                        # required=True
                        )
    parser.add_argument('--repetitions',
                        type=int,
                        default=1,
                        help='Number of repetitions per route.')

    # agent-related options
    parser.add_argument("-a", "--agent",
                        default='{}/leaderboard/team_code/interfuser_agent_local_uq.py'.format(PATH),
                        type=str, help="Path to Agent's py file to evaluate",
                        # required=True
                        )
    parser.add_argument("--agent-config",
                        default='{}/leaderboard/team_code/interfuser_config.py'.format(PATH),
                        type=str, help="Path to Agent's configuration file")

    parser.add_argument("--track", type=str, default='SENSORS', help="Participation track: SENSORS, MAP")
    parser.add_argument('--resume', type=bool, default=False, help='Resume execution from last checkpoint?')
    parser.add_argument("--checkpoint", type=str,
                        default='./simulation_results.json',
                        # '{}/simulation_results_{}.json'.format(args.checkpoint, str(int(time.time())))
                        help="Path to checkpoint used for saving statistics and resuming")
    parser.add_argument("--checkpoint_path", type=str,
                        default='{}/epiga/alg/results/simulation_results_scenario_4/'.format(PATH),
                        # '{}/simulation_results_{}.json'.format(args.checkpoint, str(int(time.time())))
                        help="Path to checkpoint used for saving statistics and resuming")
    parser.add_argument("--run", type=int, default=0, required=False, help="Experiment repetition")
    parser.add_argument("--evaluations", type=int, default=1000, required=False, help="Evaluations")
    parser.add_argument("--scenario_id", type=str, default='scenario_4', required=False, help="Scenario ID")

    arguments = parser.parse_args()

    os.system('kill $(lsof -t -i:{})'.format(int(arguments.port)))
    os.system('kill $(lsof -t -i:{})'.format(int(arguments.trafficManagerPort)))
    time.sleep(10)
    subprocess.Popen(
        ['cd {}/carla/ && DISPLAY= ./CarlaUE4.sh --world-port={} -opengl'.format(PATH, int(arguments.port))],
        stdout=subprocess.PIPE, universal_newlines=True, shell=True)

    logs = 'sbatch strategy_ga.slurm --port={} --trafficManagerPort={} --run={} --evaluations={}'.format(
        int(arguments.port), int(arguments.trafficManagerPort), int(arguments.run), int(arguments.evaluations))
    print('===================================')
    print(logs)
    print('===================================')
    f = open('./logs/logs.md', mode='a', encoding='utf-8')
    f.writelines(logs + '\n')

    time.sleep(20)
    try:
        main(arguments)
    except:
        os.system('kill $(lsof -t -i:{})'.format(int(arguments.port)))
        os.system('kill $(lsof -t -i:{})'.format(int(arguments.trafficManagerPort)))
    finally:
        os.system('kill $(lsof -t -i:{})'.format(int(arguments.port)))
        os.system('kill $(lsof -t -i:{})'.format(int(arguments.trafficManagerPort)))
