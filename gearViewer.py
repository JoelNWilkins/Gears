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
    from tkinter.filedialog import askopenfilename, askopenfilenames, asksaveasfilename
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

                # Add the circles to the graph
                ref, = self.addCircle(parameters["r"], style="b:")
                base, = self.addCircle(parameters["r_b"], style="g:")
                tip, = self.addCircle(parameters["r_a"], style="m:")
                root, = self.addCircle(parameters["r_f"], style="y:")

                # Shrink the current axis' height by 10% at the bottom
                box = self.axis.get_position()
                self.axis.set_position([box.x0, box.y0 + box.height * 0.1,
                                        box.width, box.height * 0.9])

                # Put a legend below current axis
                self.axis.legend([ref, base, tip, root],
                                 ["Reference circle", "Base circle",
                                  "Tip circle", "Root circle"],
                                 loc='upper center',
                                 bbox_to_anchor=(0.5, -0.075),
                                 fancybox=True, shadow=True, ncol=2)
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

    def plot(self, x, y, style=None, clear=True):
        # Remove any previous gears
        if clear:
            self.axis.clear()
        
        if style == None:
            style = "r"

        # Plot the points onto the graph
        return self.axis.plot(x, y, style)

    def title(self, text):
        # Change the title of the plot
        self.axis.set_title(text)

    def addCircle(self, r, style=None, centre=(0, 0)):
        # Generate the list of points on the circle of radius r
        x, y = circlePoints(r, 0.01)

        if centre[0] != 0:
            for i in range(len(x)):
                x[i] = x[i] + centre[0]
        if centre[1] != 0:
            for i in range(len(y)):
                y[i] = y[i] + centre[1]

        if style == None:
            style = "r"

        # Plot the points onto the graph
        return self.axis.plot(x, y, style)

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
        # Ask the user to select the xls file(s) to open
        fileNames = askopenfilenames(initialdir="data", filetypes=[("Excel 97-2003 Workbook","*.xls")], defaultextension=".csv")

        if len(fileNames) > 1:
            # Load the gear data from the xls files
            points1, parameters1 = readData(fileNames[0])
            points2, parameters2 = readData(fileNames[1])

            # Convert the points to a list of x and y values
            x1, y1 = zip(*points1)
            x2, y2 = zip(*points2)

            # Rotate the second gear
            x2, y2 = rotatePointList(x2, y2, parameters2["angle"]/2, (0, 0))

            # Convert the x and y values to lists
            x1, y1 = list(x1), list(y1)
            x2, y2 = list(x2), list(y2)

            # Adjust the x values so the gears don't overlap
            for i in range(len(x1)):
                x1[i] = x1[i] - parameters1["r"]
            for i in range(len(x2)):
                x2[i] = x2[i] + parameters2["r"]

            # Plot the points by invoking the GraphFrame plot function
            self.frame.plot(x1, y1)
            self.frame.plot(x2, y2, clear=False)

            xc = [-parameters1["r"], parameters2["r"], 0]
            yc = [0, 0, 0]
            lineOfCentres, = self.frame.plot(xc, yc, style="bo-", clear=False)

            # Remove the path from the file name and set the title to the file name
            if "\\" in fileNames[0]:
                self.frame.title("{} and {}".format(fileNames[0].split("\\")[-1],
                                                    fileNames[1].split("\\")[-1]))
            else:
                self.frame.title("{} and {}".format(fileNames[0].split("/")[-1],
                                                    fileNames[1].split("/")[-1]))

            # Add the circles to the graph
            ref1, = self.frame.addCircle(parameters1["r"], style="b:", centre=(xc[0], yc[0]))
            base1, = self.frame.addCircle(parameters1["r_b"], style="g:", centre=(xc[0], yc[0]))
            tip1, = self.frame.addCircle(parameters1["r_a"], style="m:", centre=(xc[0], yc[0]))
            root1, = self.frame.addCircle(parameters1["r_f"], style="y:", centre=(xc[0], yc[0]))
            ref2, = self.frame.addCircle(parameters2["r"], style="b:", centre=(xc[1], yc[1]))
            base2, = self.frame.addCircle(parameters2["r_b"], style="g:", centre=(xc[1], yc[1]))
            tip2, = self.frame.addCircle(parameters2["r_a"], style="m:", centre=(xc[1], yc[1]))
            root2, = self.frame.addCircle(parameters2["r_f"], style="y:", centre=(xc[1], yc[1]))

            # Update the legend
            self.frame.axis.legend([ref1, base1, tip1, root1, lineOfCentres],
                                   ["Reference circle", "Base circle",
                                    "Tip circle", "Root circle", "Line of centres"],
                                   loc='upper center', bbox_to_anchor=(0.5, -0.075),
                                   fancybox=True, shadow=True, ncol=3)
        else:
            # Select the first item in the list of file names
            fileName = fileNames[0]

            # Load the gear data from the xls file
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
            ref, = self.frame.addCircle(parameters["r"], style="b:")
            base, = self.frame.addCircle(parameters["r_b"], style="g:")
            tip, = self.frame.addCircle(parameters["r_a"], style="m:")
            root, = self.frame.addCircle(parameters["r_f"], style="y:")

            # Update the legend
            self.frame.axis.legend([ref, base, tip, root],
                                   ["Reference circle", "Base circle",
                                    "Tip circle", "Root circle"],
                                   loc='upper center', bbox_to_anchor=(0.5, -0.075),
                                   fancybox=True, shadow=True, ncol=2)

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
