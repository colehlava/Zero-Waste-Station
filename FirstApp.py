# FirstApp.py
# Controls Zero Waste Station
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

ser = serial.Serial('/dev/ttyS0', 9600, timeout=1)

MESSAGE_FONT = ("Times New Roman", 25)
LARGE_FONT = ("Times New Roman", 50)
style.use("ggplot")
matplotlib.rcParams['font.size'] = 20.0

f, a = plt.subplots()
labels = ['Paper', 'Cans & Bottles', 'Compost', 'Landfill']
colors = ['grey', 'b', 'g', 'saddlebrown']
explode = (0, 0, 0, 0)


def updateDivRate(sizes):
    total = int(sizes[0] + sizes[1] + sizes[2] +sizes[3])

    if total == 0:
        divRate = "100"
    else:
        cleanWaste = int(sizes[0] + sizes[1] + sizes[2])
        div = cleanWaste / total
        div = int(div * 100)
        divRate = str(div)
    
    label11.configure(text=divRate+"%")


def animate(i):
    a.clear()
    a.axis('equal')
    f.suptitle('Interactive Zero Waste Station', size=55, color='green')
    a.set_title('Distribution of Materials', size=25)
    
    data = []
    sizes = []
    adjustFactor = 1
    data = ser.readline()   # read data from Arduino
    sizes = data.split(b',') # split data into list of individual scale readings

    scale1 = sizes[0]
    scale2 = sizes[1]
    scale3 = sizes[2]
    scale4 = sizes[3]

    scale1 = float(scale1)  # convert readings from strings to floats
    scale2 = float(scale2)
    scale3 = float(scale3)
    scale4 = float(scale4)

    if scale1 < 0:          # handle negative readings
        scale1 = scale1 * -1
    if scale2 < 0:
        scale2 = scale2 * -1
    if scale3 < 0:
        scale3 = scale3 * -1
    if scale4 < 0:
        scale4 = scale4 * -1

    scale1 = scale1 - 7.3   # adjust for weight of trash bins
    scale2 = scale2 - 7.3
    scale3 = scale3 - 7.3
    scale4 = scale4 - 7.3
    
    if scale1 < 1:          # handle values that are too small to graph
        scale1 = adjustFactor
    if scale2 < 1:
        scale2 = adjustFactor
    if scale3 < 1:
        scale3 = adjustFactor
    if scale4 < 1:
        scale4 = adjustFactor

    sizes[0] = scale1
    sizes[1] = scale2
    sizes[2] = scale3
    sizes[3] = scale4

    a.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)

    updateDivRate(sizes)


class FirstApp(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Zero Waste Station")

        #self.attributes('-fullscreen', True) # comment out to disable fullscreen mode
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, GraphPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="NSEW")
        
        self.show_frame(GraphPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button3 = ttk.Button(self, text="Visit Graph Page", command=lambda: controller.show_frame(GraphPage))
        button3.pack()


class GraphPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        canvas._tkcanvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        m = tk.Message(self, font=MESSAGE_FONT, width=400, text="The University of California has a goal to reach zero waste by 2020. Achieving zero waste is defined as diverting at least 90% of discarded materials (by weight) from the landfill. This station was designed to help reach our goal of zero waste by 2020 by emphasizing where materials go after they have been thrown away.", bg='white')
        m.pack()

        label1 = tk.Label(self, font=MESSAGE_FONT, text="\n\nThe current diversion rate is:", bg='white', fg='blue')
        label1.pack(fill=tk.X)
        
        global label11
        label11 = tk.Label(self, font=LARGE_FONT, text="", bg='white')
        label11.pack(fill=tk.BOTH)

        label2 = tk.Label(self, text="", bg='white')
        label2.pack(fill=tk.BOTH, expand=True)



app = FirstApp()
ani = animation.FuncAnimation(f, animate, interval=450)
app.mainloop()
