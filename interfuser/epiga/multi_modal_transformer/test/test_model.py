#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 27.08.2023 21:29
# @Author  : Chengjie
# @File    : test_model.py
# @Software: PyCharm
import unittest

import cv2
import numpy as np

from epiga.multi_modal_transformer.preprocess import Preprocess
from epiga.multi_modal_transformer.model import ImageCNN, LidarEncoder, Transfuser
import torch


class TestCNN(unittest.TestCase):
    def test_image_cnn(self):
        image_cnn = ImageCNN()
        print(image_cnn.features)

    def test_lidar_encoder(self):
        lidar_encoder = LidarEncoder()
        print(lidar_encoder._model)

    def test_transfuser(self):
        transfuser = Transfuser()
        # image = torchvision.io.read_image(path='../example_data/rgb/%04d.png').float()
        # bev = torchvision.io.read_image(
        #     path='../example_data/topdown/encoded_%04d.png').float()

        image = torch.tensor(cv2.imread('../example_data/rgb/%04d.png', cv2.IMREAD_COLOR))
        bev = torch.tensor(cv2.imread('../example_data/topdown/encoded_%04d.png', cv2.IMREAD_COLOR))

        image = image.repeat(16, 1, 1, 1)
        bev = bev.repeat(16, 1, 1, 1)

        print(image.shape, bev.shape)

        para_names = torch.LongTensor(np.repeat([[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]], 16, axis=0))

        print(para_names.shape)

        # print(image.shape)
        # print(bev.shape)
        fused_features = transfuser.forward(image, bev, para_names)
        # print(fused_features, fused_features.shape)

    def test_load_data(self):
        preprocess = Preprocess()
        image_, bev_, para_v_, min_dis_ = preprocess.get_image_bev(f_n='../dataset/new.csv')
        # image_ = torch.tensor(image_, dtype=torch.float)
        # bev_ = torch.tensor(bev_, dtype=torch.float)
        # para_v_ = torch.tensor(para_v_, dtype=torch.float)
        # min_dis_ = torch.tensor(min_dis_, dtype=torch.float)

        para_names = torch.LongTensor(np.repeat([[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]], 16, axis=0))

        transfuser = Transfuser()

        fused_features = transfuser.forward(image=image_, lidar=bev_, var_name=para_names, var_value=para_v_)
