# -*- coding: UTF-8 -*-
import numpy as np


class Net(object):
    """
    YangNet neural Net
    """
    loss_type = "default"

    def __init__(self):
        """
        Constructor
        layer: All layers of net.
        """
        self.layers = []

    @staticmethod
    def set_loss_type(loss_type:str):
        Net.loss_type = loss_type

    def predict(self, sample):
        """
        Get predict result from network.
        sample: The data to be predicted.
        """
        output = sample
        for layer in self.layers:
            layer.forward(output)
            output = layer.output
        return output

    def train(self, data_set, labels):
        """
        Train the net.
        data_set: the data set of sample.
        labels: labels of sample.
        """
        self.predict(data_set)
        self.calc_gradient(labels)

    def calc_gradient(self, label):
        layer = self.layers[-1]
        grad_y = Net.diff(layer.output, label)
        for layer in self.layers[::-1]:
            layer.backward(grad_y)
            grad_y = layer.pre_gy

    def dump(self):
        for layer in self.layers:
            layer.dump()

    @staticmethod
    def diff(o, t):
        """
        if use o - t then update W and B with '-'.
        if use t - o then update W and B with '+'.
        :param o: Out of net.
        :param t: target labels.
        :return: The difference between a and b.
        """
        if Net.loss_type == 'mse':
            return Net.mse_back(o, t)
        else:
            return o - t

    @staticmethod
    def loss(output, label):
        if Net.loss_type == 'mse':
            return Net.mse(output, label)
        else:
            diff = -Net.diff(output, label)
            return 0.5 * np.sum(diff * diff)

    @staticmethod
    def mse_back(o, t):
        return 2 * (o - t) / t.size

    @staticmethod
    def mse(output, label):
        return np.sum(np.square(output - label)) / label.size
