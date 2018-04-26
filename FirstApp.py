# FirstApp.py
# Author: Cole Hlava

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib import style
import tkinter as tk
from tkinter import ttk
import serial
from PIL import Image, ImageTk
import numpy as np

ser = serial.Serial('/dev/ttyS0',9600,timeout=1)

LARGE_FONT = ("Verdana", 12)
style.use("ggplot")

f, a = plt.subplots()
barFig = Figure(figsize=(5,5), dpi=100)
bg = barFig.add_subplot(111)
barFig.suptitle('How Much Trash\nGets Sent to the Landfill?', fontsize=24, fontweight='bold', color='green')
plt.suptitle('Breakdown of Trash Content', fontsize=36, fontweight='bold', color='green')
labels = ['Paper', 'Cans & Bottles', 'Compost', 'Landfill']
colors = ['grey', 'b', 'g', 'saddlebrown']
explode = (0, 0, 0, 0)
objects = ('Diverted', 'Landfill')
y_pos = np.arange(len(objects))


def animate(i):
    a.clear()
    a.axis('equal')
    data = []
    sizes = []

    data = ser.readline()  # read data from Arduino
    sizes = data.split(b',')

    scale1 = sizes[0]
    scale2 = sizes[1]
    scale3 = sizes[2]
    scale4 = sizes[3]

    scale1 = float(scale1)
    scale2 = float(scale2)
    scale3 = float(scale3)
    scale4 = float(scale4)

    if scale1 <= 0:
        scale1 = scale1 * -1
    if scale2 <= 0:
        scale2 = scale2 * -1
    if scale3 <= 0:
        scale3 = scale3 * -1
    if scale4 <= 0:
        scale4 = scale4 * -1

    sizes[0] = scale1
    sizes[1] = scale2
    sizes[2] = scale3
    sizes[3] = scale4

    a.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)


def animate2(i):
    bg.clear()
    data = []
    sizes = []

    data = ser.readline()  # read data from Arduino
    sizes = data.split(b',')

    scale1 = sizes[0]
    scale2 = sizes[1]
    scale3 = sizes[2]
    scale4 = sizes[3]

    scale1 = float(scale1)
    scale2 = float(scale2)
    scale3 = float(scale3)
    scale4 = float(scale4)

    if scale1 <= 0:
        scale1 = scale1 * -1
    if scale2 <= 0:
        scale2 = scale2 * -1
    if scale3 <= 0:
        scale3 = scale3 * -1
    if scale4 <= 0:
        scale4 = scale4 * -1
    
    total = scale1 + scale2 + scale3 + scale4
    diverted = (scale1 + scale2 + scale3) / total
    landfill = scale4 / total
    performance = [diverted, landfill]
    
    bg.bar(y_pos, performance, align='center', alpha=0.5)
    #bg.title('Diversion Rate')
    #bg.xticks(y_pos, objects)
    #bg.ylabel('Percentage')
  

class FirstApp(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Zero Waste Station")
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo, PageThree):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="NSEW")
        
        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

  
class StartPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Visit Page One", command=lambda: controller.show_frame(PageOne))
        button1.pack()

        button2 = ttk.Button(self, text="Visit Page Two", command=lambda: controller.show_frame(PageTwo))
        button2.pack()

        button3 = ttk.Button(self, text="Visit Graph Page", command=lambda: controller.show_frame(PageThree))
        button3.pack()

        button4 = ttk.Button(self, text="Exit", command=quit)
        button4.pack()


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page One", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text="Visit Page Two", command=lambda: controller.show_frame(PageTwo))
        button2.pack()


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page Two", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text="Visit Page One", command=lambda: controller.show_frame(PageOne))
        button2.pack()


class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label1 = tk.Label(self, text="Zero Waste Station", font=LARGE_FONT)
        label1.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
        button1.pack()

        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        canvas._tkcanvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        #c = tk.Canvas(self, bg="green", width=900, height=900)
        #c.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        #im = Image.open('/home/pi/Documents/ZeroWasteStation/UCSC-Engineering-09.jpg')
        #self.image = ImageTk.PhotoImage(im)
        #c.create_image(50, 50, image=self.image, anchor='ne')
        
        #image = Image.open("/home/pi/capture_3.jpg")
        #photo = ImageTk.PhotoImage(image)
        #c.create_image(50, 50, image=photo, anchor='nw')

        canvas2 = FigureCanvasTkAgg(barFig, self)
        canvas2.show()
        canvas2.get_tk_widget().pack(side=tk.RIGHT, fill=tk.Y)
        canvas2._tkcanvas.pack(side=tk.RIGHT, fill=tk.Y)


app = FirstApp()
ani = animation.FuncAnimation(f, animate, interval=200)
#ani2 = animation.FuncAnimation(barFig, animate2, interval=300)
app.mainloop()
