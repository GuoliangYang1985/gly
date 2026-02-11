import numpy as np


class High:
    """
    Function of the higher power of the output value.
    """

    @staticmethod
    def forward(u, ps, step):
        """
        Forward process.
        :param u: The processing of input, weight and bias terms.
        :param ps: The power tensor of the output.
        :param step: The step size in each case.
        :return: The p power of the output value.
        """
        c = len(ps)
        if c == 1 and ps[0] == 1:
            # No action is required when there is only one time.
            return u
        # Reserved for higher-order function implementation here.

    @staticmethod
    def backward(h_delta, u, ps, step):
        """
        Backward process.
        :param h_delta: The error items.
        :param u: The processing of input, weight and bias terms.
        :param ps: The power tensor of the output.
        :param step: The step size in each case.
        :return: Derivative of the p power of the output value.
        """
        c = len(ps)
        if c == 1 and ps[0] == 1:
            # No action is required when there is only one time.
            return h_delta
        # Reserved for higher-order function implementation here.
