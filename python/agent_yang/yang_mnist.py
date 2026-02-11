# -*- coding: UTF-8 -*-
import numpy as np
from image_loader import ImageLoader
from label_loader import LabelLoader
from nn.activators import Sigmoid, Relu, ArcTan
from yang_net import YangNet
from nn.bp_net import BPNet
from nn.batch import Batch
from tools import Tools


def get_training_data_set(bound):
    """
    Get the train data set.
    """
    image_loader = ImageLoader('data/train-images.idx3-ubyte', 60000)
    label_loader = LabelLoader('data/train-labels.idx1-ubyte', 60000)
    return image_loader.load(), label_loader.load(bound)


def get_test_data_set(bound):
    """
    Get the test data set.
    """
    image_loader = ImageLoader('data/t10k-images.idx3-ubyte', 10000)
    label_loader = LabelLoader('data/t10k-labels.idx1-ubyte', 10000)
    return image_loader.load(), label_loader.load(bound)


def transpose(args, use_bp):
    if use_bp:
        args0 = [np.array(line).flatten() for line in args[0]]
    else:
        args0 = [np.expand_dims(line, axis=0) for line in args[0]]
    args1 = [np.array(line) for line in args[1]]
    return np.array(args0), np.array(args1)


def train_and_evaluate(use_bp):
    batch_size = 10
    out_act = Sigmoid
    if out_act == ArcTan:
        r = 1  # high
        b = [-r, r]
    else:
        b = [0, 1]
    train_data, train_labels = transpose(get_training_data_set(b), use_bp)
    test_data, test_labels = transpose(get_test_data_set(b), use_bp)
    train_data = Tools.normalization(train_data)
    test_data = Tools.normalization(test_data)
    if use_bp:
        BPNet.set_loss_type('default')
        network = BPNet([784, 256, 128, 10], [out_act, Relu, Relu, out_act], 0.1, 0.1, [[1], [1], [1], [1]])
    else:
        network = YangNet(0, 0.01, 10)
    best = 0
    m = int(len(train_labels) / batch_size)
    epoch = 0
    step = 0
    while True:
        epoch += 1
        batch_input, batch_labels = Batch.next_batch(train_data, train_labels, batch_size)
        network.train(batch_input, batch_labels)
        if epoch % m == 0:
            step += 1
            tb_input, tb_labels = Batch.next_batch(test_data, test_labels, batch_size)
            los = network.loss(tb_labels, network.predict(tb_input))
            eva = Tools.predict_test(network, test_data, test_labels.shape, batch_size)
            error_ratio = Tools.evaluate(eva, test_labels)
            correct = (1 - error_ratio) * 100
            if correct > best:
                print('find better')
                best = correct
            p = Tools.now(), step, epoch, los, best, correct
            print('%s step:%d, epoch:%d, loss:%f, best:%.2f%%, correct:%.2f%%' % p)


if __name__ == '__main__':
    train_and_evaluate(True)
