import numpy as np
from nn.conv_util import ConvUtil
from nn.activators import Identity
from nn.base import Base


class MaxPool(Base):
    def __init__(self, kernel_size, stride):
        Base.__init__(self)
        self.stride = stride
        self.filter = kernel_size

        self.activator = Identity

        self.learning_rate = 0
        self.batch_size = 0
        self.channel = 0
        self.output_height = 0
        self.output_width = 0

    def init_net(self, data):
        # data [batch, in_channels, in_height, in_width]
        # out [batch, num_filter, out_height, out_width]
        if not self.batch_size == data[0]:
            self.batch_size = data[0]
            self.channel = data[1]
            self.output_height = int((data[2] - self.filter[0]) / self.stride + 1)
            self.output_width = int((data[3] - self.filter[1]) / self.stride + 1)
            self.output = np.zeros((self.batch_size, self.channel, self.output_height, self.output_width))

    def forward(self, input_array):
        self.init_net(np.array(input_array.shape))
        self.input = input_array

        for i in range(self.output_height):
            for j in range(self.output_width):
                patch = ConvUtil.get_patch(input_array, i, j, self.filter, self.stride)
                self.output[:, :, i, j] = np.max(patch, (2, 3))

    def backward(self, grad_y):
        self.pre_gy = np.zeros(self.input.shape)
        for i in range(self.output_height):
            for j in range(self.output_width):
                patch = ConvUtil.get_patch(self.input, i, j, self.filter, self.stride)
                for p in range(self.batch_size):
                    for d in range(self.channel):
                        m, n = self.get_max_index(patch[p, d])
                        self.pre_gy[p, d, i * self.stride + m, j * self.stride + n] = grad_y[p, d, i, j]

    @staticmethod
    def get_max_index(array):
        """
        Get index of max value in 2D array.
        """
        pos = int(np.argmax(array))
        max_i, max_j = divmod(pos, array.shape[1])
        return max_i, max_j
