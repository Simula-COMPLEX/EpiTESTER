#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 19.10.2023 16:06
# @Author  : Chengjie
# @File    : test.py
# @Software: PyCharm

def calculate_solution(solution):
    lower_bounds_real = [-20, -20, 0, -10, -10, -1, -1, 0.94, -90, 0]
    upper_bounds_real = [20, 20, 0.3, 10, 10, 1, 1, 1.43, 90, 100]

    solution_norm = []
    for i in range(len(solution)):
        solution_norm.append(
            (solution[i] - lower_bounds_real[i]) / (upper_bounds_real[i] - lower_bounds_real[i]))
    return solution_norm


s = [15.420495475595438, -16.361891267159862, 0.1926758163599495, -2.16655040529149, 0.500784270446978, -1,
     0.43129383377230845, 1.0387382107751084, 53.160895710406635, 67.38204760609793
     ]

print(calculate_solution(solution=s))
