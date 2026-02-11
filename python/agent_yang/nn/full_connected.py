import numpy as np
from nn.base import Base
from nn.high import High


class FullConnected(Base):
    """
    High-order fully connected layer of BP neural network.
    """

    def __init__(self, input_size, output_size, activator, r, rate, ps):
        """
        Constructor
        :param input_size: The input size of this layer same with previous out size.
        :param output_size: The out put size of this layer.
        :param activator: The active function of this layer.
        :param r: The boundary of the weighted random number is r, and the weight value is between [-r,r].
        :param rate: Learning step during training.
        :param ps: The power tensor of the output.
        """
        Base.__init__(self)
        self.input_size = input_size
        self.step = int(output_size / len(ps))
        self.output_size = output_size
        self.activator = activator
        # The matrix of weights in this layer.
        self.w = np.random.uniform(-r, r, (input_size, output_size))
        self.b = np.random.uniform(-r, r, (1, output_size))

        # The gradient of all weight.
        self.grad_w = None
        # The gradient of all bias.
        self.grad_b = None

        # The power tensor of the output.
        self.ps = ps
        self.u = None
        self.hu = None
        self.rate = rate

    def forward(self, x):
        """
        The forward propagation of BP.
        x: The data of input that the size must equal input_size.
        """
        # formula 2
        self.input = x
        # U=X W+b               【1】
        self.u = np.dot(self.input, self.w) + self.b
        # HU=h(U)=U^P           【2】
        self.hu = High.forward(self.u, self.ps, self.step)
        # Y=f(HU)               【3】
        self.output = self.activator.forward(self.hu)

    def backward(self, grad_y):
        """
        Calculate the gradient with Back Propagation. grad_y is gradient of y, and  multiply f'(HU) is HDelta.
        from HDelta will to Delta.
        '_1' indicates the previous layer. 'H' indicates high.
        HDelta=dE/dHU           【4】
        grad_y: Current layer input DE/DY from down layer.
        """
        # HD=dE/d[HU]
        # =dE/dY dY/DHU
        # =GY f'(HU)
        h_delta = grad_y * self.activator.backward(self.hu)

        # HDelta to Delta.
        # Delta=dE/dU
        # =dE/dHU dHU/dU
        # =HDelta PU^{P-1}      【5】
        delta = High.backward(h_delta, self.u, self.ps, self.step)

        # GY_1=dE/DY_1
        # =dE/dU dU/DY_1
        # =Delta W
        # From pre_gy to previous HDelta is Delta W f'_(HU_1)
        self.pre_gy = np.dot(delta, self.w.T)

        # GW=dE/dW
        # =dE/dU dU/dW
        # =delta X
        # =X delta              【6】
        self.grad_w = np.dot(self.input.T, delta)
        # self.b_grad = np.dot(np.ones(self.input.shape[0]).T, input_delta)
        # GBl=dE/dB
        # =dE/dU dU/dB
        # =delta                【7】
        # self.grad_b = np.dot(np.ones(self.input.shape[0]).T, delta)
        self.grad_b = np.sum(delta, axis=0)

        self.w -= self.rate * self.grad_w
        self.b -= self.rate * self.grad_b

    def dump(self):
        """
        print W and b information.
        :return:
        """
        print('w: %s\nb:%s' % (self.w, self.b))
