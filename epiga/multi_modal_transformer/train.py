#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 12/09/2023 11:14
# @Author  : Chengjie
# @File    : train.py
# @Software: PyCharm
import argparse
import os

import torch
from torch import optim

from preprocess import Preprocess
from model import Transfuser

PATH = get_project_root()


class TrainingEngine:
    """
    Training Engine
    """

    def __init__(self, model, optimizer, dataloader_train, dataloader_val):
        self.model = model
        self.optimizer = optimizer
        self.dataloader_train = dataloader_train
        self.dataloader_val = dataloader_val

    def train(self, epoch_n, log_n):
        print('start training ...')
        f = open('{}/epiga/multi_modal_transformer/{}.txt'.format(PATH, log_n), mode='w', encoding='utf-8')
        # f_2 = open('{}/epiga/multi_modal_transformer/logs_f_batch_4_64_2.txt'.format(PATH), mode='w', encoding='utf-8')

        loss_fn = torch.nn.HuberLoss(reduction='mean', delta=1.0)
        for epoch in range(epoch_n):
            loss_ = []
            for step, (batch_image, batch_bev, batch_para_v, batch_para_n, batch_y) in enumerate(self.dataloader_train):
                # print(batch_image)

                y_pred = self.model(batch_image, batch_bev,  batch_para_n, batch_para_v)
                loss = loss_fn(y_pred, batch_y)

                loss_.append(loss.item())
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()

                # print(loss)
                # f_2 = open('{}/epiga/multi_modal_transformer/logs_f_batch_4_64_2.txt'.format(PATH), mode='a',
                #            encoding='utf-8')
                # f_2.writelines(str(loss.item()) + '\n')
                # f_2.close()

            if (epoch + 1) % 2 == 0:
                print(epoch, sum(loss_) / len(loss_))
                f = open('{}/epiga/multi_modal_transformer/{}.txt'.format(PATH, log_n), mode='a', encoding='utf-8')
                f.writelines(str('{}: {}\n'.format(epoch, sum(loss_) / len(loss_))))
                f.close()

            if epoch == 10000:
                self.save_model(model_path='model_{}_epoch_{}.pth'.format(log_n, epoch))

    def save_model(self, model_path):
        path = '{}/epiga/multi_modal_transformer/models/'.format(PATH)
        if not os.path.exists(path):
            os.makedirs(path)
        torch.save(self.model.state_dict(), path + model_path)


def main(args):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print('Device: {}'.format(device))
    # print('Current used device: {}'.format(torch.cuda.get_device_name(0)))

    preprocess = Preprocess(PATH=PATH)
    dataloader_train = preprocess.data_loader(f_n='{}/epiga/multi_modal_transformer/dataset/{}'.format(PATH, args.file_name), batch_size=args.batch, device=device)
    model = Transfuser()
    model.to(device=device)
    optimizer = optim.AdamW(model.parameters(), lr=args.learning_rate)

    engine = TrainingEngine(model=model, optimizer=optimizer, dataloader_train=dataloader_train, dataloader_val=dataloader_train)
    engine.train(20000, log_n='log_{}_{}_{}_{}_{}'.format(args.learning_rate, args.batch, args.file_name, args.run, args.tag))
    engine.save_model(model_path='model_{}_{}_{}_{}_{}.pth'.format(args.learning_rate, args.batch, args.file_name, args.run, args.tag))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='model training', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--file_name', default='dataset4_1500.csv',
                        help='dataset used for training')
    parser.add_argument('--learning_rate', type=float, default=1e-4,
                        help='dataset used for training')
    parser.add_argument('--batch', type=int, default=4,
                        help='dataset used for training')
    parser.add_argument('--run', type=int, default=1,
                        help='run')
    parser.add_argument('--tag', default='model5_3',
                        help='transformer layers')
    # parser.add_argument('--model', default='model_4_64_2',
    #                     help='dataset used for training')

    arguments = parser.parse_args()
    print('learning rate: {}'.format(arguments.learning_rate))
    print('batch size: {}'.format(arguments.batch))
    main(arguments)
