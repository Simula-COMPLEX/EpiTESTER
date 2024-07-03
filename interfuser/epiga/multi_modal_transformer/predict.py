#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 14/11/2023 18:06
# @Author  : Chengjie
# @File    : predict.py
# @Software: PyCharm


import cv2
import numpy as np
import torch
from torch import nn

from epiga.multi_modal_transformer.preprocess import Preprocess
from model import Transfuser

from path_utils import get_project_root

PATH = get_project_root()


class EpigenesisGeneration:
    def __init__(self, model_path):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.PATH = PATH

        self.model_path = model_path
        self.model = Transfuser()
        self.model.to(self.device)
        self.model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
        self.model.eval()

    def state_encoding(self, i_path, b_path):
        image = []
        bev = []
        for s in range(4):
            i_path = 's{}_rgb.png'.format(s + 1)
            b_path = 's4_bev.png'.format(s + 1)

            image_i = cv2.imread('{}/epiga/multi_modal_transformer/dataset/states/{}'.format(self.PATH, i_path),
                                 cv2.IMREAD_COLOR)
            bev_i = cv2.imread('{}/epiga/multi_modal_transformer/dataset/states/{}'.format(self.PATH, b_path),
                               cv2.IMREAD_UNCHANGED)
            bev_i = cv2.cvtColor(bev_i, cv2.COLOR_BGR2RGB)

            # image = np.moveaxis(image, -1, 0)
            # bev = np.moveaxis(bev, -1, 0)
            image.append(np.moveaxis(image_i, -1, 0))
            bev.append(np.moveaxis(bev_i, -1, 0))

        return torch.tensor(np.array(image), dtype=torch.float).to(device=self.device), torch.tensor(np.array(bev),
                                                                                                     dtype=torch.float).to(
            device=self.device)

    def eval(self, dataset='dataset4_2000.csv'):
        mse_fn = nn.MSELoss()

        loss_fn = torch.nn.HuberLoss(reduction='mean', delta=1.0)

        preprocess = Preprocess(PATH=PATH)
        dataloader_train = preprocess.data_loader(
            f_n='{}/epiga/multi_modal_transformer/dataset/{}'.format(PATH, dataset), batch_size=64,
            device=self.device)

        mse_list = []
        loss_list = []
        for step, (batch_image, batch_bev, batch_para_v, batch_para_n, batch_y) in enumerate(dataloader_train):
            # print(batch_image)

            y_pred = self.model(batch_image, batch_bev, batch_para_n, batch_para_v)
            mse = mse_fn(y_pred, batch_y)

            loss = loss_fn(y_pred, batch_y)

            mse_list.append(mse.item())
            loss_list.append(loss.item())
            # print(mse)

        print(sum(mse_list) / len(mse_list))

        print(sum(loss_list) / len(loss_list))


def gs_probability_generation(model_path, i_path, b_path):
    eg = EpigenesisGeneration(model_path=model_path)
    state_i, state_b = eg.state_encoding(i_path=i_path, b_path=b_path)
    para_n = torch.LongTensor(np.repeat([[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]], len(state_i), axis=0)).to(
        device=eg.device)
    para_v = torch.rand((len(state_i), 10), dtype=torch.float).to(device=eg.device)

    eg.model(state_i, state_b, para_n, para_v)
    att_weights = eg.model.attn.weights
    gs_probability_dict = {}
    for i in range(4):
        scenario_id = 'scenario_{}'.format(i + 1)
        gs_probability_dict.update({scenario_id: [round(w, 4) for w in att_weights[i][0].tolist()]})

    print(gs_probability_dict)
    return gs_probability_dict


if __name__ == '__main__':
    gs_probability_generation(model_path='./models/epigenetic_model.pth', i_path='s4_rgb.png', b_path='s4_bev.png')