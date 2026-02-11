from nn.activators import Sigmoid, Identity, ArcTan
import logging


class Log(object):
    @staticmethod
    def save_name(high, acts, num_classes, rate):
        str_h = ''
        for ha in high:
            str_h += str(max(ha))

        str_a = ''
        for a in acts:
            if a is Sigmoid:
                str_a += 's'
            elif a is ArcTan:
                str_a += 'a'
            else:
                str_a += 'i'
        name = str_a + '_' + str_h + '_' + str(num_classes) + '_' + str(rate) + '.log'
        return name

    @staticmethod
    def save(m_name):
        logging.basicConfig(filename=m_name, format='%(asctime)s %(message)s', filemode='w')
        # Let us Create an object
        logger = logging.getLogger()
        # Now we are going to Set the threshold of logger to DEBUG
        logger.setLevel(logging.DEBUG)
        return logger
