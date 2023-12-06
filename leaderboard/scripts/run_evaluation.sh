#!/bin/bash

export CARLA_ROOT=/home/complexse/workspace/Chengjie/InterFuser/carla
export CARLA_SERVER=${CARLA_ROOT}/CarlaUE4.sh
export PYTHONPATH=$PYTHONPATH:${CARLA_ROOT}/PythonAPI
export PYTHONPATH=$PYTHONPATH:${CARLA_ROOT}/PythonAPI/carla
export PYTHONPATH=$PYTHONPATH:$CARLA_ROOT/PythonAPI/carla/dist/carla-0.9.10-py3.7-linux-x86_64.egg
export PYTHONPATH=$PYTHONPATH:leaderboard
export PYTHONPATH=$PYTHONPATH:leaderboard/team_code
export PYTHONPATH=$PYTHONPATH:scenario_runner

#export CARLA_ROOT=/path/to/carla/root
#export ROUTES=leaderboard/example_data/evaluation_routes/routes_town05_long.xml
#export TEAM_AGENT=leaderboard/team_code/interfuser_agent.py
#export TEAM_CONFIG=leaderboard/team_code/interfuser_config.py
#export CHECKPOINT_ENDPOINT=results/interfuser_result.json
#export SCENARIOS=leaderboard/example_data/scenarios/town05_all_scenarios.json

export LEADERBOARD_ROOT=leaderboard
export CHALLENGE_TRACK_CODENAME=SENSORS
export PORT=2000 # same as the carla server port
export TM_PORT=2500 # port for traffic manager, required when spawning multiple servers/clients
export DEBUG_CHALLENGE=0
export REPETITIONS=1 # multiple evaluation runs
export ROUTES=leaderboard/data/42routes/Town01_Scenario1.xml
export TEAM_AGENT=leaderboard/team_code/interfuser_agent.py # agent
export TEAM_CONFIG=leaderboard/team_code/interfuser_config.py # model checkpoint, not required for expert
export CHECKPOINT_ENDPOINT=results/sample_result.json # results file
export SCENARIOS=leaderboard/data/42routes/Town01_Scenario1.json
export SAVE_PATH=data/eval # path for saving episodes while evaluating
#export RESUME=True

python3 ${LEADERBOARD_ROOT}/leaderboard/leaderboard_evaluator.py \
--scenarios=${SCENARIOS}  \
--routes=${ROUTES} \
--repetitions=${REPETITIONS} \
--track=${CHALLENGE_TRACK_CODENAME} \
--checkpoint=${CHECKPOINT_ENDPOINT} \
--agent=${TEAM_AGENT} \
--agent-config=${TEAM_CONFIG} \
--debug=${DEBUG_CHALLENGE} \
--record=${RECORD_PATH} \
--resume=${RESUME} \
--port=${PORT} \
--trafficManagerPort=${TM_PORT}

