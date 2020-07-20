import logging
import os
from ..configLoader import configReader

'''
The main commands class. To create a new command it's module needs to be loaded inside a try-catch block.
Then a new class which inherits the AbstractCommand class is created where the command call can be specified.

new Commands should match the following structure:

class <NewCommandName> (AbstractCommand):
	<short command description/documentation>

	def __init__(self):
		super().__init__( <NumberOfParameters> )

	def _act(self, params):
		try:
			<implement the command call here>
		except Exception as e:
			return "Error: " + str(e)
		return "ACK"

The classes will be imported while starting the server in 'server_start.py' in the root directory.
'''

try:
	from ...modules.schunk_module import iolink
except Exception as e:
	logging.error(" couldn't load module [iolink] .." + "\n" + str(e))
	configReader.updateConfig("modules", "iolink", "False")
try:
	from ...modules.schunk_module import led
except Exception as e:
	logging.error(" couldn't load module [led] .." + "\n" + str(e))
	configReader.updateConfig("modules", "led", "False" )
try:
	from ...modules.schunk_module import schunk_prh
except Exception as e:
	logging.error(" couldn't load module [schunk_prh] .." + "\n" + str(e))
	configReader.updateConfig("modules", "schunk", "False" )
try:
	from ...modules.exceptions.exceptions import WrongNumberOfParametersException, InvalidParametersException
except Exception as e:
	logging.error(" couldn't load module [exceptions] .." + "\n" + str(e))
try:
	from ...modules.part_detection.detection import partDetection
except Exception as e:
	logging.error(" couldn't load module [partDetection] .." + "\n" + str(e))
	configReader.updateConfig("modules", "parts", "False" )
try:
	from ...modules.cable_detection import cable
except Exception as e:
	logging.error(" couldn't load module [cable] .." + "\n" + str(e))
	configReader.updateConfig("modules", "cable", "False" )
try:
	from ...modules.circle_detection import circle
except Exception as e:
	logging.error(" couldn't load module [circle] .." + "\n" + str(e))
	configReader.updateConfig("modules", "circle", "False" )
try:
	from .calibration import calibration
except Exception as e:
	logging.error(" couldn't load module [calibration] .." + "\n" + str(e))


class AbstractCommand:
	def __init__(self, numParams):
		self.numParams = numParams

	def execute(self, params):
		if len(params) != self.numParams:
			 #raise WrongNumberOfParametersException(len(params), self.numParams)
			 logging.error("WrongNumberOfParametersException")

		return self._act(params)

	def _act(self, params):
		pass

class getCircleOffset(AbstractCommand):
	'''
	Returns the (X,Y) Offset to the nearest detected circle
	Usage: GOO
	Returns: (X,Y) as float
	'''
	def __init__(self):
		super().__init__(0)

	def _act(self, params):
		logging.debug("Executing \"circle_detection\" ")
		try:
			return circle.circleDetection.detectCircles()
		except Exception as e:
			return "Error: " + str(e)

class exitServer(AbstractCommand):
	'''
	Exits the connection between client and server and shuts both Down
	Usage: EXT
	Returns: EX as a String
	'''
	def __init__(self):
		super().__init__(0)

	def _act(self, params):
		return "EX"

class setLight(AbstractCommand):
	'''
	Sets the light to a specific Value
	Usage: LED#<value>, <value> should be a hex-Value
	Example: LED#FFFFFF to turn the LEDs black
	Returns: None
	'''
	def __init__(self):
		super().__init__(1)

	def _act(self, params):
		try:
			color = str(params[0])
			ledstrip = led.ledStrip()
			ledstrip.set_color(color)
		except Exception as e:
			return "Error: " + str(e)
		return "ACK"

class getCableOffset(AbstractCommand):
	'''
	Returns the offset between the cable and it's vertical baseline
	Usage:	GCO#<num>, where <num> is [1,2] to specify which image should be saved
	Example: GCO#2
	Returns: (X,Y) Offset as float
	'''
	def __init__(self):
		super().__init__(1)

	def _act(self, params):
		logging.debug("Executing \"cable_detection\" ")
		try:
			return cable.cableDetection.detectCable(params[0])
		except Exception as e:
			return "Error: " + str(e)

class calibrate(AbstractCommand):
	'''
	starts the calibration to calculate the scaling between pixels and milimetres
	Usage: CLB
	Returns: None
	'''
	def __init__(self):
		super().__init__(0)

	def _act(self, params):
		logging.debug("Executing \"calibration\" ")
		try:
			calibration.calibrate()
		except Exception as e:
			return "Error: " + str(e)
		return "ACK"

class makeNormalImage(AbstractCommand):
	'''
	Saves an raw image without any detection for debug purposes
	Usage: IMG
	Returns: None
	'''
	def __init__(self):
		super().__init__(0)

	def _act(self, params):
		logging.debug("Executing \"makeNormalImage\" ")
		try:
			calibration.makeNormalImage()
		except Exception as e:
			return "Error: " + str(e)
		return "ACK"

class makeBackgroundImage(AbstractCommand):
	'''
	Saves an raw image without any detection for background removal in cable detection process
	Usage: BGD
	Returns: None
	'''
	def __init__(self):
		super().__init__(0)

	def _act(self, params):
		logging.debug("Executing \"makeBackgroundImage\" ")
		try:
			calibration.makeNormalImage("background", False)
		except Exception as e:
			return "Error: " + str(e)
		return "ACK"

class grabPoint(AbstractCommand):
	'''
	returns the offset to grab the detected part and a rotation offset for the gripper
	Usage: GRP
	Returns: ((X,Y), (rot)) as float
	'''
	def __init__(self):
		super().__init__(0)

	def _act(self, params):
		logging.debug("Executing \"part_detection\" ")
		try:
			return detection.partDetection.detectParts()
		except Exception as e:
			return "Error: " + str(e)
		return "ACK"

class openGripper(AbstractCommand):
	'''
	opens the specified gripper
	Usage: OGR#<port>
	<port> is used to specify the gripper (use 1-4)
	Returns: None
	'''
	def __init__(self):
		super().__init__(1)

	def _act(self, params):
		try:
			params = list(map(int, params))
			if params[0] >= 1 and params[0] <= 4:
				gripper = iolink.Gripper(params[0])
				gripper.open()
			else:
				logger.error("Gripper parameters wrong (use 1-4)")
		except Exception as e:
			return "Error: " + str(e)
		return "ACK"

class closeGripper(AbstractCommand):
	'''
	opens the specified gripper
	Usage: CGR#<port>
	<port> is used to specify the gripper (use 1-4)
	Returns: None
	'''
	def __init__(self):
		super().__init__(1)

	def _act(self, params):
		try:
			params = list(map(int, params))
			if params[0] >= 1 and params[0] <= 4:
				gripper = iolink.Gripper(int(params[0]))
				gripper.close()
			else:
				logger.error("Gripper parameters wrong (use 1-4)")
		except Exception as e:
			return "Error: " + str(e)
		return "ACK"

class moveGripper(AbstractCommand):
	'''
	move the gripper about an specific value
	Usage: MGR#<port>#<val>
	<port> is used to specify the gripper (use 1-4)
	<val> is the value to move the gripper (positive=open, negative=close)
	Example: MGR#2#5
	Returns: None
	'''
	def __init__(self):
		super().__init__(2)

	def _act(self, params):
		try:
			params = list(map(int, params))
			if params[0] >= 1 and params[0] <= 4:
				gripper = iolink.Gripper(params[0])
				gripper.move_abs(params[1])
			else:
				logger.error("Gripper parameters wrong (use 1-4)")
		except Exception as e:
			return "Error: " + str(e)
		return "ACK"

class schunkPrh(AbstractCommand):
	'''	Schunk PRH Command
	Usage: PRH#<command>#<param>
	Commands: 	POS | Position Command, param1 = position
				PSS | Position Command with additional speed parameters, param1 = position, param2 = speed
				ACK | Acknowledge command, param = None
				HTL | Halt command, param = None
				REF | Ref Command, param = None

	Examples: PRH#POS#42, PRH#PSS#42#21
	'''
	def __init__(self):
		super().__init__(2)

	def _act(self, params):
		try:
			cmd = str(params[0]).lower()
			if cmd == "pos":
				params = list(map(int, params[1:]))
				schunk = schunk_prh.schunk_prh()
				schunk.pos(params[0])
				del schunk
			if cmd == "pss":
				params = list(map(int, params[1:]))
				schunk = schunk_prh.schunk_prh()
				schunk.pos(params[0], params[1])
				del schunk
			if cmd == "ack":
				schunk = schunk_prh.schunk_prh()
				schunk.ack()
				del schunk
			if cmd == "htl":
				schunk = schunk_prh.schunk_prh()
				schunk.halt()
				del schunk
			if cmd == "ref":
				schunk = schunk_prh.schunk_prh()
				schunk.ref()
				del schunk
		except Exception as e:
			return "Error: " + str(e)
		return "ACK"

class writeText(AbstractCommand):
	'''
	writes text on every test image on a specific Position
	Positions: UL: Up Left, UR: Up Right, DL: Down Left, DR: Down Right
	usage: WRT#<text>#<pos>
	example: WRT#test#DL
	'''
	def __init__(self):
		super().__init__(2)

	def _act(self, params):
		logging.debug("Executing \"write_text\" ")
		try:
			text = str(params[0])
			pos = str(params[1]).lower()
			calibration.writeText(text, pos)
		except Exception as e:
			return "Error: " + str(e)
		return "ACK"
