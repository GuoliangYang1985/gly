import numpy as np


class Batch(object):
    @staticmethod
    def next_batch(data_set, labels, batch_size):
        """
        Randomly generate specified batch data.
        :param data_set: All input data.
        :param labels: All label data.
        :param batch_size: The size of the batch of data generated.
        :return: Generate a batch of data.
        """
        count = len(data_set)
        index = np.random.randint(count, size=batch_size)
        # index = [0, 1,2,3,4,5,6,7,8,9]
        data = []
        label = []
        for i in index:
            data.append(data_set[i])
            label.append(labels[i])
        return np.array(data), np.array(label)
