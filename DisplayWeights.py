# DisplayWeights.py
# Displays live data from load cells from Arduino to a pie chart

import time
import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

ser = serial.Serial('/dev/ttyS0',9600,timeout=1)

try:
        labels = ['scale 1', 'scale 2', 'scale 3', 'scale 4']
        sizes = [0, 0, 0, 0]
        colors = ['grey', 'b', 'g', 'k']
        explode = (0, 0, 0, 0)

        fig, ax = plt.subplots()
        
        def update(num):
                ax.clear()
                ax.axis('equal')
                data = ser.readline() # read data from Arduino
				scale1 = 0
				scale2 = 0
				scale3 = 0
				scale4 = 0
				sizes = [scale1, scale2, scale3, scale4]
                sizes = data.split(',')
                
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
        
        ani = FuncAnimation(fig, update, frames=range(100), repeat=False)
        plt.show()


except KeyboardInterrupt:
	ser.close()
