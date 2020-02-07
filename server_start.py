#!/usr/bin/python3

import sys
import logging
import signal
import argparse

stop = False

def main():
	from smartcam.configLoader import configReader
	from smartcam.exceptions.exceptions import UnknownCommandException, WrongNumberOfParametersException, InvalidParametersException
	from smartcam.api.commandManager import CommandManager
	from smartcam.api.commands import exitServer, getCableOffset, getCircleOffset, setLight, calibrate, grabPoint, moveGripper, closeGripper, openGripper
	from smartcam.api.server import Server

	# Create CommandManager and register all handlers
	commandManager = CommandManager(3)
	commandManager.addCommand("GOO", getCircleOffset())
	commandManager.addCommand("GRP", grabPoint())
	commandManager.addCommand("GCO", getCableOffset())
	commandManager.addCommand("EXT", exitServer())
	commandManager.addCommand("SFX", setLight())
	commandManager.addCommand("CLB", calibrate())
	commandManager.addCommand("MGR", moveGripper())
	commandManager.addCommand("OGR", openGripper())
	commandManager.addCommand("CGR", closeGripper())

	bind_ip = args.bind_address
	port = args.port

	try:
		bind_ip = configReader.returnEntry("tcp", "host")
		port = configReader.returnEntry("tcp", "port")
	except Exception as e:
		logging.error("couldnt load ip from config file" + str(e.message))

	server = Server(bind_ip, port)

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
	from smartcam.configLoader import configReader
	configReader.loadConfig("config.ini")

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
