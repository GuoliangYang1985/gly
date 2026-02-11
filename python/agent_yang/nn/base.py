class Base(object):
    """
    The base class of layer.
    """
    def __init__(self):
        # The input tensor of this layer.
        self.input = None
        # The output tensor of this layer.
        self.output = None
        # The activator of this layer.
        self.activator = None
        # The grad Y item of previous layer.
        self.pre_gy = None
