# DisplayWeights.py

import time
import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

ser = serial.Serial('/dev/ttyS0',9600,timeout=1)

scale1 = 0
scale2 = 0
scale3 = 0
scale4 = 0
count = 0

try:

        labels = 'scale 1', 'scale 2', 'scale 3', 'scale 4'
        sizes = [scale1, scale2, scale3, scale4]
        colors = ['grey', 'b', 'g', 'k']
        explode = (0.1, 0, 0, 0)

        fig, ax = plt.subplots()
        
        def update(num):
                ax.clear()
                ax.axis('equal')
                data = ser.readline() # read data from Arduino

                sizes = data.split(',')
                """
                if count > 0:
                        scale1 = sizes[0]
                        scale2 = sizes[1]
                        scale3 = sizes[2]
                        scale4 = sizes[3]

                scale1 = float(scale1)
                scale2 = float(scale2)
                scale3 = float(scale3)
                scale4 = float(scale4)

		sizes[0] = scale1
		sizes[1] = scale2
		sizes[2] = scale3
		sizes[3] = scale4

                ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)

                count += 1
        """
        ani = FuncAnimation(fig, update, frames=range(100), repeat=False)
        plt.show()


except KeyboardInterrupt:
	ser.close()
	
"""
try:
	while True:
		data = ser.readline() # read data from Arduino

		# interpret data for scale 1
		if data.startswith('a'):
			data = data.replace('a', "")
			if data.startswith('-'):
				data = data.replace('-', "")
			scale1 = float(data)
			#print("scale 1: ")
			#print(scale1)

		# interpret data for scale 2
		if data.startswith('b'):
			data = data.replace('b', "")
			if data.startswith('-'):
				data = data.replace('-', "")
			scale2 = float(data)
			#print("scale 2: ")
			#print(scale2)

		# interpret data for scale 3
		if data.startswith('c'):
			data = data.replace('c', "")
			if data.startswith('-'):
				data = data.replace('-', "")
			scale3 = float(data)
			#print("scale 3: ")
			#print(scale3)

		# interpret data for scale 4
		if data.startswith('d'):
			data = data.replace('d', "")
			if data.startswith('-'):
				data = data.replace('-', "")
			scale4 = float(data)
			#print("scale 4: ")
			#print(scale4)

		#print("\n")

                labels = 'scale 1', 'scale 2', 'scale 3', 'scale 4'
                sizes = [scale1, scale2, scale3, scale4]
                colors = ['grey', 'b', 'g', 'k']
                explode = (0.1, 0, 0, 0)

                fig = plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=0)
                plt.axis('equal')
                plt.legend()
                #ani = animation.FuncAnimation(fig, animate, interval=1000)
                plt.show()
                #time.sleep(2)
                #plt.close()
	
except KeyboardInterrupt:
	ser.close()

"""   
