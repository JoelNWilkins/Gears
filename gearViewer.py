# Import required modules

# This imports the core functions for working with gears
# We do not have to import math etc. as this is done in gearCore
from gearCore import *
# tkinter is used to create the GUI
# ttk is an extension of tkinter and provides more advanced widgets
# askopenfilename opens a file explorer window to select the file to open
# asksaveasfilename opens a file explorer window to save the file
try:
    # The lower case t is for use in python 3
    import tkinter as tk
    from tkinter import ttk
    from tkinter.filedialog import askopenfilename, asksaveasfilename
except:
    # The upper case T is for use in python 2
    import Tkinter as tk
    import ttk
    from tkFileDialog import askopenfilename, asksaveasfilename
# matplotlib is the module to generate the graphs
# A tkinter backend is required to use matplotlib in tkinter window
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
# os is required to find the files in the data directory etc.
import os

# Configure matplotlib to use the tkinter backend
matplotlib.use("TkAgg")
# Change the default directory for saving figures
matplotlib.rcParams["savefig.directory"] = os.getcwd() + "\\images"

class GraphFrame(tk.Frame):
    # A frame containing the matplotlib graph
    
    def __init__(self, root, fileName=None):
        # Create a frame in the root window
        tk.Frame.__init__(self, root)

        # Save the root for later use
        self.root = root

        # Create a new figure and add an axis to the figure
        self.fig = Figure(figsize=(6, 5), dpi=100)
        self.axis = self.fig.add_subplot(111)
        # The equal means that the graph will not be distorted
        self.axis.axis("equal")

        if fileName != None:
            try:
                # Load the gear data from an xls file
                points, parameters = readData(fileName)

                # Convert the points into a list of x and y values
                x, y = zip(*points)

                # Plot the points by invoking the GraphFrame plot function
                self.plot(x, y)

                # Remove the path from the file name and set the title to the file name
                if "\\" in fileName:
                    path, name = "\\".join(fileName.split("\\")[:-1]), fileName.split("\\")[-1]
                    self.title(fileName.split("\\")[-1])
                else:
                    path, name = "/".join(fileName.split("/")[:-1]), fileName.split("/")[-1]
                    self.title(fileName.split("/")[-1])

                self.addCircle(parameters["r"], style="b:")
                self.addCircle(parameters["r_b"], style="g:")
                self.addCircle(parameters["r_a"], style="m:")
                self.addCircle(parameters["r_f"], style="y:")
            except:
                pass

        # Create a canvas object containing the figure
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.show()
        # Make a tkinter widget from the canvas to add to the frame
        self.tkCanvas = self.canvas.get_tk_widget()
        self.tkCanvas.pack()

        # Add a toolbar to zoom in on the graph etc.
        self.toolbar = NavigationToolbar2TkAgg(self.canvas, self)
        self.toolbar.update()
        self.canvas._tkcanvas.pack()

    def plot(self, x, y, style=None):
        # Remove any previous gears
        self.axis.clear()
        
        if style == None:
            style = "r"

        # Plot the points onto the graph
        self.axis.plot(x, y, style)

    def title(self, text):
        # Change the title of the plot
        self.axis.set_title(text)

    def addCircle(self, r, style=None):
        # Generate the list of points on the circle of radius r
        x, y = circlePoints(r, 0.01)

        if style == None:
            style = "r"

        # Plot the points onto the graph
        self.axis.plot(x, y, style)

class MenuBar(tk.Menu):
    # A menubar containing drop-down menus such as file
    
    def __init__(self, root, frame):
        # Create the menubar and bind it to the root window
        tk.Menu.__init__(self, root)
        root.config(menu=self)

        # Save the root and frame for later use
        self.root = root
        self.frame = frame

        # Create a sub-menu to go on the menubar
        self.fileMenu = tk.Menu(self, tearoff=False)
        # Bind the command openFile to the open button
        self.fileMenu.add_command(label="Open...", command=self.openFile, accelerator="Ctrl+O")
        # Add the sub-menu to the menubar
        self.add_cascade(label="File", menu=self.fileMenu)

    def openFile(self, *args, **kwargs):
        # Ask the user to select an xls file to open
        fileName = askopenfilename(initialdir="data", filetypes=[("Excel 97-2003 Workbook","*.xls")], defaultextension=".csv")

        # Load the gear data from an xls file
        points, parameters = readData(fileName)

        # Convert the points into a list of x and y values
        x, y = zip(*points)

        # Plot the points by invoking the GraphFrame plot function
        self.frame.plot(x, y)

        # Remove the path from the file name and set the title to the file name
        if "\\" in fileName:
            self.frame.title(fileName.split("\\")[-1])
        else:
            self.frame.title(fileName.split("/")[-1])

        # Add the circles to the graph
        self.frame.addCircle(parameters["r"], style="b:")
        self.frame.addCircle(parameters["r_b"], style="g:")
        self.frame.addCircle(parameters["r_a"], style="m:")
        self.frame.addCircle(parameters["r_f"], style="y:")

        # Update the canvas to show the gear
        self.frame.canvas.draw()

# If this program is being run directly this code will be executed
# If this program is being imported this code will not be executed
if __name__ == "__main__":
    # Get a list of xls files in the data directory
    xlsFiles = listXls()
    
    # Create a new tkinter window
    root = tk.Tk()
    root.title("Gear Viewer")
    # Add the GraphFrame and MenuBar objects
    frame = GraphFrame(root, fileName=xlsFiles[0])
    frame.pack()
    menubar = MenuBar(root, frame)
    # Run the window
    root.mainloop()
