class Loader(object):
    """
    The base loader of MNIST
    """
    def __init__(self, path, count):
        """
         Init loader.
        :param path: The path of the MNIST.
        :param count: The count of loading MNIST.
        """
        self.path = path
        self.count = count

    def get_file_content(self):
        """
        Read the file content.
        """
        f = open(self.path, 'rb')
        content = f.read()
        f.close()
        return content
