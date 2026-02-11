import numpy as np


class ConvUtil(object):

    @staticmethod
    def get_patch(input_array, i, j, ws, stride):
        """
        Get region from input tensor.
        :param input_array: [batch, in_channels, in_height, in_width]
        :param i: each i in out_height
        :param j: each j in out_width
        :param ws: w_height, w_width
        :param stride: step
        :return: [batch, in_channels, w_height, w_width]
        """
        start_i = i * stride
        start_j = j * stride
        return input_array[:, :, start_i: start_i + ws[0], start_j: start_j + ws[1]]

    @staticmethod
    def cross_correlation(array, fi, size, stride):
        """
        [batch, in_channels, in_height, in_width] * [out_channels, in_channels, w_height, w_width]
        ->[batch, out_channels, out_height, out_width]
        :param array: padded input array [batch, in_channels, in_height, in_width]
        :param fi: weights[out_channels, in_channels, w_height, w_width], bias [out_channels]
        :param size: [out_height, out_width]
        :param stride: step
        :return: [batch, out_channels, out_height, out_width]
        """
        weights = fi.weights
        bias = fi.bias
        ws = weights.shape
        ins = array.shape
        h = size[0]
        w = size[1]

        # [out_channels, out_height, out_width, batch, in_channels, w_height, w_width]
        e_output = np.zeros((ws[0], h, w, ins[0], ins[1], ws[2], ws[3]))
        # [batch, out_height, out_width, out_channels, in_channels, w_height, w_width]
        e_weights = np.zeros((ins[0], h, w, ws[0], ws[1], ws[2], ws[3]))
        # [batch, out_height, out_width, out_channels]
        e_bias = np.zeros((ins[0], h, w, ws[0]))

        ConvUtil.expend_input(array, e_output, h, w, ws[2:4], stride)
        e_weights[:, :, :] = weights
        e_bias[:, :, :] = bias
        # sum(e_output turn to weight order)->[batch, out_height, out_width, out_channels]+e_bias
        temp = np.sum(e_output.transpose((3, 1, 2, 0, 4, 5, 6)) * e_weights, (4, 5, 6)) + e_bias
        # [batch, out_height, out_width, out_channels]->[batch, out_channels, out_height, out_width]
        return temp.transpose((0, 3, 1, 2))

    @staticmethod
    def back_cross_correlation1(array, weights, size):
        """
        [batch, out_channels, in_height, in_width] * [out_channels, in_channels, w_height, w_width]
        ->[batch, in_channels, in_height, in_width], in_channels and out_channels maybe not same.
        :param array: padded extend sensitivity [batch, out_channels, in_height, in_width]
        :param weights: flipped weights [out_channels, in_channels, w_height, w_width]
        :param size: [in_height, in_width]
        :return: [batch, in_channels, in_height, in_width]
        """
        ws = weights.shape
        ins = array.shape
        h = size[0]
        w = size[1]

        # [in_channels, in_height, in_width, batch, out_channels, w_height, w_width]
        e_output = np.zeros((ws[1], h, w, ins[0], ins[1], ws[2], ws[3]))
        # [batch, in_height, in_width, out_channels, in_channels, w_height, w_width]
        e_weights = np.zeros((ins[0], h, w, ws[0], ws[1], ws[2], ws[3]))

        ConvUtil.expend_input(array, e_output, h, w, ws[2:4], 1)
        e_weights[:, :, :] = weights
        # sum(e_output turn to weight order)->[batch, in_height, in_width, in_channels]
        temp = np.sum(e_output.transpose((3, 1, 2, 4, 0, 5, 6)) * e_weights, (3, 5, 6))
        # [batch, in_height, in_width, in_channels]->[batch, in_channels, in_height, in_width]
        return temp.transpose((0, 3, 1, 2))

    @staticmethod
    def back_cross_correlation2(array, weights, size):
        """
        [batch, in_channels, pin_height, pin_width] * [batch, out_channels, es_height, es_width]
        ->[out_channels, in_channels, w_height, w_width], in_channels and out_channels maybe not same.
        :param array: padded input array [batch, in_channels, pin_height, pin_width]
        :param weights: extend sensitivity [batch, out_channels, es_height, es_width]
        :param size: [w_height, w_width]
        :return: weights_grad [out_channels, in_channels, w_height, w_width]
        """
        ws = weights.shape
        ins = array.shape
        h = size[0]
        w = size[1]

        # [out_channels, w_height, w_width, batch, in_channels, es_height, es_width]
        e_output = np.zeros((ws[1], h, w, ins[0], ins[1], ws[2], ws[3]))
        # [in_channels, w_height, w_width, batch, out_channels, es_height, es_width]
        e_weights = np.zeros((ins[1], h, w, ws[0], ws[1], ws[2], ws[3]))

        ConvUtil.expend_input(array, e_output, h, w, ws[2:4], 1)
        e_weights[:, :, :] = weights
        # sum(e_output turn to weight order)->[in_channels, w_height, w_width, out_channels]
        temp = np.sum((e_output.transpose((4, 1, 2, 3, 0, 5, 6)) * e_weights), (3, 5, 6))
        # [in_channels, w_height, w_width, out_channels]->[out_channels, in_channels, w_height, w_width]
        return temp.transpose((3, 0, 1, 2))

    @staticmethod
    def expend_input(input_array, e_output, oh, ow, f, stride):
        """
        All convolutions to e_output array.
        :param input_array: input array
        :param e_output: extend output
        :param oh: out_height
        :param ow: out_width
        :param f: w_height, w_width
        :param stride: step
        """
        rh = range(oh)
        rw = range(ow)
        for i in rh:
            for j in rw:
                e_output[:, i, j] = ConvUtil.get_patch(input_array, i, j, f, stride)

    @staticmethod
    def padding(input_array, zero_pad):
        """
        Add zero padding to the array of 3D.
        input_array [batch, channels, height, width]
        """
        zs = zero_pad.astype(int)
        if zs[0] == 0 and zs[1] == 0:
            return input_array
        else:
            s = input_array.shape
            size = s[2:4]
            n_size = zs * 2 + size  # new_size = zero_size* 2 + size
            end = zs + size  # end = zero_size + size
            padded_array = np.zeros((s[0], s[1], n_size[0], n_size[1]))
            padded_array[:, :, zs[0]:end[0], zs[1]: end[1]] = input_array
            return padded_array

    @staticmethod
    def output_size(input_size, filter_size, zero_padding, stride):
        temp = (input_size - filter_size + 2 * zero_padding) / stride + 1
        return temp.astype(int)
