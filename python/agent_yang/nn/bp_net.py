# -*- coding: UTF-8 -*-

from nn.full_connected import FullConnected
from nn.net import Net


class BPNet(Net):
    def __init__(self, num, act, r, rate, order):
        """
        Init neural network.
        """
        Net.__init__(self)

        input_size = num[0]
        for i in range(len(num) - 1):
            layer = FullConnected(input_size, num[i + 1], act[i + 1], r, rate, order[i + 1])
            self.layers.append(layer)
            input_size = layer.output_size
