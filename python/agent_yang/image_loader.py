from loader import Loader
import numpy as np


class ImageLoader(Loader):
    """
    The image loader of MNIST.
    """
    @staticmethod
    def get_picture(content, index):
        """
        Get image from MNIST data file.
        :param content: The MNIST's data.
        :param index: Current index of the image in content.
        :return:
        """
        start = index * 28 * 28 + 16
        picture = []
        for i in range(28):
            picture.append([])
            for j in range(28):
                picture[i].append(content[start + i * 28 + j])

        picture = np.array(picture, dtype='uint8')
        # import cv2
        # cv2.imshow('11', picture)
        # cv2.waitKey(0)
        return picture

    def load(self):
        """
        Load  images tensor.
        """
        content = self.get_file_content()
        data_set = []
        for index in range(self.count):
            data_set.append(self.get_picture(content, index))
        return data_set
