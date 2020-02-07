class NoContoursFoundException(Exception):

    def __init__(self, message):
        super().__init__()
        self.message = message


class NoInstanceException(Exception):

    def __init__(self, var, instance):
        super().__init__()
        self.message = str(var) + " is not an instance of " + str(instance)


class NoImageDataFoundException(Exception):

    def __init__(self, path):
        super().__init__()
        self.message = "could not load image data from " + str(path)
