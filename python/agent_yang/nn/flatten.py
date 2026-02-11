from nn.base import Base


class Flatten(Base):
    """
    Full connected layer of BP
    """

    def __init__(self, activator):
        """
        Constructor
        activator: The active function of this layer.
        """
        Base.__init__(self)
        self.activator = activator
        self.in_shape = None

    def forward(self, input_data):
        """
        The forward propagation of BP.
        input_data: The data of input that the size must equal input_size.
        """
        self.input = input_data
        self.in_shape = self.input.shape
        # Product of all elements after the second element.
        p = self.in_shape[1]
        rs = range(2, len(self.in_shape))
        for i in rs:
            p *= self.in_shape[i]

        self.output = input_data.reshape(self.in_shape[0], p)

    def backward(self, input_delta):
        """
        Calculate the gradient with Back Propagation.
        input_delta: Current layer input delta from down layer.
        """
        # restore dim.
        self.pre_gy = input_delta.reshape(self.in_shape)
