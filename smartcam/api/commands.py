import logging
import os

from ..schunk_module import iolink
from ..exceptions.exceptions import WrongNumberOfParametersException, InvalidParametersException
from ..part_detection import detection
from ..cable_detection import cable
from ..circle_detection import circle
from .calibration import calibration

'''
new Commands should match the following structure:

class <NewCommandName> (AbstractCommand):

	def __init__(self):
		super().__init__( <NumberOfParameters> )

	def _act(self, params):
		#implement the command call here
'''

class AbstractCommand:
	def __init__(self, numParams):
		self.numParams = numParams

	def execute(self, params):
		if len(params) != self.numParams:
			raise WrongNumberOfParametersException(len(params), self.numParams)

		return self._act(params)

	def _act(self, params):
		pass

class getCircleOffset(AbstractCommand):
	def __init__(self):
		super().__init__(0)

	def _act(self, params):
		logging.debug("Executing \"circle_detection\" ")
		return circle.circleDetection.detectCircles()

class exitServer(AbstractCommand):
	def __init__(self):
		super().__init__(0)

	def _act(self, params):
		return "EX"

class setLight(AbstractCommand):
	def __init__(self):
		super().__init__(6)

	def _act(self, params):
		color = str(params[:6])
		cmd = '../schunk_module/led.py ' + color
		os.system(cmd)

class makePicture(AbstractCommand):
	def __init__(self):
		super().__init__(0)

	def _act(self, params):
		pass

class getCableOffset(AbstractCommand):
	def __init__(self):
		super().__init__(0)

	def _act(self, params):
		logging.debug("Executing \"cable_detection\" ")
		return cable.cableDetection.detectCable()

class calibrate(AbstractCommand):
	def __init__(self):
		super().__init__(0)

	def _act(self, params):
		logging.debug("Executing \"calibration\" ")
		calibration.calibrate()

class makeNormalImage(AbstractCommand):
	def __init__(self):
		super().__init__(0)

	def _act(self, params):
		logging.debug("Executing \"makeNormalImage\" ")
		calibration.makeNormalImage()

class grabPoint(AbstractCommand):
	def __init__(self):
		super().__init__(0)

	def _act(self, params):
		logging.debug("Executing \"part_detection\" ")
		return detection.partDetection.detectParts()

class openGripper(AbstractCommand):
	def __init__(self):
		super().__init__(1)

	def _act(self, params):
		gripper = iolink.Gripper(params[0])
		gripper.open()

class closeGripper(AbstractCommand):
	def __init__(self):
		super().__init__(1)

	def _act(self, params):
		gripper = iolink.Gripper(params[0])
		gripper.close()

class moveGripper(AbstractCommand):
	def __init__(self):
		super().__init__(2)

	def _act(self, params):
		gripper = iolink.Gripper(params[0])
		gripper.move_abs(params[1])
