from .exceptions import UnknownCommandException

class CommandManager:

	def __init__(self, cmdSize):
		self.cmdSize = cmdSize
		self.commands = {}

	def addCommand(self, key, command):
		assert len(key) == self.cmdSize

		self.commands[key] = command

	def removeCommand(self, key):
		del self.commands[key]

	def execute(self, data):
		# Remove trailing line endings
		data = data.rstrip()
		# Get command string
		cmd = data[:self.cmdSize]
		# Get parameters and split them
		params = list(filter(None, data[self.cmdSize:].split(",")))

		if cmd not in self.commands:
			raise UnknownCommandException(cmd)

		return str(self.commands[cmd].execute(params))
