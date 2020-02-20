#!/usr/bin/python3

import sys
import threading
import serial
import struct
import time

running = True
tbl = [0x0000, 0xC0C1, 0xC181, 0x0140, 0xC301, 0x03C0, 0x0280, 0xC241,0xC601, 0x06C0, 0x0780, 0xC741, 0x0500, 0xC5C1, 0xC481, 0x0440,0xCC01, 0x0CC0, 0x0D80, 0xCD41, 0x0F00, 0xCFC1, 0xCE81, 0x0E40,0x0A00, 0xCAC1, 0xCB81, 0x0B40, 0xC901, 0x09C0, 0x0880, 0xC841,0xD801, 0x18C0, 0x1980, 0xD941, 0x1B00, 0xDBC1, 0xDA81, 0x1A40,0x1E00, 0xDEC1, 0xDF81, 0x1F40, 0xDD01, 0x1DC0, 0x1C80, 0xDC41,0x1400, 0xD4C1, 0xD581, 0x1540, 0xD701, 0x17C0, 0x1680, 0xD641,0xD201, 0x12C0, 0x1380, 0xD341, 0x1100, 0xD1C1, 0xD081, 0x1040,0xF001, 0x30C0, 0x3180, 0xF141, 0x3300, 0xF3C1, 0xF281, 0x3240,0x3600, 0xF6C1, 0xF781, 0x3740, 0xF501, 0x35C0, 0x3480, 0xF441,0x3C00, 0xFCC1, 0xFD81, 0x3D40, 0xFF01, 0x3FC0, 0x3E80, 0xFE41,0xFA01, 0x3AC0, 0x3B80, 0xFB41, 0x3900, 0xF9C1, 0xF881, 0x3840,0x2800, 0xE8C1, 0xE981, 0x2940, 0xEB01, 0x2BC0, 0x2A80, 0xEA41,0xEE01, 0x2EC0, 0x2F80, 0xEF41, 0x2D00, 0xEDC1, 0xEC81, 0x2C40,0xE401, 0x24C0, 0x2580, 0xE541, 0x2700, 0xE7C1, 0xE681, 0x2640,0x2200, 0xE2C1, 0xE381, 0x2340, 0xE101, 0x21C0, 0x2080, 0xE041,0xA001, 0x60C0, 0x6180, 0xA141, 0x6300, 0xA3C1, 0xA281, 0x6240,0x6600, 0xA6C1, 0xA781, 0x6740, 0xA501, 0x65C0, 0x6480, 0xA441,0x6C00, 0xACC1, 0xAD81, 0x6D40, 0xAF01, 0x6FC0, 0x6E80, 0xAE41,0xAA01, 0x6AC0, 0x6B80, 0xAB41, 0x6900, 0xA9C1, 0xA881, 0x6840,0x7800, 0xB8C1, 0xB981, 0x7940, 0xBB01, 0x7BC0, 0x7A80, 0xBA41,0xBE01, 0x7EC0, 0x7F80, 0xBF41, 0x7D00, 0xBDC1, 0xBC81, 0x7C40,0xB401, 0x74C0, 0x7580, 0xB541, 0x7700, 0xB7C1, 0xB681, 0x7640,0x7200, 0xB2C1, 0xB381, 0x7340, 0xB101, 0x71C0, 0x7080, 0xB041,0x5000, 0x90C1, 0x9181, 0x5140, 0x9301, 0x53C0, 0x5280, 0x9241,0x9601, 0x56C0, 0x5780, 0x9741, 0x5500, 0x95C1, 0x9481, 0x5440,0x9C01, 0x5CC0, 0x5D80, 0x9D41, 0x5F00, 0x9FC1, 0x9E81, 0x5E40,0x5A00, 0x9AC1, 0x9B81, 0x5B40, 0x9901, 0x59C0, 0x5880, 0x9841,0x8801, 0x48C0, 0x4980, 0x8941, 0x4B00, 0x8BC1, 0x8A81, 0x4A40,0x4E00, 0x8EC1, 0x8F81, 0x4F40, 0x8D01, 0x4DC0, 0x4C80, 0x8C41,0x4400, 0x84C1, 0x8581, 0x4540, 0x8701, 0x47C0, 0x4680, 0x8641,0x8201, 0x42C0, 0x4380, 0x8341, 0x4100, 0x81C1, 0x8081, 0x4040]

def crc16_add_data(crc, data):
	return ((crc & 0xFF00) >> 8) ^ tbl[(crc & 0x00FF) ^ (data & 0x00FF)]

def crc16(data):
	crc = 0
	for d in data:
		value = int.from_bytes(d, byteorder='big')
		crc = crc16_add_data(crc, value)
	return crc

def crc16_p(data):
	crc = 0
	arr = bytearray(data)
	for b in arr:
		crc = crc16_add_data(crc, b)
	return crc

def write_command(dev, id, cmd, data):
	# 0x03 Fehlernachricht eines Moduls
	# 0x05 Nachricht vom Master zu einem Modul
	# 0x07 Antwort vom Modul
	pack  = struct.pack('<B', 0x05)
	pack += struct.pack('<B', id)
	pack += struct.pack('<B', 1+len(data))
	pack += struct.pack('<B', cmd)
	for d in data:
		pack += struct.pack('<B', d)
	crc = crc16_p(pack)
	pack += struct.pack('<H', crc)

	crc = crc16_p(pack)
	print('>>> ', pack, crc)
	dev.write(bytearray(pack))

def send_ack(dev, id):
	write_command(dev, id, 0x8b, [])

def send_get_state(dev, id):
	time = 1.0
	data = list(struct.pack('<f', time))
	data.append(0x07)
	write_command(dev, id, 0x95, [])

def send_fast_stop(dev, id):
	write_command(dev, id, 0x90, [])

def send_reference(dev, id):
	write_command(dev, id, 0x92, [])

def send_move_to(dev, id, pos):
	data = list(struct.pack('<f', pos))
	#data.extend(list(struct.pack('<f', speed))
	write_command(dev, id, 0xb0, data)

def send_move_to_s(dev, id, pos, speed):
    data = list(struct.pack('<f', pos))
    data.extend(list(struct.pack('<f', speed)))
    write_command(dev, id, 0xb0, data)

def send_get_detailed_error(dev, id):
	write_command(dev, id, 0x96, [])

def check_message(data):
	if len(data) == 0:
		return 0

	group = int.from_bytes(data[0], byteorder='big')
	if group != 0x03 and group != 0x07:
		print('ignoring ',group)
		return 1

	if len(data) < 4:
		return 0

	id = int.from_bytes(data[1], byteorder='big')
	dlen = int.from_bytes(data[2], byteorder='big')

	if len(data) < 5 + dlen:
		return 0

	value = crc16(data)
	if value != 0:
		print('CRC ERROR')
		return 1

	cmd = int.from_bytes(data[3], byteorder='big')

	if cmd == 0x95:
		pos = struct.unpack('<f', data[4]+data[5]+data[6]+data[7])[0]
		speed = struct.unpack('<f', data[8]+data[9]+data[10]+data[11])[0]
		current = struct.unpack('<f', data[12]+data[13]+data[14]+data[15])[0]

		value = int.from_bytes(data[16], byteorder='big')
		error = value & 0x10 != 0

		print('<<< ', id,error,hex(value),pos,speed,current)

	elif cmd == 0x88:
		error = int.from_bytes(data[4], byteorder='big')
		print('<<< ', 'ERROR = ', hex(error))

	else:
		print('<<< ', id,'CMD = ',hex(cmd), data)

	return 5 + dlen


def read_from_port(dev):
	data = []
	while running:
		inp = dev.read(1)
		if len(inp) > 0:
			value = int.from_bytes(inp, byteorder='big')
			data.append(inp)
			handled = check_message(data)
			data = data[handled:]

if len(sys.argv) < 2:
	print("missing arguments")
	sys.exit(1)

dev = serial.Serial('/dev/ttyUSB0', timeout=1)
thread = threading.Thread(target=read_from_port, args=(dev,))
thread.start()

command = sys.argv[1]
if command == "halt":
	send_fast_stop(dev, 11)

elif command == "pos":
	if len(sys.argv) < 3:
		print("position missing")
	else:
		pos = float(sys.argv[2])
		if len(sys.argv) == 3:
			send_move_to(dev, 11, pos)
		else:
			speed = float(sys.argv[3])
			send_move_to_s(dev, 11, pos, speed)

elif command == "ref":
	send_reference(dev, 11)

elif command == "ack":
	send_ack(dev, 11)

#send_reference(dev, 11)
#input('')

#send_move_to(dev, 11, 0.0)
#input('')

#send_get_detailed_error(dev, 11)
#time.sleep(1)
#send_ack(dev, 11)

#send_fast_stop(dev, 11)

#send_get_state(dev, 11)
#input('')

time.sleep(0.2)

running = False
thread.join()
dev.close()

