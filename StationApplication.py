from Tkinter import *
import serial
import time

ser = serial.Serial('/dev/ttyS0',9600,timeout=1)

def frac(value, total):
    return 360. * value/total

def Update():
    data = ser.readline()  # read data from Arduino
    sizes = data.split(',')

    scale1 = sizes[0]
    scale2 = sizes[1]
    scale3 = sizes[2]
    scale4 = sizes[3]
        
    scale1 = float(scale1)
    scale2 = float(scale2)
    scale3 = float(scale3)
    scale4 = float(scale4)

    if scale1 < 0:
        scale1 = scale1 * -1
    if scale2 < 0:
        scale2 = scale2 * -1
    if scale3 < 0:
        scale3 = scale3 * -1
    if scale4 < 0:
        scale4 = scale4 * -1

    total = scale1+scale2+scale3+scale4
    r1 = frac(scale1, total)
    r2 = frac(scale2, total)
    r3 = frac(scale3, total)
    r4 = frac(scale4, total)

    Rs = [r1,r2,r3,r4]

    return Rs
    

root = Tk()
root.title("Zero Waste Station")
root.configure(background="green")
Label(root, text="Zero Waste Station", bg="green", fg="white", font="none 20 bold").grid(row=0, column=0, sticky=W)

ratios = Update()
c = Canvas(root, bg="white", width=700, height=700)
c.grid(row=1, column=0, sticky=W)
c.create_arc((0,0,700,700), fill="grey", start=0, extent=ratios[0])
c.create_arc((0,0,700,700), fill="blue", start=ratios[0], extent=ratios[1])
c.create_arc((0,0,700,700), fill="green", start=ratios[1], extent=ratios[2])
c.create_arc((0,0,700,700), fill="red", start=ratios[2], extent=ratios[3])

root.mainloop()
