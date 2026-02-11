import numpy as np
from nn.activators import Sigmoid, ArcTan
from yang_net import YangNet
from nn.batch import Batch
from tools import Tools


def transpose(m, c, h, w, out_size, pos):
    # [0, pi/2]
    args0 = np.random.uniform(0, np.pi * 0.5, (m, c, h, w))
    total = c * h * w
    args1 = np.sin((np.sum(args0, (1, 2, 3)) / total)**2)
    return args0, get_label(args1, out_size, pos)


def get_label(args, out_size, pos):
    result = []
    count = len(args)
    n = out_size
    step = 1 / n
    begin = 0
    for i in range(count):
        for j in range(n):
            if args[i] < begin + (j + 1) * step:
                temp = np.zeros(n) + pos
                temp[j] = 1
                result.append(temp)
                break

    return np.array(result)


def train_and_evaluate():
    batch_size = 10  # 批处理大小
    num_classes = 4  # 输出大小
    chanel = 2  # 输入通道
    input_size_h = 5  # 输入宽
    input_size_w = 5  # 输入高
    test_count = 1000
    act = Sigmoid
    if act == ArcTan:
        pos = -1
    else:
        pos = 0
    train_data, train_labels = transpose(10000, chanel, input_size_h, input_size_w, num_classes, pos)
    test_data, test_labels = transpose(test_count, chanel, input_size_h, input_size_w, num_classes, pos)
    train_data = Tools.normalization(np.array(train_data))
    test_data = Tools.normalization(np.array(test_data))
    network = YangNet(2, 0.01, num_classes)

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
            los = network.loss(network.predict(batch_input), batch_labels)
            eva = Tools.predict_test(network, test_data, test_labels.shape, batch_size)
            error_ratio = Tools.evaluate(eva, test_labels)
            correct = (1 - error_ratio) * 100
            if correct > best:
                print('find better')
                best = correct
            p = Tools.now(), step, epoch, los, best, correct
            print('%s step:%d, epoch:%d, loss:%f, best:%.2f%%, correct:%.2f%%' % p)


if __name__ == '__main__':
    train_and_evaluate()
