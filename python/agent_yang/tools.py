import numpy as np
from datetime import datetime


class Tools(object):
    @staticmethod
    def evaluate(labels, predict):
        labels1 = np.argmax(labels, 1)
        predicts1 = np.argmax(predict, 1)
        return np.sum(labels1 != predicts1) / len(labels)

    @staticmethod
    def normalization(input_x):
        f_put = np.array(input_x).flatten()
        max_in = max(f_put)
        min_in = min(f_put)
        return (input_x - min_in) / (max_in - min_in)

    @staticmethod
    def predict_test(network, test_data, shape, batch_size):
        count = shape[0]
        out_num = shape[1]
        temp = np.zeros((count, out_num))
        b = 0
        e = 0
        while e < count:
            e = min(count, b + batch_size)
            index = range(b, e)
            temp[index] = network.predict(test_data[index])
            b = e
        return temp

    @staticmethod
    def now():
        return datetime.now().strftime('%c')
