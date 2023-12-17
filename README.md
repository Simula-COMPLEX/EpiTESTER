# EpiTESTER: Testing Autonomous Vehicles with Epigenetic Algorithm and Attention Mechanism

> This repository contains the replication package for the paper [EpiTESTER: Testing Autonomous Vehicles with Epigenetic Algorithm and Attention Mechanism](https://arxiv.org/abs/2312.00207).
> To facilitate reviewing our proposed approach, reviewers please refer to the corresponding data in this repository.
> This repository also contains the source code of our tool.<br/>

## Table of Contents
- [Abstract](#abstract)
- [Running Environment](#running-environment)
- [Scenario Generation](#scenario-generation)


## Abstract
Testing autonomous vehicles (AVs) under various environmental scenarios that lead the vehicles to unsafe situations is known to be challenging. Given the infinite possible environmental scenarios, it is essential to find critical scenarios efficiently. To this end, we propose a novel testing method, named EpiTESTER, by taking inspiration from epigenetics, which enables species to adapt to sudden environmental changes. In particular, EpiTESTER adopts gene silencing as its epigenetic mechanism, which regulates gene expression to prevent the expression of a certain gene, and the probability of gene expression is dynamically computed as the environment changes. Given different data modalities (e.g., images, lidar point clouds) in the context of AV, EpiTESTER benefits from a multi-model fusion transformer to extract high-level feature representations from environmental factors and then calculates probabilities based on these features with the attention mechanism. To assess the cost-effectiveness of EpiTESTER, we compare it with a classical genetic algorithm (GA) (i.e., without any epigenetic mechanism implemented) and EpiTESTER with equal probability for each gene. We evaluate EpiTESTER with four initial environments from CARLA, an open-source simulator for autonomous driving research, and an end-to-end AV controller, Interfuser. Our results show that EpiTESTER achieved a promising performance in identifying critical scenarios compared to the baselines, showing that applying epigenetic mechanisms is a good option for solving practical problems.

<div align=center><img src="https://github.com/Simula-COMPLEX/EpiTESTER/blob/main/assets/overview.png" width="960" /></div>

## Running Environment

Install the latest version of Anaconda

```sh
sudo apt-get update
sudo apt-get upgrade

wget https://repo.anaconda.com/archive/Anaconda3-2023.09-0-Linux-x86_64.sh
bash Anaconda3-2023.09-0-Linux-x86_64.sh
source ~/.profile
```

Clone the project and set the environment

```sh
git clone https://github.com/Simula-COMPLEX/EpiTESTER.git
cd EpiTESTER
conda create -n epitester python=3.7
conda activate epitester
pip3 install -r requirements.txt
```

Configure the ADS under test (i.e., [Interfuser](https://github.com/opendilab/InterFuser))

> Download the pre-trained Interfuser [model](http://43.159.60.142/s/p2CN) and place it in the [leaderboard/team_code](https://github.com/Simula-COMPLEX/EpiTESTER/tree/main/leaderboard/team_code) folder.

```sh
## ads
cd interfuser
python setup.py develop
```

Configure the Simulator (i.e., [CARLA](https://carla.org/))

> Download and set CARLA 0.9.10

```sh
chmod +x setup_carla.sh
./setup_carla.sh
easy_install carla/PythonAPI/carla/dist/carla-0.9.10-py3.7-linux-x86_64.egg
```


# Scenario Generation

<div align=center><img src="https://github.com/Simula-COMPLEX/EpiTESTER/blob/main/assets/gene_expression_probabilities.png" width="960" /></div>

Clone the project and set the environment

```sh
cd epiga/alg
python strategy_epitester.py
```
