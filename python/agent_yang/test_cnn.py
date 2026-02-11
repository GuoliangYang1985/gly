import numpy as np
from nn.activators import Identity, Relu, ArcTan, Sigmoid
from nn.conv import Conv
from nn.net import Net


def init_test(activator, rate, order):
    a = np.array(
        [[[[0, 1, 1, 0, 2],
           [2, 2, 2, 2, 1],
           [1, 0, 0, 2, 0],
           [0, 1, 1, 0, 0],
           [1, 2, 0, 0, 2]],
          [[1, 0, 2, 2, 0],
           [0, 0, 0, 2, 0],
           [1, 2, 1, 2, 1],
           [1, 0, 0, 0, 0],
           [1, 2, 1, 1, 1]],
          [[2, 1, 2, 0, 0],
           [1, 0, 0, 1, 0],
           [0, 2, 1, 0, 1],
           [0, 1, 2, 2, 2],
           [2, 1, 0, 0, 1]]],

         [[[0, 1, 1, 0, 2],
           [2, 2, 2, 2, 1],
           [1, 0, 0, 2, 0],
           [0, 1, 1, 0, 0],
           [1, 2, 0, 0, 2]],
          [[1, 0, 2, 2, 0],
           [0, 0, 0, 2, 0],
           [1, 2, 1, 2, 1],
           [1, 0, 0, 0, 0],
           [1, 2, 1, 1, 1]],
          [[2, 1, 2, 0, 0],
           [1, 0, 0, 1, 0],
           [0, 2, 1, 0, 1],
           [0, 1, 2, 2, 2],
           [2, 1, 0, 0, 1]]],
         [[[0, 1, 1, 0, 2],
           [2, 2, 0, 2, 1],
           [1, 0, 0, 2, 0],
           [0, 1, 1, 1, 0],
           [1, 2, 0, 0, 2]],
          [[1, 0, 2, 0, 0],
           [0, 0, 0, 2, 0],
           [1, 2, 1, 2, 1],
           [1, 0, 1, 0, 0],
           [1, 2, 1, 1, 1]],
          [[2, 1, 2, 0, 0],
           [1, 0, 0, 1, 0],
           [0, 2, 1, 0, 1],
           [0, 1, 2, 0, 2],
           [2, 0, 1, 0, 1]]],
         [[[0, 1, 1, 0, 2],
           [2, 2, 0, 2, 1],
           [1, 0, 0, 2, 0],
           [0, 1, 1, 1, 0],
           [1, 2, 0, 0, 2]],
          [[1, 0, 2, 0, 0],
           [0, 0, 0, 2, 0],
           [1, 2, 1, 2, 1],
           [1, 0, 1, 0, 0],
           [1, 2, 1, 1, 1]],
          [[2, 1, 2, 0, 0],
           [1, 0, 0, 1, 0],
           [0, 2, 1, 0, 1],
           [0, 1, 2, 0, 2],
           [2, 0, 1, 0, 1]]]
         ])

    cl = Conv([3, 3, 2], [1, 1], 2, activator, rate, order)
    cl.init_net(a.shape)
    cl.filters.weights[0] = np.array(
        [[[-1, 1, 0],
          [0, 1, 0],
          [0, 1, 1]],
         [[-1, -1, 0],
          [0, 0, 0],
          [0, -1, 0]],
         [[0, 0, -1],
          [0, 1, 0],
          [1, -1, -1]]], dtype=np.float64)
    cl.filters.bias[0] = 1
    cl.filters.weights[1] = np.array(
        [[[1, 1, -1],
          [-1, -1, 1],
          [0, -1, 1]],
         [[0, 1, 0],
          [-1, 0, -1],
          [-1, 1, 0]],
         [[-1, 0, 0],
          [-1, 0, 1],
          [-1, 0, 0]]], dtype=np.float64)
    cl.filters.bias[1] = 0
    return a, cl


def gradient_check():
    """
    Check gradient of cnn.
    """
    # forward propagation.
    act = Relu  # Identity   # ArcTan
    a, cl = init_test(act, 0, [1])
    cl.forward(a)

    label = 0
    # get sensitivity map.
    sensitivity_array = Net.diff(cl.output, label)
    # calculate gradient through back propagation.
    cl.backward(sensitivity_array)
    # check gradient.
    epsilon = 10e-4
    e2 = epsilon * 2
    f = cl.filters
    wei = f.weights
    out, inp, h, w = wei.shape
    for t in range(out):
        for d in range(inp):
            for i in range(h):
                for j in range(w):
                    wei[t, d, i, j] += epsilon
                    cl.forward(a)
                    err1 = Net.loss(cl.output, label)
                    wei[t, d, i, j] -= e2
                    cl.forward(a)
                    err2 = Net.loss(cl.output, label)
                    expect_grad = (err1 - err2) / e2
                    wei[t, d, i, j] += epsilon
                    act = f.weights_grad[t, d, i, j]

                    p = t, d, i, j, expect_grad, act, expect_grad - act
                    print('weights(%d,%d,%d,%d): expected %f,actual:%f,diff:%.4e' % p)


if __name__ == '__main__':
    gradient_check()
