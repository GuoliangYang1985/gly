import numpy as np
from nn.activators import Sigmoid, Identity, ArcTan
from nn.bp_net import BPNet
from nn.batch import Batch


def gradient_check(net, sample_feature, sample_label):
    """
    Check gradient of BP.
    :param net: Specify the network and verify whether it has been correctly implemented.
    :param sample_feature: The feature of sample.
    :param sample_label: The label of sample.
    :return:
    """
    m_net.predict(sample_feature)
    m_net.calc_gradient(sample_label)
    # check gradient.
    epsilon = 10e-4
    e2 = epsilon * 2
    for fc in net.layers:
        s = fc.w.shape
        for i in range(s[0]):
            for j in range(s[1]):
                w = fc.w
                # calculate gradient by define
                w[i, j] += epsilon
                output = net.predict(sample_feature)
                y1 = net.loss(sample_label, output)
                w[i, j] -= e2
                output = net.predict(sample_feature)
                y2 = net.loss(sample_label, output)
                expect_grad = (y1 - y2) / e2
                w[i, j] += epsilon

                p = i, j, expect_grad, fc.grad_w[i, j], expect_grad - fc.grad_w[i, j]
                print('weights(%d,%d): expected:%.4e, actual:%.4e, diff:%.4e' % p)


class Normalizer(object):
    def __init__(self):
        self.mask = [0x1, 0x2, 0x4, 0x8, 0x10, 0x20, 0x40, 0x80]

    def norm(self, number):
        data = [0.9 if number & m else 0.1 for m in self.mask]
        return np.array(data)


def get_train_data_set():
    normalizer = Normalizer()
    data_set = []
    labels = []
    for i in range(0, 256):
        n = normalizer.norm(i)
        data_set.append(n)
        labels.append(n)
    return labels, data_set


if __name__ == '__main__':
    m_labels, m_data_set = get_train_data_set()
    BPNet.set_loss_type('mse')
    m_net = BPNet([8, 9, 8], [Identity, ArcTan, Sigmoid], 0.1, 0, [[1], [1], [1], [1]])
    batch_input, batch_labels = Batch.next_batch(m_data_set, m_labels, 10)
    gradient_check(m_net, batch_input, batch_labels)
