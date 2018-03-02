# DisplayWeights.py

import serial

ser = serial.Serial('/dev/ttyS0',9600,timeout=1)

try:
	while True:
		data = ser.readline() # read data

		# read data for scale 1
		if data.startswith('a'):
			data = data.replace('a', "")
			if data.startswith('-'):
				data = data.replace('-', "")
			scale1 = float(data)
			print("scale 1: ",scale1)

		# read data for scale 2
		if data.startswith('b'):
			data = data.replace('b', "")
			if data.startswith('-'):
				data = data.replace('-', "")
			scale2 = float(data)
			print("scale 2: ",scale2)

		# read data for scale 3
		if data.startswith('c'):
			data = data.replace('c', "")
			if data.startswith('-'):
				data = data.replace('-', "")
			scale3 = float(data)
			print("scale 3: ",scale3)

		# read data for scale 4
		if data.startswith('d'):
			data = data.replace('d', "")
			if data.startswith('-'):
				data = data.replace('-', "")
			scale4 = float(data)
			print("scale 4: ",scale4)

except KeyboardInterrupt:
	ser.close()
