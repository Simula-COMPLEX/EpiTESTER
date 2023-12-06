#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 27.09.2023 15:29
# @Author  : 
# @File    : all_three.py
# @Software: PyCharm

import argparse
import os
import subprocess
import time

import strategy_epiga as epiga
import strategy_ga as ga
import strategy_epiga_model as epiga_model

# PATH = '/home/chengjielu/D1/projects/epiga-carla/epiga-project'

PATH = '/home/complexse/workspace/Chengjie/InterFuser'  # local path


if __name__ == '__main__':
    description = "CARLA AD Leaderboard Evaluation: evaluate your Agent in CARLA scenarios\n"

    # general parameters
    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--host', default='localhost',
                        help='IP of the host server (default: localhost)')
    parser.add_argument('--port', default='3000', required=False, help='TCP port to listen to (default: 2000)')
    parser.add_argument('--trafficManagerPort', required=False, default='8000',
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
                        default='{}/leaderboard/data/42routes/Scenario2_Town2.xml'.format(PATH),
                        help='Name of the route to be executed. Point to the route_xml_file to be executed.',
                        # required=True
                        )
    parser.add_argument('--scenarios',
                        default='{}/leaderboard/data/42routes/Scenario2_Town2.json'.format(PATH),
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
    parser.add_argument("--run", type=int, default=0, required=False, help="Experiment repetition")
    parser.add_argument("--evaluations", type=int, default=2, required=False, help="Evaluations")
    parser.add_argument("--scenario_id", type=str, default='scenario_2', required=False, help="Scenario ID")

    arguments = parser.parse_args()

    #########################
    # GA
    #########################

    os.system('kill $(lsof -t -i:{})'.format(int(arguments.port)))
    os.system('kill $(lsof -t -i:{})'.format(int(arguments.trafficManagerPort)))
    time.sleep(10)
    os.system('kill $(lsof -t -i:{})'.format(int(arguments.port)))
    os.system('kill $(lsof -t -i:{})'.format(int(arguments.trafficManagerPort)))
    time.sleep(10)

    subprocess.Popen(
        ['cd {}/carla/ && DISPLAY= ./CarlaUE4.sh --world-port={} -opengl'.format(PATH, int(arguments.port))],
        stdout=subprocess.PIPE, universal_newlines=True, shell=True)

    logs = 'sbatch strategy_ga.slurm --port={} --trafficManagerPort={} --run={} --evaluations={} --scenario_id={}'. \
        format(int(arguments.port), int(arguments.trafficManagerPort), int(arguments.run), int(arguments.evaluations),
               arguments.scenario_id)
    print('===================================')
    print(logs)
    print('===================================')
    # f = open('./logs/logs.md', mode='a', encoding='utf-8')
    # f.writelines(logs + '\n')

    time.sleep(20)
    ga.main(arguments)

    #########################
    # EpiGA
    #########################

    # os.system('kill $(lsof -t -i:{})'.format(int(arguments.port)))
    # os.system('kill $(lsof -t -i:{})'.format(int(arguments.trafficManagerPort)))
    # time.sleep(10)
    # os.system('kill $(lsof -t -i:{})'.format(int(arguments.port)))
    # os.system('kill $(lsof -t -i:{})'.format(int(arguments.trafficManagerPort)))
    # time.sleep(10)
    #
    # subprocess.Popen(
    #     ['cd {}/carla/ && DISPLAY= ./CarlaUE4.sh --world-port={} -opengl'.format(PATH, int(arguments.port))],
    #     stdout=subprocess.PIPE, universal_newlines=True, shell=True)

    logs = 'sbatch strategy_epiga.slurm --port={} --trafficManagerPort={} --run={} --evaluations={} --scenario_id={}'. \
        format(int(arguments.port), int(arguments.trafficManagerPort), int(arguments.run), int(arguments.evaluations),
               arguments.scenario_id)
    print('===================================')
    print(logs)
    print('===================================')
    f = open('./logs/logs.md', mode='a', encoding='utf-8')
    f.writelines(logs + '\n')

    time.sleep(20)
    epiga.main(arguments)

    #########################
    # EpiGA Model
    #########################

    # os.system('kill $(lsof -t -i:{})'.format(int(arguments.port)))
    # os.system('kill $(lsof -t -i:{})'.format(int(arguments.trafficManagerPort)))
    # time.sleep(10)
    # os.system('kill $(lsof -t -i:{})'.format(int(arguments.port)))
    # os.system('kill $(lsof -t -i:{})'.format(int(arguments.trafficManagerPort)))
    # time.sleep(10)
    #
    # subprocess.Popen(
    #     ['cd {}/carla/ && DISPLAY= ./CarlaUE4.sh --world-port={} -opengl'.format(PATH, int(arguments.port))],
    #     stdout=subprocess.PIPE, universal_newlines=True, shell=True)

    logs = 'sbatch strategy_epig_model.slurm --port={} --trafficManagerPort={} --run={} --evaluations={} --scenario_id={}'. \
        format(int(arguments.port), int(arguments.trafficManagerPort), int(arguments.run), int(arguments.evaluations),
               arguments.scenario_id)
    print('===================================')
    print(logs)
    print('===================================')
    f = open('./logs/logs.md', mode='a', encoding='utf-8')
    f.writelines(logs + '\n')

    time.sleep(20)
    epiga_model.main(arguments)
