# FirstApp.py

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style

import tkinter as tk
from tkinter import ttk

import serial

ser = serial.Serial('/dev/ttyS0',9600,timeout=1)

LARGE_FONT = ("Verdana", 12)
style.use("ggplot")

f = Figure(figsize=(5,5), dpi=100)
a = f.add_subplot(111)
labels = ['Paper', 'Cans & Bottles', 'Compost', 'Landfill']
colors = ['grey', 'b', 'g', 'saddlebrown']
explode = (0, 0, 0, 0.1)

def animate(i):
    a.clear()
    a.axis('equal')
    #sizes = [0,0,0,0]

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

def qf(param):
    print(param)
    
class StartPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Visit Page One",
                            command=lambda: controller.show_frame(PageOne))
        button1.pack()

        button2 = ttk.Button(self, text="Visit Page Two",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()

        button3 = ttk.Button(self, text="Visit Graph Page",
                            command=lambda: controller.show_frame(PageThree))
        button3.pack()

class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page One", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text="Visit Page Two",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()

class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page Two", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text="Visit Page One",
                            command=lambda: controller.show_frame(PageOne))
        button2.pack()

class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Graph Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        #f = Figure(figsize=(5,5), dpi=100)
        #a = f.add_subplot(111)
        #a.plot([1,2,3,4,5,6,7,8], [5,6,1,3,8,9,3,5])

        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


app = FirstApp()
ani = animation.FuncAnimation(f, animate, interval=1000)
app.mainloop()
