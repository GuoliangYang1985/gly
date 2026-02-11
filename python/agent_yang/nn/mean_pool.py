import numpy as np
from nn.conv_util import ConvUtil
from nn.activators import Identity
from nn.base import Base


class MeanPool(Base):
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
                self.output[:, :, i, j] = np.mean(patch, (2, 3))

    def backward(self, grad_y):
        h = self.filter[0]
        w = self.filter[1]
        area = h * w
        scale = 1 / area

        self.pre_gy = np.zeros(self.input.shape)
        for d in range(self.channel):
            for i in range(self.output_height):
                for j in range(self.output_width):
                    for p in range(self.batch_size):
                        i_s = i * self.stride
                        j_s = j * self.stride
                        self.pre_gy[p, d, i_s:i_s + h, j_s:j_s + w] = scale * grad_y[p, d, i, j]