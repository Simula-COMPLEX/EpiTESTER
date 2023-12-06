#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 06.09.2023 20:34
# @Author  : Chengjie
# @File    : strategy_ga.py
# @Software: PyCharm
import argparse
import os
import subprocess
import time
import traceback

from jmetal.algorithm.singleobjective.genetic_algorithm import GeneticAlgorithm
from jmetal.operator import PolynomialMutation, SBXCrossover
from jmetal.util.solution import print_function_values_to_file, print_variables_to_file
from jmetal.util.termination_criterion import StoppingByEvaluations
from leaderboard.leaderboard_evaluator_2 import LeaderboardEvaluator
import pandas as pd
import gc
import numpy as np
from jmetal.core.problem import FloatProblem
from jmetal.core.solution import FloatSolution

from leaderboard.utils.route_indexer import RouteIndexer
from leaderboard.utils.statistics_manager import StatisticsManager
from path_utils import get_project_root

PATH = get_project_root()


class GAGeneration(FloatProblem):
    def __init__(self, number_of_variables, evaluator, args):
        """
        Problem Initialization.

        :param int number_of_variables: the problem size. The number of float numbers in the solution vector (list).
        """
        super(GAGeneration, self).__init__()
        self.config = None
        self.route_indexer = None

        title = ['npc_vertical', 'npc_horizontal', 'npc_behavior', 'pedestrian_vertical',
                 'pedestrian_horizontal', 'pedestrian_direction_x', 'pedestrian_direction_y',
                 'pedestrian_speed', 'weather_sun_angle', 'weather_fog_density', 'min_dis']
        self.scenario_n = args.scenarios.split('/')[-1].split('.')[0]

        self.path = './logs/ga/{}/run_{}/'.format(args.scenario_id, args.run)
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        self.log_file_name = self.path + self.scenario_n + '.csv'
        pd.DataFrame([title]).to_csv(self.log_file_name, mode='w', header=False, index=False)

        """
        NPC: {vertical: [-20, 20], horizontal: [-20, 20], behavior: [0,0.3]}

        Pedestrian: {vertical: [-20, 20], horizontal: [-20, 20], direction_x: [-1, 1],
         direction_y: [-1, 1], speed: [0.94, 1.43]}

        Weather: {sun_altitude_angle: [-90, 90], fog_density: [0, 100]}
        """
        self.obj_directions = [self.MINIMIZE]
        self.obj_labels = ["f(x)"]

        self.lower_bound = [0] * number_of_variables
        self.upper_bound = [1] * number_of_variables
        FloatSolution.lower_bound = self.lower_bound
        FloatSolution.upper_bound = self.upper_bound

        self.evaluations = 1
        self.evaluator = evaluator
        self.args = args
        self.set_route()

    def number_of_objectives(self) -> int:
        return 1

    def number_of_constraints(self) -> int:
        return 0

    def generate_solution(self):
        solution = []
        for i in range(len(self.lower_bound)):
            solution.append(np.random.uniform(self.lower_bound[i], self.upper_bound[i]))

        return solution

    @staticmethod
    def calculate_solution(solution):
        lower_bounds_real = [-20, -20, 0, -10, -10, -1, -1, 0.94, -90, 0]
        upper_bounds_real = [20, 20, 0.3, 10, 10, 1, 1, 1.43, 90, 100]

        solution_real = []
        for i in range(solution.number_of_variables):
            solution_real.append(
                solution.variables[i] * (upper_bounds_real[i] - lower_bounds_real[i]) + lower_bounds_real[i])
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

    def evaluate(self, solution: FloatSolution) -> FloatSolution:
        """
        Implements the Fitness calculation.
        Evaluates the solution made of a list of float numbers of length equal to the problem size.

        :param list[float] solution: the solution vector. A list of float numbers.
        :return: the fitness value.
        :rtype: float
        """

        print('Evaluation Step: {}'.format(self.evaluations))
        real_solution = self.calculate_solution(solution)

        # run
        self.evaluator._load_and_run_scenario(self.args, self.config, real_solution)
        min_dis = self.evaluator.min_dis
        objective = self.evaluator.objective

        if self.evaluator.collision:
            objective = 0
            min_dis = 0

        gc.collect()

        pd.DataFrame([real_solution + [min_dis]]).to_csv(self.log_file_name, mode='a', header=False,
                                                         index=False)

        self.evaluations += 1

        solution.objectives[0] = objective

        return solution

    def name(self) -> str:
        return "GAGeneration"


def main(args):
    print('Termination criterion: {}'.format(args.evaluations))
    """
    start
    """
    statistics_manager = StatisticsManager()
    L = 10

    try:
        leaderboard_evaluator = LeaderboardEvaluator(args, statistics_manager)

        ga_problem = GAGeneration(number_of_variables=L, evaluator=leaderboard_evaluator, args=args)
        algorithm = GeneticAlgorithm(
            problem=ga_problem,
            population_size=20,
            offspring_population_size=1,
            mutation=PolynomialMutation(1.0 / ga_problem.number_of_variables(), 20.0),
            crossover=SBXCrossover(0.9, 5.0),
            termination_criterion=StoppingByEvaluations(max_evaluations=args.evaluations),
        )

        algorithm.run()
        result = algorithm.get_result()

        print("Algorithm: {}".format(algorithm.get_name()))
        print("Problem: {}".format(ga_problem.name()))
        print("Solution: {}".format(result.variables))
        print("Fitness: {}".format(result.objectives[0]))
        print("Computing time: {}".format(algorithm.total_computing_time))

        # Save results to file
        print_function_values_to_file(result, './logs/ga/{}/run_{}/objective.txt'.format(args.scenario_id, args.run))
        print_variables_to_file(result, './logs/ga/{}/run_{}/solution.txt'.format(args.scenario_id, args.run))

    except Exception as e:
        traceback.print_exc()
    finally:
        del leaderboard_evaluator


if __name__ == "__main__":
    description = "CARLA AD Leaderboard Evaluation: evaluate your Agent in CARLA scenarios\n"

    # general parameters
    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--host', default='localhost',
                        help='IP of the host server (default: localhost)')
    parser.add_argument('--port', default='2700', required=False, help='TCP port to listen to (default: 2000)')
    parser.add_argument('--trafficManagerPort', required=False, default='2750',
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
                        default='{}/epiga/alg/results/simulation_results_no_uq_scenario_2/'.format(PATH),
                        help="Path to checkpoint used for saving statistics and resuming")
    parser.add_argument("--run", type=int, default=7, required=False, help="Experiment repetition")
    parser.add_argument("--evaluations", type=int, default=1000, required=False, help="Evaluations")
    parser.add_argument("--scenario_id", type=str, default='scenario_4', required=False, help="Scenario ID")

    arguments = parser.parse_args()

    os.system('kill $(lsof -t -i:{})'.format(int(arguments.port)))
    os.system('kill $(lsof -t -i:{})'.format(int(arguments.trafficManagerPort)))
    time.sleep(10)
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
    main(arguments)
