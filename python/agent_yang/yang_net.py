# -*- coding: UTF-8 -*-

from nn.activators import Sigmoid, Identity, Relu
from nn.conv import Conv
from nn.max_pool import MaxPool
from nn.mean_pool import MeanPool
from nn.full_connected import FullConnected
from nn.net import Net
from nn.flatten import Flatten


class YangNet(Net):
    """
    YangNet neural Net
    """

    def __init__(self, net, rate, out):
        """
        Constructor
        """
        Net.__init__(self)

        if net == 0:
            self.net0(2, out, rate)
        if net == 1:
            self.net1(out, rate)
        if net == 2:
            self.net2(out, rate)

    def net0(self, n, out, rate):
        print('cnn net0:', n)
        c1 = Conv([5, 5, n], [0, 0], 1, Relu, rate, [1])
        self.layers.append(c1)
        s1 = MaxPool([8, 8], 4)
        self.layers.append(s1)
        fl = Flatten(s1.activator)
        self.layers.append(fl)
        fc1 = FullConnected(25 * n, out, Sigmoid, 0.1, rate, [1])
        self.layers.append(fc1)

    def net1(self, out, rate):
        print('cnn net1')
        c1 = Conv([3, 3, 8], [0, 0], 1, Relu, rate, [1])
        self.layers.append(c1)
        s1 = MaxPool([2, 2], 2)
        self.layers.append(s1)
        c2 = Conv([3, 3, 4], [0, 0], 2, Relu, rate, [1])
        self.layers.append(c2)
        s2 = MaxPool([2, 2], 1)
        self.layers.append(s2)
        fl = Flatten(s1.activator)
        self.layers.append(fl)
        fc1 = FullConnected(100, 8, Sigmoid, 0.1, rate, [1])
        self.layers.append(fc1)
        fc2 = FullConnected(8, out, Sigmoid, 0.1, rate, [1])
        self.layers.append(fc2)

    def net2(self, out, rate):
        """
        Function test.
        """
        print('cnn net2')
        c1 = Conv([3, 3, 32], [0, 0], 1, Identity, rate, [1])
        self.layers.append(c1)
        s1 = MeanPool([2, 2], 1)
        self.layers.append(s1)
        fl = Flatten(s1.activator)
        self.layers.append(fl)
        fc1 = FullConnected(128, 128, Sigmoid, 0.1, rate, [1])
        self.layers.append(fc1)
        fc2 = FullConnected(128, 64, Sigmoid, 0.1, rate, [1])
        self.layers.append(fc2)
        fc3 = FullConnected(64, out, Sigmoid, 0.1, rate, [1])
        self.layers.append(fc3)

    def net3(self, n, out, rate):
        """
        On MNIST set if n=16 than success rate is 99.19%.
        """
        print('cnn net0:', n)
        c1 = Conv([5, 5, n], [0, 0], 1, Relu, rate, [1])
        self.layers.append(c1)
        s1 = MaxPool([8, 8], 4)
        self.layers.append(s1)
        fl = Flatten(s1.activator)
        self.layers.append(fl)
        fc1 = FullConnected(25 * n, 128, Sigmoid, 0.1, rate, [1])
        self.layers.append(fc1)
        fc2 = FullConnected(128, out, Sigmoid, 0.1, rate, [1])
        self.layers.append(fc2)
