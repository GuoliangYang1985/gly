# -*- coding: UTF-8 -*-
import numpy as np


class Relu(object):
    @staticmethod
    def forward(weighted_input):
        return np.maximum(0, weighted_input)

    @staticmethod
    def backward(x):
        x = np.maximum(0, x)
        x[x > 0] = 1
        return x


class ArcTan(object):
    @staticmethod
    def forward(weighted_input):
        return np.arctan(weighted_input)

    @staticmethod
    def backward(x):
        return 1.0 / (1.0 + x ** 2)


class Identity(object):
    @staticmethod
    def forward(weighted_input):
        return weighted_input

    @staticmethod
    def backward(x):
        return 1


class Sigmoid(object):
    @staticmethod
    def forward(weighted_input):
        return 1.0 / (1.0 + np.exp(-weighted_input))

    @staticmethod
    def backward(x):
        y = Sigmoid.forward(x)
        return y * (1 - y)


class Tanh(object):
    @staticmethod
    def forward(weighted_input):
        return 2.0 / (1.0 + np.exp(-2 * weighted_input)) - 1.0

    @staticmethod
    def backward(x):
        y = Tanh.forward(x)
        return 1.0 - y * y
