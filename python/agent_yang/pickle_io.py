import pickle


class PickleIO:
    """
    将数据或类型存储到磁盘，或从磁盘中读取文件。
    """

    @staticmethod
    def read(path):
        """
        读取用此类写入的文件。
        :param path: 文件路径。
        :return: 磁盘中的数据。
        """
        with open(path, 'rb') as file2:
            return pickle.load(file2)

    @staticmethod
    def write(path, data):
        """
        将数据固化到磁盘。
        :param path: 输出路径。
        :param data: 内存中的数据。
        """
        with open(path, 'wb') as file:
            pickle.dump(data, file)
