# EpiTESTER: Testing Autonomous Vehicles with Epigenetic Algorithm and Attention Mechanism

> This repository contains the replication package for the paper [EpiTESTER: Testing Autonomous Vehicles with Epigenetic Algorithm and Attention Mechanism](https://arxiv.org/abs/2312.00207).
> To facilitate reviewing our proposed approach, reviewers please refer to the corresponding data in this repository.
> This repository also contains the source code of our tool.<br/>

## Table of Contents
- [Abstract](#abstract)
- [Running Environment](#running-environment)
- [Scenario Generation](#scenario-generation)


## Abstract
Testing autonomous vehicles (AVs) under various environmental scenarios that lead the vehicles to unsafe situations is challenging. Given the infinite possible environmental scenarios, it is essential to find critical scenarios efficiently. To this end, we propose a novel testing method, named EpiTESTER, by taking inspiration from epigenetics, which enables species to adapt to sudden environmental changes. In particular, EpiTESTER adopts gene silencing as its epigenetic mechanism, which regulates gene expression to prevent the expression of a certain gene, and the probability of gene expression is dynamically computed as the environment changes. Given different data modalities (e.g., images, lidar point clouds) in the context of AV, EpiTESTER benefits from a multi-model fusion transformer to extract high-level feature representations from environmental factors. Next, it calculates probabilities based on these features with the attention mechanism. To assess the cost-effectiveness of EpiTESTER, we compare it with a probabilistic search algorithm (Simulated Annealing, SA), a classical genetic algorithm (GA) (i.e., without any epigenetic mechanism implemented), and EpiTESTER with equal probability for each gene. We evaluate EpiTESTER with six initial environments from CARLA, an open-source simulator for autonomous driving research, and two end-to-end AV controllers, Interfuser and TCP. Our results show that EpiTESTER achieved a promising performance in identifying critical scenarios compared to the baselines, showing that applying epigenetic mechanisms is a good option for solving practical problems.

<div align=center><img src="https://github.com/Simula-COMPLEX/EpiTESTER/blob/main/assets/overview.png" width="960" /></div>

## Test Interfuser


## Test TCP
