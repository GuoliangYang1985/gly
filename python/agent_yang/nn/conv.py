import numpy as np
from nn.filter import Filter
from nn.conv_util import ConvUtil
from nn.base import Base
from nn.high import High


class Conv(Base):
    def __init__(self, kernel, pad_size, stride, activator, rate, order):
        Base.__init__(self)
        # data(batch, in_channels, height, width)
        # weight: (out_channels, in_channels, height, width)
        # bias: (out_channels,)
        # out: (batch, out_channels, height, width)
        # filter_height, filter_width
        self.filter_size = np.array(kernel[0:2])
        self.out_channels = kernel[2]

        self.pad_size = np.array(pad_size)
        self.stride = stride
        self.rate = rate

        self.activator = activator
        self.padded_input = None
        self.e_sensitivity = None

        self.output = None
        self.u = None
        self.order = order
        self.step = int(self.out_channels / len(order))
        self.filters = None
        self.batch = 0
        # in_height, in_width
        self.in_size = None
        # out_height, out_width
        self.out_size = None
        self.hu = None

    def init_net(self, data):
        # data batch, in_channels, in_height, in_width
        if not self.batch == data[0]:
            self.batch = data[0]
            self.in_size = np.array(data[2:4])
            self.out_size = ConvUtil.output_size(self.in_size, self.filter_size, self.pad_size, self.stride)
            self.filters = Filter(self.out_channels, data[1], self.filter_size, self.rate)

    def forward(self, input_array):
        """
        Calculate out of the convolution layer that save to self.output
        """
        self.init_net(input_array.shape)
        self.input = input_array
        self.padded_input = ConvUtil.padding(input_array, self.pad_size)
        self.u = ConvUtil.cross_correlation(self.padded_input, self.filters, self.out_size, self.stride)
        self.hu = High.forward(self.u, self.order, self.step)
        self.output = self.activator.forward(self.hu)

    def backward(self, grad_y):
        """
        Calculate the error item passed to the previous layer and calculate the gradient for each weight.
        The error of the previous layer is stored in self.pre_delta
        The gradient is saved in the weights_grad of the Filter
        :param grad_y: The sensitivity map of this layer from down layer.
        :return: The active function of previous layer.
        """
        # Restore sensitivity map to stride equal 1.
        h_delta = grad_y * self.activator.backward(self.hu)
        delta = High.backward(h_delta, self.u, self.order, self.step)
        self.e_sensitivity = self.expand_sensitivity(delta)
        # W2=(W1-F+2P)/S+1 => P=(W2+F-1-W1)/2 W1=expanded_width W2=in_width F=filter_width
        zps = (self.in_size + self.filter_size - 1 - self.e_sensitivity.shape[2:4]) / 2
        padded_array = ConvUtil.padding(self.e_sensitivity, zps)
        fi = self.filters
        # Turn 180 degree of all filter weights.
        flipped_weights = np.array([np.rot90(i, 2) for i in fi.weights])
        # Calculate an array of error items corresponding to one filter.
        # The output of the previous layer as input of the partial derivative of the activation function.
        self.pre_gy = ConvUtil.back_cross_correlation1(padded_array, flipped_weights, self.in_size)
        # Set gradient of every Weight.
        out_size = fi.weights.shape[2:4]
        fi.weights_grad = ConvUtil.back_cross_correlation2(self.padded_input, self.e_sensitivity, out_size)
        # Set gradient of the bias.
        fi.bias_grad = np.sum(delta, axis=(0, 2, 3))
        # Update weights according to stochastic gradient descent.
        self.filters.update()

    def expand_sensitivity(self, sensitivity):
        """
        Expand sensitivity map with stride equal 1 and use zero fill interval.
        :param sensitivity: Original sensitivity.
        :return:
        """
        # W2=(W1-F+2P)/S+1 where S is 1.
        expanded_size = ConvUtil.output_size(self.in_size, self.filter_size, self.pad_size, 1)
        # create new sensitivity_map.
        ss = sensitivity.shape
        # expended sensitivity map size
        expand_array = np.zeros((ss[0], ss[1], expanded_size[0], expanded_size[1]))
        # Get error items from original sensitivity.
        rh = range(self.out_size[0])
        rw = range(self.out_size[1])
        for i in rh:
            for j in rw:
                expand_array[:, :, i * self.stride, j * self.stride] = sensitivity[:, :, i, j]
        return expand_array
