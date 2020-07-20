from ...modules.exceptions.exceptions import UnknownCommandException

class CommandManager:
'''
Just a simple CommandManager which creates a dictionary with all existing commands and compares the entries with incoming commands to execute the command or throw an exception if necessary.
'''

	def __init__(self):
		#self.cmdSize = cmdSize
		self.commands = {}

	def addCommand(self, key, command):
		#assert len(key) == self.cmdSize
		self.commands[key] = command

	def removeCommand(self, key):
		del self.commands[key]

	def execute(self, data):
		# Remove trailing line endings
		data = data.rstrip()
		data = data.split("#")
		# Get command string
		cmd = data[0]
		# Get parameters and split them
		params = data[1:]

		if cmd not in self.commands:
			raise UnknownCommandException(cmd)

		return str(self.commands[cmd].execute(params))
