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
