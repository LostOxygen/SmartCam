import logging
import importlib

from ..exceptions.exceptions import WrongNumberOfParametersException, InvalidParametersException
from ..part_detection import detection
from ..cable_detection import cable
from ..circle_detection import circle
from .calibration import Calibration

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
		super().__init__(3)

	def _act(self, params):
		pass


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


class grabPoint(AbstractCommand):
	def __init__(self):
		super().__init__(0)

	def _act(self, params):
		logging.debug("Executing \"part_detection\" ")
		return detection.partDetection.detectParts()
