#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 21.08.2023 22:10
# @Author  : Chengjie
# @File    : strategy_epiga.py
# @Software: PyCharm
import argparse
import gc
import os
import subprocess
import time
import traceback
from os.path import dirname

import pandas as pd

from epiga.epiga import EpiGA
from epiga.operators.binarytournamentselection import BinaryTournamentSelection
from epiga.operators.elitistreplacement import ElitistReplacement
from epiga.operators.nucleosomebasedreproduction import NucleosomeBasedReproduction
from epiga.operators.nucleosomegenerator import NucleosomeGenerator
from epiga.operators.numericgenesilencing import NumericGeneSilencing
from epiga.problems.floatproblem import FloatProblem
from leaderboard.leaderboard_evaluator_2 import LeaderboardEvaluator
from leaderboard.utils.route_indexer import RouteIndexer
from leaderboard.utils.statistics_manager import StatisticsManager
from path_utils import get_project_root

PATH = get_project_root()


class ScenarioOptimization(FloatProblem):
    def __init__(self, n_variables, environment, evaluator, args):
        """
        Problem Initialization.

        :param int n_variables: the problem size. The number of float numbers in the solution vector (list).
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

    # envs = {'scenario_1': [0.9978, 0.9999, 0.6610, 0.9978, 0.9999, 0.9861, 1.0000, 0.9761,
    #                        0.9981, 0.6075],
    #         'scenario_2': [0.9977, 0.9987, 0.0217, 0.9953, 0.9996, 0.9880, 0.9998, 0.8468,
    #                        0.9975, 0.1451],
    #         'scenario_3': [0.9881, 0.9992, 0.0430, 0.9901, 0.9997, 0.9671, 0.9998, 0.9363,
    #                        0.9975, 0.7384],
    #         'scenario_4': [0.9953, 0.9987, 0.0608, 0.9894, 0.9998, 0.9526, 1.0000, 0.8228,
    #                        0.9983, 0.6538],
    #         }

    envs = {'scenario_1': [0.9978, 0.9999, 0.6610, 0.9978, 0.9999, 0.9861, 1.0000, 0.9761,
                           0.9981, 0.6075],
            # 'scenario_1': [0.6616, 0.9924, 0.6521, 0.6771, 0.9639, 0.9626, 0.1263, 0.9663,
            #                0.0083, 0.4031],
            'scenario_2': [0.9492, 0.9961, 0.5908, 0.9811, 0.1556, 0.6454, 0.1561, 0.9282,
                           0.0060, 0.5017],
            'scenario_3': [0.4335, 0.9950, 0.6238, 0.9467, 0.9354, 0.6524, 0.2173, 0.9658,
                           0.0291, 0.5827],
            'scenario_4': [0.8298, 0.9971, 0.5753, 0.9398, 0.7376, 0.8373, 0.2104, 0.8913,
                           0.0184, 0.7678],
            }  # model_0.0001_64_dataset4_2000.csv_1_model5_2.pth

    # envs = {'scenario_1': [0.2087, 0.9540, 0.3372, 0.1045, 0.9740, 0.7171, 0.9611, 0.2486,
    #                        0.9495, 0.9772],
    #         'scenario_2': [0.2924, 0.9636, 0.3709, 0.0958, 0.9574, 0.8925, 0.9458, 0.5331,
    #                        0.8900, 0.9784],
    #         'scenario_3': [0.6281, 0.9619, 0.8447, 0.3142, 0.9558, 0.8885, 0.8665, 0.3868,
    #                        0.8962, 0.972],
    #         'scenario_4': [0.2453, 0.9557, 0.4447, 0.0926, 0.9660, 0.8315, 0.8835, 0.4118,
    #                        0.9076, 0.9753]
    #         }   # model_0.0001_64_dataset4_1500.csv_1_model5.pth

    env = envs[args.scenario_id]

    # env = [0.5] * L

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
    parser.add_argument('--port', default='3000', required=False, help='TCP port to listen to (default: 2000)')
    parser.add_argument('--trafficManagerPort', required=False, default='3050',
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
                        default='{}/leaderboard/data/42routes/Scenario1_Town1.xml'.format(PATH),
                        help='Name of the route to be executed. Point to the route_xml_file to be executed.',
                        # required=True
                        )
    parser.add_argument('--scenarios',
                        default='{}/leaderboard/data/42routes/Scenario1_Town1.json'.format(PATH),
                        help='Name of the scenario annotation file to be mixed with the route.',
                        # required=True
                        )
    parser.add_argument('--repetitions',
                        type=int,
                        default=1,
                        help='Number of repetitions per route.')

    # agent-related options
    parser.add_argument("-a", "--agent",
                        default='{}/leaderboard/team_code/interfuser_agent.py'.format(PATH),
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
                        help="Path to checkpoint used for saving statistics and resuming")
    parser.add_argument("--checkpoint_path", type=str,
                        default='{}/epiga/alg/results/simulation_results_scenario_1/'.format(PATH),
                        help="Path to checkpoint used for saving statistics and resuming")
    parser.add_argument("--run", type=int, default=1, required=False, help="Experiment repetition")
    parser.add_argument("--evaluations", type=int, default=1000, required=False, help="Evaluations")
    parser.add_argument("--scenario_id", type=str, default='scenario_1', required=False, help="Scenario ID")

    arguments = parser.parse_args()

    os.system('kill $(lsof -t -i:{})'.format(int(arguments.port)))
    os.system('kill $(lsof -t -i:{})'.format(int(arguments.trafficManagerPort)))
    time.sleep(10)
    os.system('kill $(lsof -t -i:{})'.format(int(arguments.port)))
    os.system('kill $(lsof -t -i:{})'.format(int(arguments.trafficManagerPort)))
    time.sleep(10)
    subprocess.Popen(
        ['cd {}/carla/ && ./CarlaUE4.sh --world-port={} -opengl'.format(PATH, int(arguments.port))],
        stdout=subprocess.PIPE, universal_newlines=True, shell=True)

    # no display mode
    # subprocess.Popen(
    #     ['cd {}/carla/ && DISPLAY= ./CarlaUE4.sh --world-port={} -opengl'.format(PATH, int(arguments.port))],
    #     stdout=subprocess.PIPE, universal_newlines=True, shell=True)

    logs = 'sbatch strategy_epiga.slurm --port={} --trafficManagerPort={} --run={} --evaluations={}'.format(
        int(arguments.port), int(arguments.trafficManagerPort), int(arguments.run), int(arguments.evaluations))
    print('===================================')
    print(logs)
    print('===================================')
    f = open('./logs/logs.md', mode='a', encoding='utf-8')
    f.writelines(logs + '\n')

    time.sleep(20)
    main(arguments)
