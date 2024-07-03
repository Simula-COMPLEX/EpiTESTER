#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 29.11.2023 16:43
# @Author  : Chengjie
# @File    : path_utils.py
# @Software: PyCharm

from pathlib import Path


def get_project_root():
    return Path(__file__).parent


print(get_project_root())
