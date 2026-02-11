import numpy as np
from nn.activators import Sigmoid, Identity, ArcTan
from nn.bp_net import BPNet
from nn.batch import Batch
from tools import Tools
from log import Log


def transpose(m, c, h, w, out_size, pos):
    args0 = np.random.uniform(0, np.pi * 0.5, (m, c, h, w))
    total = c * h * w
    args2 = args0 ** 2
    ave = np.sum(args2, (1, 2, 3)) / total
    args1 = np.sin(ave)
    return args0.reshape(m, total), get_label(args1, out_size, pos)


def get_label(args, out_size, pos):
    result = []
    count = len(args)
    n = out_size
    step = 1 / n
    begin = 0
    for i in range(count):
        for j in range(n):
            if args[i] < begin + (j + 1) * step:
                temp = np.zeros(n) + pos[0]
                temp[j] = pos[1]
                result.append(temp)
                break

    return np.array(result)


def train_and_evaluate(high, acts, num_classes, rate):
    batch_size = 10  # 批处理大小
    channel = 2  # 输入通道
    input_size_h = 5  # 输入宽
    input_size_w = 5  # 输入高
    act = acts[len(acts) - 1]
    if act is ArcTan:
        p2 = np.pi * 0.5
        pos = [-p2, p2]
    else:
        pos = [0, 1]
    train_data, train_labels = transpose(10000, channel, input_size_h, input_size_w, num_classes, pos)
    test_data, test_labels = transpose(1000, channel, input_size_h, input_size_w, num_classes, pos)
    train_data = Tools.normalization(train_data)
    test_data = Tools.normalization(test_data)

    network = BPNet([channel * input_size_h * input_size_w, 128, 64, num_classes], acts, 1, rate, high)

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
            los = network.loss(train_labels[-1], network.predict(train_data[-1]))
            eva = Tools.predict_test(network, test_data, test_labels.shape, batch_size)
            error_ratio = Tools.evaluate(eva, test_labels)
            correct = (1 - error_ratio) * 100
            if correct > best:
                print('find better')
                best = correct
            p = Tools.now(), step, epoch, los, best, correct
            str1 = '%s step:%d, epoch:%d, loss:%f, best:%.2f%%, correct:%.2f%%' % p
            print(str1)
            logger.debug(str1)


if __name__ == '__main__':
    m_high = [[1], [1, 2], [1, 2], [1]]
    # m_high = [[1], [1], [1], [1]]
    m_acts = [Identity, Sigmoid, Sigmoid, Sigmoid]
    m_num_classes = 4  # 输出大小
    m_rate = 0.1

    m_name = Log.save_name(m_high, m_acts, m_num_classes, m_rate)
    logger = Log.save(m_name)

    train_and_evaluate(m_high, m_acts, m_num_classes, m_rate)
