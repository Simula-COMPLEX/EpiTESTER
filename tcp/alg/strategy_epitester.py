#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 21.08.2023 22:10
# @Author  : Chengjie
# @File    : strategy_epiga.py
# @Software: PyCharm
import argparse
import os
import subprocess
import time
import traceback

import carla
import torch

from epiga.epiga import EpiGA
from epiga.problems.floatproblem import FloatProblem
from epiga.operators.nucleosomegenerator import NucleosomeGenerator
from epiga.operators.binarytournamentselection import BinaryTournamentSelection
from epiga.operators.nucleosomebasedreproduction import NucleosomeBasedReproduction
from epiga.operators.numericgenesilencing import NumericGeneSilencing
from epiga.operators.elitistreplacement import ElitistReplacement
from leaderboard.leaderboard_evaluator_2 import LeaderboardEvaluator
import pandas as pd
import gc

from leaderboard.utils.route_indexer import RouteIndexer
from leaderboard.utils.statistics_manager import StatisticsManager
from path_utils import get_project_root

PATH = get_project_root()

# os.environ["CUDA_VISIBLE_DEVICES"] = "2"

class ScenarioOptimization(FloatProblem):
    def __init__(self, n_variables, environment, evaluator, args):
        """
        Problem Initialization.

        param int n_variables: the problem size. The number of float numbers in the solution vector (list).
        """
        self.config = None
        self.route_indexer = None

        title = ['npc_vertical', 'npc_horizontal', 'npc_behavior', 'pedestrian_vertical',
                 'pedestrian_horizontal', 'pedestrian_direction_x', 'pedestrian_direction_y',
                 'pedestrian_speed', 'weather_sun_angle', 'weather_fog_density', 'min_dis']
        self.scenario_n = args.scenarios.split('/')[-1].split('.')[0]

        self.path = './logs/epiga_model/{}/run_{}/'.format(args.scenario_id, args.run)
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        self.log_file_name = self.path + self.scenario_n + '.csv'
        pd.DataFrame([title]).to_csv(self.log_file_name, mode='w', header=False, index=False)

        # f = open('./logs/{}.txt'.format(self.scenario_n), mode='w', encoding='utf-8')

        """
        NPC: {vertical: [-20, 20], horizontal: [-20, 20], behavior: [0,0.3]}

        Pedestrian: {vertical: [-20, 20], horizontal: [-20, 20], direction_x: [-1, 1],
         direction_y: [-1, 1], speed: [0.94, 1.43]}

        Weather: {sun_altitude_angle: [-90, 90], fog_density: [0, 100]}
        """
        lower_bounds = [0] * n_variables
        upper_bounds = [1] * n_variables

        self.evaluator = evaluator
        self.args = args
        self.set_route()

        super().__init__("My ADS Problem", n_variables, lower_bounds, upper_bounds, environment,
                         FloatProblem.MINIMIZATION)

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

    @staticmethod
    def start_simulation():
        os.system('echo simula | sudo docker run --privileged --gpus all --net=host -v '
                  '/tmp/.X11-unix:/tmp/.X11-unix:rw carlasim/carla:0.9.14 /bin/bash ./CarlaUE4.sh --world-port=2000 '
                  '-RenderOffScreen')

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

        if self.evaluator.collision:
            objective = 0
            min_dis = 0

        gc.collect()

        # if min_dis == 0:
        #     f = open('./logs/{}.txt'.format(self.scenario_n), mode='a', encoding='utf-8')
        #     f.writelines(str(solution).replace('[', '').replace(']', '').replace("'", '').replace(",", '') + '\n')

        pd.DataFrame([solution + [min_dis]]).to_csv(self.log_file_name, mode='a', header=False,
                                                    index=False)

        return objective

    def k(self, position):
        """
        Overrides the attenuation coefficient. Controls the convergence speed.

        :param int position: the position in the solution vector (list).
        :return: the fitness value.
        :rtype: float
        """
        return 200 / self.evaluations


def main(args):
    """
    start
    """
    statistics_manager = StatisticsManager()

    L = 10

    envs = {'scenario_1':  [0.6006, 0.1178, 0.9986, 0.8089, 0.3451, 0.9935, 0.9985, 0.1263,
                           0.1056, 0.006],
            'scenario_2':  [0.5019, 0.9903, 0.9795, 0.9387, 0.4386, 0.9674, 0.1160, 0.0958,
                           0.5792, 0.0015],
            'scenario_3':  [0.926, 0.6574, 0.9984, 0.9605, 0.1184, 0.5834, 0.9557, 0.1300,
                           0.7391, 0.0038],
            'scenario_4':  [0.8756, 0.9933, 0.9061, 0.9745, 0.8622, 0.9611, 0.8341, 0.0085,
                           0.952, 0.0007],
            'scenario_5':  [0.8044, 0.9841, 0.9794, 0.9788, 0.8668, 0.9408, 0.274, 0.0209,
                           0.9315, 0.001],
            'scenario_6': [0.9365, 0.9556, 0.9991, 0.938, 0.5043, 0.6414, 0.9231, 0.0072,
                           0.7993, 0.0006]
            }
    env = envs[args.scenario_id]

    try:
        leaderboard_evaluator = LeaderboardEvaluator(args, statistics_manager)
        p = ScenarioOptimization(L, environment=env, evaluator=leaderboard_evaluator, args=args)
        alg = EpiGA(p, 20, 1,
                    NucleosomeGenerator(2 / L, 1),
                    BinaryTournamentSelection(),
                    NucleosomeBasedReproduction(),
                    NumericGeneSilencing(1 / L, p.path),
                    ElitistReplacement(duplicates=False))
        alg.run(int(args.evaluations), 1, p.path + "solution.txt", p.path + "stats.txt")

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
    parser.add_argument('--port', default='2000', required=True, help='TCP port to listen to (default: 2000)')
    parser.add_argument('--trafficManagerPort', required=True, default='8000',
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
                        default='{}/leaderboard/data/scenarios/scenario_1.xml'.format(PATH),
                        help='Name of the route to be executed. Point to the route_xml_file to be executed.',
                        # required=True
                        )
    parser.add_argument('--scenarios',
                        default='{}/leaderboard/data/scenarios/scenario_1.json'.format(PATH),
                        help='Name of the scenario annotation file to be mixed with the route.',
                        # required=True
                        )
    parser.add_argument('--repetitions',
                        type=int,
                        default=1,
                        help='Number of repetitions per route.')

    # agent-related options
    parser.add_argument("-a", "--agent",
                        default='{}/leaderboard/team_code/tcp_agent.py'.format(PATH),
                        type=str, help="Path to Agent's py file to evaluate",
                        # required=True
                        )
    parser.add_argument("--agent-config",
                        default='{}/leaderboard/leaderboard/model/best_model.ckpt'.format(PATH),
                        type=str, help="Path to Agent's configuration file")

    parser.add_argument("--track", type=str, default='SENSORS', help="Participation track: SENSORS, MAP")
    parser.add_argument('--resume', type=bool, default=False, help='Resume execution from last checkpoint?')
    parser.add_argument("--checkpoint", type=str,
                        default='./simulation_results.json',
                        help="Path to checkpoint used for saving statistics and resuming")
    parser.add_argument("--checkpoint_path", type=str,
                        default='{}/epiga/alg/results/ga/simulation_results_scenario_2/'.format(PATH),
                        help="Path to checkpoint used for saving statistics and resuming")
    parser.add_argument("--run", type=int, default=20, required=True, help="Experiment repetition")
    parser.add_argument("--evaluations", type=int, default=1000, required=False, help="Evaluations")
    parser.add_argument("--scenario_id", type=str, default='scenario_1', required=True, help="Scenario ID")

    arguments = parser.parse_args()

    os.system('kill $(lsof -t -i:{})'.format(int(arguments.port)))
    os.system('kill $(lsof -t -i:{})'.format(int(int(arguments.port) - int(arguments.port) / arguments.run)))

    os.system('kill $(lsof -t -i:{})'.format(int(arguments.trafficManagerPort)))
    os.system('kill $(lsof -t -i:{})'.format(int(int(arguments.port) - int(arguments.port) / arguments.run + 100)))

    time.sleep(10)
    os.system('kill $(lsof -t -i:{})'.format(int(arguments.port)))
    os.system('kill $(lsof -t -i:{})'.format(int(int(arguments.port) - int(arguments.port) / arguments.run)))

    os.system('kill $(lsof -t -i:{})'.format(int(arguments.trafficManagerPort)))
    os.system('kill $(lsof -t -i:{})'.format(int(int(arguments.port) - int(arguments.port) / arguments.run + 100)))

    time.sleep(10)

    subprocess.Popen(
        ['cd {}/carla/ && DISPLAY= ./CarlaUE4.sh --world-port={} -opengl'.format(PATH, int(arguments.port))],
        stdout=subprocess.PIPE, universal_newlines=True, shell=True)

    logs = 'sbatch strategy_epiga.slurm scenario_id={} --port={} --trafficManagerPort={} --run={} --evaluations={}'. \
        format(arguments.scenario_id, int(arguments.port), int(arguments.trafficManagerPort), int(arguments.run),
               int(arguments.evaluations))
    print('===================================')
    print(logs)
    print('===================================')
    f = open('./logs/logs.md', mode='a', encoding='utf-8')
    f.writelines(logs + '\n')

    time.sleep(20)
    # try:
    main(arguments)
    os.system('kill $(lsof -t -i:{})'.format(int(arguments.port)))
    os.system('kill $(lsof -t -i:{})'.format(int(arguments.trafficManagerPort)))
    time.sleep(10)
    os.system('kill $(lsof -t -i:{})'.format(int(arguments.port)))
    os.system('kill $(lsof -t -i:{})'.format(int(arguments.trafficManagerPort)))
    time.sleep(10)
    os.system('kill $(lsof -t -i:{})'.format(int(arguments.port)))
    os.system('kill $(lsof -t -i:{})'.format(int(arguments.trafficManagerPort)))
    # except:
    #     os.system('kill $(lsof -t -i:2000)')
    #     time.sleep(10)
    #     subprocess.Popen(
    #         ['cd /home/chengjielu/D1/projects/epiga-carla/epiga-project/carla/ && DISPLAY= ./CarlaUE4.sh -opengl'],
    #         stdout=subprocess.PIPE, universal_newlines=True, shell=True)
    #     time.sleep(10)
