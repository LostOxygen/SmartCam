class UnknownCommandException(Exception):

	def __init__(self, cmd):
		super().__init__()
		self.message = str(cmd) + " is no valid command"

class WrongNumberOfParametersException(Exception):

	def __init__(self, given, expected):
		super().__init__()
		self.message = str(given) + " parameters were given, " \
			+ str(expected) + " were expected"

class InvalidParametersException(Exception):

	def __init__(self, given):
		super().__init__()
		self.message = str(given) + " are no valid parameters"

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
