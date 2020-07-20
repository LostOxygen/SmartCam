#!/usr/bin/python3

import sys
import logging
import signal
import argparse
from smartcam.core.configLoader import configReader

from smartcam.modules.exceptions.exceptions import UnknownCommandException, WrongNumberOfParametersException, InvalidParametersException
from smartcam.core.api.commandManager import CommandManager
from smartcam.core.api.server import Server
#import standard commands
from smartcam.core.api.commands import exitServer, calibrate, makeNormalImage, makeBackgroundImage, writeText

stop = False

'''
starts the server and registers all the imported modules as handlers for a command manager. uses the ip and port specified in the config.ini
'''

def main():
# Create CommandManager and register all handlers
	commandManager = CommandManager()
	commandManager.addCommand("IMG", makeNormalImage())
	commandManager.addCommand("BGD", makeBackgroundImage())
	commandManager.addCommand("CLB", calibrate())
	commandManager.addCommand("WRT", writeText())
	commandManager.addCommand("EXT", exitServer())

#check the modules and load specific handlers
	if configReader.returnEntry("modules", "circle"):
		from smartcam.core.api.commands import getCircleOffset
		commandManager.addCommand("GOO", getCircleOffset())

	if configReader.returnEntry("modules", "cable"):
		from smartcam.core.api.commands import getCableOffset
		commandManager.addCommand("GCO", getCableOffset())

	if configReader.returnEntry("modules", "parts"):
		from smartcam.core.api.commands import grabPoint
		commandManager.addCommand("GRP", grabPoint())

	if configReader.returnEntry("modules", "led"):
		from smartcam.core.api.commands import setLight
		commandManager.addCommand("LED", setLight())

	if configReader.returnEntry("modules", "iolink"):
		from smartcam.core.api.commands import moveGripper, closeGripper, openGripper
		commandManager.addCommand("MGR", moveGripper())
		commandManager.addCommand("OGR", openGripper())
		commandManager.addCommand("CGR", closeGripper())

	if configReader.returnEntry("modules", "schunk"):
		from smartcam.core.api.commands import schunkPrh
		commandManager.addCommand("PRH", schunkPrh())

	try:
		bind_ip = configReader.returnEntry("tcp", "host")
		port = int(configReader.returnEntry("tcp", "port"))
	except Exception as e:
		logging.error("could not load server ip and port from config file" + str(e))

	server = Server(bind_ip, port)
	logging.info(" ip: " + str(bind_ip) + " port: " + str(port))

	while not (server.isConnected() or stop):
		server.accept()

	# Listen to incomming messages
	while not stop:
		data = server.receive()
		if data is None:
			continue
		try:
			ans = commandManager.execute(data)
			if ans[0] == "E" and ans[1] == "X":
				global stop
				stop = True
			server.send(ans)
		except UnknownCommandException as e:
			logging.debug(e.message)
			server.send("EUNC")
		except WrongNumberOfParametersException as e:
			logging.debug(e.message)
			server.send("EINC")
		except InvalidParametersException as e:
			logging.debug(e.message)
			server.send("EINC")

	server.close()

def loadConfig():
	#loads the config
	from smartcam.core.configLoader import configReader
	configReader.loadConfig("/home/pi/.smartcam/config.ini")

def handler(signum, frame):
	global stop

	stop = True
	print("SIGINT received. Stopping programm.")

if __name__ == "__main__":
	parser = argparse.ArgumentParser()

	parser.add_argument("-p", "--port", help="port on which the server should run", type=int)
	parser.add_argument("-a", "--bind_address", help="address on which the server should bind")

	loggerMode = parser.add_mutually_exclusive_group(required=False)
	loggerMode.add_argument("-v", "--verbose", help="Prints info messages", action="store_true")
	loggerMode.add_argument("-q", "--quiet", help="Prints only error messages", action="store_true")
	parser.add_argument("--logfile", help="Logs will be written to this file")

	args = parser.parse_args()

	if args.verbose:
		logging.basicConfig(level=logging.DEBUG, filename=args.logfile)
	elif args.quiet:
		logging.basicConfig(level=logging.ERROR, filename=args.logfile)
	else:
		logging.basicConfig(level=logging.INFO, filename=args.logfile)

	# Register handler for SIGINT (Ctrl-C) interrupt
	signal.signal(signal.SIGINT, handler)

	loadConfig()
	main()
