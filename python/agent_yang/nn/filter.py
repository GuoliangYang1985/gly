import numpy as np


class Filter(object):
    def __init__(self, out_channels, in_channels, size, rate):
        r = 0.1
        self.num_filter = out_channels
        # out_channels, in_channels, height, width
        self.weights = np.random.uniform(-r, r, (out_channels, in_channels, size[0], size[1]))
        self.bias = np.random.uniform(-r, r, out_channels)
        self.weights_grad = None
        self.bias_grad = None
        self.rate = rate

    def update(self):
        self.weights -= self.rate * self.weights_grad
        self.bias -= self.rate * self.bias_grad

    def __repr__(self):
        return 'filter weights:\n%s\nbias:\n%s' % (
            repr(self.weights), repr(self.bias))
