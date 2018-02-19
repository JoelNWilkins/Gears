# Import required modules

# This imports the core functions for working with gears
# We do not have to import math etc. as this is done in gearCore
from gearCore import *

# tkinter is used to create the GUI
# ttk is an extension of tkinter and provides more advanced widgets
# askopenfilename opens a file explorer window to select the file to open
# asksaveasfilename opens a file explorer window to save the file
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import (askopenfilename, askopenfilenames,
                                asksaveasfilename)
from tkinter import messagebox

# matplotlib is the module to generate the graphs
# A tkinter backend is required to use matplotlib in tkinter window
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

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

        # Create variables for the state of each line
        self.showRef = tk.BooleanVar()
        self.showBase = tk.BooleanVar()
        self.showTip = tk.BooleanVar()
        self.showRoot = tk.BooleanVar()
        self.showCentres = tk.BooleanVar()

        # Set the values of the variables
        self.showRef.set(True)
        self.showBase.set(True)
        self.showTip.set(True)
        self.showRoot.set(True)
        self.showCentres.set(True)

        # Shrink the current axis' height by 10% at the bottom
        box = self.axis.get_position()
        self.axis.set_position([box.x0, box.y0 + box.height * 0.1,
                                box.width, box.height * 0.9])

        # Store the file names for later use
        self.fileNames = [fileName]

        # Load a file if it is provided
        if fileName != None:
            self.openFile(self.fileNames)

        # Create a canvas object containing the figure
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.show()
        # Make a tkinter widget from the canvas to add to the frame
        self.tkCanvas = self.canvas.get_tk_widget()
        self.tkCanvas.pack(fill="both", expand=True)
        # Add a toolbar to zoom in on the graph etc.
        self.toolbar = NavigationToolbar2TkAgg(self.canvas, self)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(fill="both", expand=True)

    def openFile(self, fileNames):
        # Update the file names of the current gear(s)
        self.fileNames = fileNames

        try:
            if len(fileNames) > 1:
                # Load the gear data from the xls files
                points1, parameters1 = readData(fileNames[0])
                points2, parameters2 = readData(fileNames[1])

                if (parameters1["alpha"] == parameters2["alpha"]
                    and parameters1["m"] == parameters2["m"]):
                    # Convert the points to a list of x and y values
                    x1, y1 = zip(*points1)
                    x2, y2 = zip(*points2)

                    # Rotate the second gear
                    x2, y2 = rotatePointList(x2, y2, parameters2["angle"] / 2,
                                             (0, 0))

                    # Convert the x and y values to lists
                    x1, y1 = list(x1), list(y1)
                    x2, y2 = list(x2), list(y2)

                    # Adjust the x values so the gears don't overlap
                    for i in range(len(x1)):
                        x1[i] = x1[i] - parameters1["r"]
                    for i in range(len(x2)):
                        x2[i] = x2[i] + parameters2["r"]

                    # Plot the points by invoking the GraphFrame plot function
                    self.plot(x1, y1)
                    self.plot(x2, y2, clear=False)

                    # Add the points on the line of centres
                    xc = [-parameters1["r"], parameters2["r"], 0]
                    yc = [0, 0, 0]

                    # Remove the path from the file name and set the title to the file name
                    if "\\" in fileNames[0]:
                        self.title("{} and {}".format(
                            fileNames[0].split("\\")[-1],
                            fileNames[1].split("\\")[-1]))
                    else:
                        self.title("{} and {}".format(
                            fileNames[0].split("/")[-1],
                            fileNames[1].split("/")[-1]))

                    # Lines and labels to be passed to the legend
                    lines = []
                    labels = []

                    # Add the circles to the graph
                    if self.showRef.get():
                        ref1, = self.addCircle(parameters1["r"], style="b:",
                                               centre=(xc[0], yc[0]))
                        ref2, = self.addCircle(parameters2["r"], style="b:",
                                               centre=(xc[1], yc[1]))
                        lines.append(ref1)
                        labels.append("Reference Circle")
                    if self.showBase.get():
                        base1, = self.addCircle(parameters1["r_b"], style="g:",
                                                centre=(xc[0], yc[0]))
                        base2, = self.addCircle(parameters2["r_b"], style="g:",
                                                centre=(xc[1], yc[1]))
                        lines.append(base1)
                        labels.append("Base Circle")
                    if self.showTip.get():
                        tip1, = self.addCircle(parameters1["r_a"], style="m:",
                                               centre=(xc[0], yc[0]))
                        tip2, = self.addCircle(parameters2["r_a"], style="m:",
                                               centre=(xc[1], yc[1]))
                        lines.append(tip1)
                        labels.append("Tip Circle")
                    if self.showRoot.get():
                        root1, = self.addCircle(parameters1["r_f"], style="y:",
                                                centre=(xc[0], yc[0]))
                        root2, = self.addCircle(parameters2["r_f"], style="y:",
                                                centre=(xc[1], yc[1]))
                        lines.append(root1)
                        labels.append("Root Circle")
                    if self.showCentres.get():
                        lineOfCentres, = self.plot(xc, yc, style="bo-", clear=False)
                        lines.append(lineOfCentres)
                        labels.append("Line of Centres")

                    # Adjust the number of columns of the legend to make it look neater
                    if len(lines) > 4 or len(lines) == 3:
                        cols = 3
                    else:
                        cols = 2

                    # Update the legend
                    self.axis.legend(lines, labels,
                                     loc='upper center',
                                     bbox_to_anchor=(0.5, -0.075),
                                     fancybox=True, shadow=True, ncol=cols)

                    # Hide the legend if it is empty
                    self.axis.get_legend().set_visible(len(lines) != 0)
                else:
                    messagebox.showinfo("Incompatible gears",
                                        """Incompatible gears.
In order 2 for gears to mesh they must have the same module and pressure angle.""")
            else:
                # Select the first item in the list of file names
                fileName = fileNames[0]

                # Load the gear data from the xls file
                points, parameters = readData(fileName)

                # Convert the points into a list of x and y values
                x, y = zip(*points)

                # Plot the points by invoking the GraphFrame plot function
                self.plot(x, y)

                # Remove the path from the file name and set the title to the file name
                if "\\" in fileName:
                    self.title(fileName.split("\\")[-1])
                else:
                    self.title(fileName.split("/")[-1])

                # Lines and labels to be passed to the legend
                lines = []
                labels = []

                # Add the circles to the graph
                if self.showRef.get():
                    ref, = self.addCircle(parameters["r"], style="b:")
                    lines.append(ref)
                    labels.append("Reference Circle")
                if self.showBase.get():
                    base, = self.addCircle(parameters["r_b"], style="g:")
                    lines.append(base)
                    labels.append("Base Circle")
                if self.showTip.get():
                    tip, = self.addCircle(parameters["r_a"], style="m:")
                    lines.append(tip)
                    labels.append("Tip Circle")
                if self.showRoot.get():
                    root, = self.addCircle(parameters["r_f"], style="y:")
                    lines.append(root)
                    labels.append("Root Circle")

                # Adjust the number of columns of the legend to make it look neater
                if len(lines) == 3:
                    cols = 3
                else:
                    cols = 2

                # Update the legend
                self.axis.legend(lines, labels, loc='upper center',
                                 bbox_to_anchor=(0.5, -0.075), fancybox=True,
                                 shadow=True, ncol=cols)

                # Hide the legend if it is empty
                self.axis.get_legend().set_visible(len(lines) != 0)
        except PermissionError:
            messagebox.showerror("Permission Error",
"""Permission Error.
The gear cannot be opened because it is already open in another program.""")                
        try:
            # Reset the toolbar
            self.toolbar.update()
        except:
            pass

        try:
            # Update the canvas to show the gear
            self.canvas.draw()
        except:
            pass

    def plot(self, x, y, style=None, clear=True):
        # Remove any previous gears
        if clear:
            self.axis.clear()
        
        if style == None:
            style = "r"

        # Plot the points onto the graph
        return self.axis.plot(x, y, style)

    def title(self, text):
        # Change the title of the window
        self.root.title("{} - {}".format(text, self.root.title().split(" - ")[-1]))
        
        # Change the title of the plot
        self.axis.set_title(text)

    def addCircle(self, r, style=None, centre=(0, 0)):
        # Generate the list of points on the circle of radius r
        x, y = circlePoints(r, 0.01)

        # Adjust the coordinates for non-zero centres
        if centre[0] != 0:
            for i in range(len(x)):
                x[i] = x[i] + centre[0]
        if centre[1] != 0:
            for i in range(len(y)):
                y[i] = y[i] + centre[1]

        # Set the default style to a red line
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

        # Create the file menu
        # Create a sub-menu to go on the menubar
        self.fileMenu = tk.Menu(self, tearoff=False)
        # Bind the command openFile to the open button
        self.fileMenu.add_command(label="Open...", command=self.openFile,
                                  accelerator="Ctrl+O")
        self.fileMenu.add_command(label="Open Multiple...",
                                  command=self.openMultiple,
                                  accelerator="Ctrl+Shift+O")
        # Add the sub-menu to the menubar
        self.add_cascade(label="File", menu=self.fileMenu)

        # Create the options menu
        # Create a sub-menu to go on the menubar
        self.optionsMenu = tk.Menu(self, tearoff=False)
        # Bind the options to the menu as checkbuttons
        self.optionsMenu.add_checkbutton(label="Reference Circle",
                                       command=self.updateGraph,
                                       variable=self.frame.showRef)
        self.optionsMenu.add_checkbutton(label="Base Circle",
                                       command=self.updateGraph,
                                       variable=self.frame.showBase)
        self.optionsMenu.add_checkbutton(label="Tip Circle",
                                       command=self.updateGraph,
                                       variable=self.frame.showTip)
        self.optionsMenu.add_checkbutton(label="Root Circle",
                                       command=self.updateGraph,
                                       variable=self.frame.showRoot)
        self.optionsMenu.add_checkbutton(label="Line of Centres",
                                       command=self.updateGraph,
                                       variable=self.frame.showCentres)
        # Add the sub-menu to the menubar
        self.add_cascade(label="Options", menu=self.optionsMenu)

        # Create the help menu
        self.add_command(label="Help", command=self.help)

        # Add the key bindings
        root.bind("<Control-o>", self.openFile)
        root.bind("<Control-Shift-KeyPress-O>", self.openMultiple)

    def openFile(self, *args, multiple=False, **kwargs):
        if multiple:
            # Ask the user to select the xls files to open
            fileNames = askopenfilenames(initialdir="data",
                                         filetypes=[("Excel 97-2003 Workbook",
                                                     "*.xls")],
                                         defaultextension=".xls")

            if len(fileNames) != 0:
                if len(fileNames) > 1:
                    if fileNames[0] != fileNames[1]:
                        fileNames = [fileNames[0], fileNames[1]]
                else:
                    fileNames = [fileNames[0], fileNames[0]]
            else:
                return
        else:
            # Ask the user to select the xls file(s) to open
            fileName = askopenfilename(initialdir="data",
                                         filetypes=[("Excel 97-2003 Workbook",
                                                     "*.xls")],
                                         defaultextension=".xls")

            if fileName != "":
                fileNames = [fileName]
            else:
                return
        
        if len(fileNames) != 0:
            # Call the GraphFrame openFile function to load the gear
            self.frame.openFile(fileNames)

    def openMultiple(self, *args, **kwargs):
        self.openFile(multiple=True)

    def updateGraph(self, *args, **kwargs):
        self.frame.openFile(self.frame.fileNames)

    def help(self, *args, **kwargs):
        # Create a popup window for the help guide
        window = tk.Tk()
        window.title("Help")
        window.geometry("600x400")

        # Create a frame containing the text and scrollbar widgets
        frame = tk.Frame(window)
        frame.pack(fill="both", expand=True)

        # Allow the user to resize the window
        #sizegrip = ttk.Sizegrip(window)
        #sizegrip.pack(side="right")

        # Add a text widget to contain the help guide
        text = tk.Text(frame, wrap="word", width=0, height=0)
        text.pack(side="left", fill="both", expand=True)

        # Add a scrollbar widget to navigate through the help guide
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")

        # Bind the scrollbar to the text widget
        text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=text.yview)

        # Open the help file
        with open("help.txt", "rb") as f:
            lines = f.readlines()

        # Add the help file to the text widget
        for line in lines:
            text.insert(tk.END, line.decode("utf-8"))

        # Prevent the user from changing the text
        text.config(state="disabled")
        
# If this program is being run directly this code will be executed
# If this program is being imported this code will not be executed
if __name__ == "__main__":
    # Get a list of xls files in the data directory
    xlsFiles = listXls()
    
    # Create a new tkinter window
    root = tk.Tk()
    root.title("Gear Viewer")
    root.resizable(0, 0)
    # Add the GraphFrame and MenuBar objects
    frame = GraphFrame(root, fileName=xlsFiles[0])
    frame.pack()
    menubar = MenuBar(root, frame)
    # Run the window
    root.mainloop()
