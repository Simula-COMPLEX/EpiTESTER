#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 10/09/2023 16:15
# @Author  : Chengjie
# @File    : preprocess.py
# @Software: PyCharm
import cv2
import pandas as pd
import torchvision
import torch
import numpy as np
import torch.utils.data as Data

from path_utils import get_project_root

PATH = get_project_root()


# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# print('Device: {}'.format(device))


class Preprocess:
    def __init__(self, PATH):
        self.PATH = PATH

    @staticmethod
    def preprocess_csv(f_n, scenario_n):
        data = pd.read_csv(filepath_or_buffer=f_n, sep=',')
        data['state_image'] = data['npc_vertical']
        data['state_bev'] = data['npc_vertical']

        # print(data.loc[1, 'npc_vertical'])

        for i in range(len(data)):
            data.loc[i, 'state_image'] = '{}_rgb'.format(scenario_n)
            data.loc[i, 'state_bev'] = '{}_bev'.format(scenario_n)

        data = data[
            ['state_image', 'state_bev', 'npc_vertical', 'npc_horizontal', 'npc_behavior',
             'pedestrian_vertical', 'pedestrian_horizontal', 'pedestrian_direction_x',
             'pedestrian_direction_y', 'pedestrian_speed', 'weather_sun_angle', 'weather_fog_density', 'min_dis']]

        data.to_csv(f_n, mode='w', index=True, header=True)

    @staticmethod
    def drop_rows(f_n, new_f_n):
        data = pd.read_csv(filepath_or_buffer=f_n, sep=',', index_col=0)

        drop = []
        for i in range(len(data)):
            print(data['min_dis'][i])
            if float(data['min_dis'][i]) > 5:
                drop.append(i)
        # print(drop)
        data = data.drop(np.array(drop).astype(int), axis=0).reset_index(drop=True)
        # data = data.reset_index(drop=True, inplace=True)

        data.to_csv(new_f_n, mode='w', index=False, header=True)

    @staticmethod
    def merge_files(file_list, save_f):
        df = pd.concat(map(pd.read_csv, file_list), ignore_index=True)
        print(len(df))
        df.to_csv(save_f, mode='w', index=False, header=True)

    # @staticmethod
    def get_image_bev(self, f_n, device):
        data = pd.read_csv(filepath_or_buffer=f_n, sep=',')  # , nrows=4
        data = data.sample(frac=1).head(2000).reset_index(drop=True)
        # data = data.sample(frac=1).reset_index(drop=True)
        # print(data.head(10000).reset_index(drop=True))

        print('training dataset size: {}'.format(len(data)))

        image = []
        bev = []

        para_v = data[['npc_vertical', 'npc_horizontal', 'npc_behavior',
                       'pedestrian_vertical', 'pedestrian_horizontal', 'pedestrian_direction_x',
                       'pedestrian_direction_y', 'pedestrian_speed', 'weather_sun_angle',
                       'weather_fog_density']].values
        min_dis = data[['min_dis']].values

        # print(len(para_v))
        for i in range(len(data)):
            i_path = data.loc[i, 'state_image'] + '.png'
            b_path = data.loc[i, 'state_bev'] + '.png'

            # print(i_path, b_path)
            images_i = cv2.imread('{}/epiga/multi_modal_transformer/dataset/states/{}'.format(self.PATH, i_path),
                                  cv2.IMREAD_COLOR)
            # images_i = scale_image_cv2(cv2.cvtColor(images_i, cv2.COLOR_BGR2RGB), 1)

            bev_i = cv2.imread('{}/epiga/multi_modal_transformer/dataset/states/{}'.format(self.PATH, b_path),
                               cv2.IMREAD_UNCHANGED)
            bev_i = cv2.cvtColor(bev_i, cv2.COLOR_BGR2RGB)

            image.append(np.moveaxis(images_i, -1, 0))
            bev.append(np.moveaxis(bev_i, -1, 0))
        # print(torch.tensor(data['state_image'][0]))
        # data.to_csv('./new2.csv', mode='w', index=False, header=True)
        return torch.tensor(np.array(image), dtype=torch.float).to(device=device), torch.tensor(np.array(bev),
                                                                                                dtype=torch.float).to(
            device=device), \
               torch.tensor(np.array(para_v), dtype=torch.float).to(device=device), torch.tensor(np.array(min_dis),
                                                                                                 dtype=torch.float).to(
            device=device)

    @staticmethod
    def read_csv(f_n):
        data = pd.read_csv(filepath_or_buffer=f_n, sep=',')
        state_image = data[['state_image']]
        state_bev = data[['state_bev']]
        para_v = data[['npc_vertical', 'npc_horizontal', 'npc_behavior',
                       'pedestrian_vertical', 'pedestrian_horizontal', 'pedestrian_direction_x',
                       'pedestrian_direction_y', 'pedestrian_speed', 'weather_sun_angle', 'weather_fog_density']]
        min_dis = data[['min_dis']]

        print(torch.tensor(np.array(state_image.values[0], dtype=np.float)))
        # print(state_bev.values[0])
        # print(para_v.values)

    def data_loader(self, f_n, batch_size=10, device='cpu'):
        image, bev, para_v, min_dis = self.get_image_bev(f_n=f_n, device=device)
        para_n = torch.LongTensor(np.repeat([[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]], len(image), axis=0)).to(device=device)
        torch_dataset = Data.TensorDataset(image, bev, para_v, para_n, min_dis)
        loader = Data.DataLoader(
            dataset=torch_dataset,
            batch_size=batch_size,
            shuffle=True,
            num_workers=0
        )

        # for step, (batch_image, batch_bev, batch_para_v, batch_para_n, batch_y) in enumerate(loader):
        #     print(batch_image)
        return loader


def scale_image_cv2(image, scale):
    (width, height) = (int(image.shape[1] // scale), int(image.shape[0] // scale))
    im_resized = cv2.resize(image, (width, height))
    return im_resized
