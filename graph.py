# tkinter is used to create the GUI
import tkinter as tk

# matplotlib is the module to generate the graphs
# A tkinter backend is required to use matplotlib in tkinter window
import matplotlib
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2TkAgg)
from matplotlib.figure import Figure

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

# Create a test graph
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Graph")

    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    graph = Graph(root, figsize=(6, 5), dpi=100)
    graph.grid(row=0, column=0, sticky="nsew")

    fig = graph.figure()
    
    axis = fig.add_subplot(111)
    axis.set_title("Test Graph")

    x1 = []
    y1 = []

    x2 = []
    y2 = []

    x3 = []
    y3 = []

    n = 0
    while n <= 2:
        x1.append(n)
        y1.append(n)

        x2.append(n)
        y2.append(n**2)

        x3.append(n)
        y3.append(n**3)

        n += 0.01

    linear, = axis.plot(x1, y1, "r")
    quadratic, = axis.plot(x2, y2, "b")
    cubic, = axis.plot(x3, y3, "g")

    axis.legend([linear, quadratic, cubic],
                ["Linear", "Quadratic", "Cubic"])

    root.mainloop()
