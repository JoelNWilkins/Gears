# tkinter is used to create the GUI
import tkinter as tk

# matplotlib is the module to generate the graphs
# A tkinter backend is required to use matplotlib in tkinter window
import matplotlib
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2TkAgg)
from matplotlib.figure import Figure

# numpy is used for some mathematical tools
import numpy as np

# Configure matplotlib to use the tkinter backend
matplotlib.use("TkAgg")

class Graph(tk.Frame):
    # A frame containing a matplotlib graph
    
    def __init__(self, parent, *args, **kwargs):
        # Create a frame to contain the widgets
        tk.Frame.__init__(self, parent)

        # Create a new figure and add an axis to the figure
        self.__figure = Figure(*args, **kwargs)

        # Create a canvas object containing the figure
        self.__canvas = FigureCanvasTkAgg(self.__figure, self)
        self.__canvas.show()

        # Add a toolbar to navigate the graph
        self.__toolbar = NavigationToolbar2TkAgg(self.__canvas, self)
        self.__toolbar.update()

        # Pack the canvas in the frame
        self.__canvas._tkcanvas.pack(fill="both", expand=True)

    def figure(self, *args, **kwargs):
        # Return the figure object
        return self.__figure

    def canvas(self, *args, **kwargs):
        # Return the canvas object
        return self.__canvas

    def toolbar(self, *args, **kwargs):
        # Return the toolbar object
        return self.__toolbar

class InfiniteLine(object):
    def __init__(self, *args, **kwargs):
        self.axis = args[0]
        args = args[1:]

        # Turn off autoscale
        self.axis.set_autoscale_on(False)

        if "connect" in kwargs.keys():
            connect = kwargs.pop("connect", None)
        else:
            connect = True

        # Bind the event of changing the limits to updating the graph
        if connect:
            self.axis.callbacks.connect('xlim_changed', self.update)
            self.axis.callbacks.connect('ylim_changed', self.update)

        # Reference the functions of the line
        if "x" in kwargs.keys():
            if type(kwargs["x"]) != int:
                self.xFunc = kwargs.pop("x", None)
            else:
                self.xFunc = False
                self.xValue = kwargs.pop("x", None)
        else:
            self.xFunc = None
        if "y" in kwargs.keys():
            if type(kwargs["y"]) != int:
                self.yFunc = kwargs.pop("y", None)
            else:
                self.yFunc = False
                self.yValue = kwargs.pop("y", None)
        else:
            self.yFunc = None

        # Create a default line to plot to
        self.line, = self.axis.plot(0, 0, *args, **kwargs)
        self.update()

        self = self.line

    def update(self, *args, **kwargs):
        if self.xFunc == None and self.yFunc != None and self.yFunc != False:
            # Calculate the x values
            limits = self.axis.get_xlim()
            x = list(np.arange(start=limits[0], stop=limits[1],
                               step=abs(limits[1] - limits[0]) / 100))
            x.append(limits[1])

            # Calculate the y values
            y = []
            for i in range(len(x)):
                y.append(self.yFunc(x[i]))
        elif self.xFunc != None and self.yFunc == None and self.xFunc != False:
            # Calculate the y values
            limits = self.axis.get_ylim()
            y = list(np.arange(start=limits[0], stop=limits[1],
                               step=abs(limits[1] - limits[0]) / 100))
            y.append(limits[1])

            # Calculate the x values
            x = []
            for i in range(len(y)):
                x.append(self.yFunc(y[i]))
        elif self.xFunc == False:
            # Calculate the y values
            limits = self.axis.get_ylim()
            y = list(np.arange(start=limits[0], stop=limits[1],
                               step=abs(limits[1] - limits[0]) / 100))
            y.append(limits[1])

            # Calculate the x values
            x = []
            for i in range(len(y)):
                x.append(self.xValue)
        elif self.yFunc == False:
            # Calculate the x values
            limits = self.axis.get_xlim()
            x = list(np.arange(start=limits[0], stop=limits[1],
                               step=abs(limits[1] - limits[0]) / 100))
            x.append(limits[1])

            # Calculate the y values
            y = []
            for i in range(len(x)):
                y.append(self.yValue)

        # Update the points on the line
        self.line.set_xdata(x)
        self.line.set_ydata(y)

        return self.line

# Create a test graph
if __name__ == "__main__":
    def f(x):
        return x
    
    def g(x):
        return x**2

    def h(x):
        return x**3
    
    root = tk.Tk()
    root.title("Graph")

    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    graph = Graph(root, figsize=(6, 5), dpi=100)
    graph.grid(row=0, column=0, sticky="nsew")

    fig = graph.figure()
    
    axis = fig.add_subplot(111)
    axis.set_title("Test Graph")

    linear = InfiniteLine(axis, "r", y=f)
    quadratic = InfiniteLine(axis, "g", y=g)
    cubic = InfiniteLine(axis, "b", y=h)

    axis.legend([linear.line, quadratic.line, cubic.line],
                ["Linear", "Quadratic", "Cubic"])

    root.mainloop()
