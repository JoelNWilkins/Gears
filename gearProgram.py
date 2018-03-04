# Import required modules

# This imports the core functions for working with gears
# We do not have to import math etc. as this is done in gearCore
from gearCore import *

# Import the frame containing a matplotlib graph
from graph import *

# tkinter is used to create the GUI
# ttk is an extension of tkinter and provides more advanced widgets
# askopenfilename opens a file explorer window to select the file to open
# asksaveasfilename opens a file explorer window to save the file
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import (askopenfilename, askopenfilenames,
                                asksaveasfilename)
from tkinter import messagebox
from tkinter.colorchooser  import askcolor

# matplotlib is the module to generate the graphs
import matplotlib
from matplotlib import pyplot as plt

# PIL is used for image manipulation
from PIL import Image, ImageTk
import io

# sys is used to get the arguments from the command line
import sys

# Change the default directory for saving figures
matplotlib.rcParams["savefig.directory"] = os.getcwd() + "\\images"

class GearGUI(tk.Tk):
    def __init__(self, *args, fileNames=None, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Gear Generator")
        self.iconbitmap(default="images/logo.ico")

        # Allow the user to resize the graph
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        
        # Add the matplotlib graph frame 
        self.graph = Graph(self)
        self.graph.grid(row=0, column=0, sticky="nsew")

        # Reference the graph frame items
        self.figure = self.graph.figure()
        self.canvas = self.graph.canvas()
        self.toolbar = self.graph.toolbar()

        # Create a new axis to draw to
        self.axis = self.figure.add_subplot(111)
        
        # The equal means that the graph will not be distorted
        self.axis.axis("equal")

        # Create variables for the state of each line
        self.showRef = tk.BooleanVar()
        self.showBase = tk.BooleanVar()
        self.showTip = tk.BooleanVar()
        self.showRoot = tk.BooleanVar()
        self.showCentres = tk.BooleanVar()
        self.showAction = tk.BooleanVar()
        self.showNormal = tk.BooleanVar()
        self.showCentrePoints = tk.BooleanVar()
        self.showPitchPoint = tk.BooleanVar()
        self.showActionPoints = tk.BooleanVar()

        # Set the values of the variables
        self.showRef.set(True)
        self.showBase.set(True)
        self.showTip.set(True)
        self.showRoot.set(True)
        self.showCentres.set(True)
        self.showAction.set(True)
        self.showNormal.set(True)
        self.showCentrePoints.set(True)
        self.showPitchPoint.set(True)
        self.showActionPoints.set(True)

        # A variable to control the animation state
        self.animationOn = tk.BooleanVar()
        self.animationOn.set(True)

        # Add the menubar
        self.menubar = MenuBar(self)

        # Shrink the current axis' height by 10% at the bottom
        # this is so that the legend can fit into the plot
        box = self.axis.get_position()
        self.axis.set_position([box.x0, box.y0 + box.height * 0.1,
                                box.width, box.height * 0.9])

        # Store the file names for later use
        self.fileNames = fileNames

        # Load a file if it is provided
        if fileNames != None:
            self.openFile(self.fileNames)

        # Check to see if the window has been resized
        self.animationStatus = None
        self.bind("<Configure>", self.configure)
        self.canvas.callbacks.connect("scroll_event", self.zoom)

    def openFile(self, fileNames, limits=False):
        # Update the file names of the current gear(s)
        self.fileNames = fileNames

        xlim = self.axis.get_xlim()
        ylim = self.axis.get_ylim()

        try:
            if len(fileNames) > 1:
                # Load the gear data from the xls files
                points1, parameters1 = readData(fileNames[0])
                points2, parameters2 = readData(fileNames[1])

                self.parameters1 = parameters1
                self.parameters2 = parameters2

                if (parameters1["alpha"] == parameters2["alpha"]
                    and parameters1["m"] == parameters2["m"]):
                    # Convert the points to a list of x and y values
                    x1, y1 = zip(*points1)
                    x2, y2 = zip(*points2)

                    # Check if the gear has backlash
                    if not "j_t" in parameters2.keys():
                        if "j_t" in parameters1.keys():
                            parameters2["j_t"] = parameters1["j_t"]
                            self.parameters2["j_t"] = parameters1["j_t"]
                        else:
                            parameters2["j_t"] = 0
                            self.parameters2["j_t"] = 0

                    # Rotate the second gear
                    x2, y2 = rotatePointList(x2, y2, parameters2["angle"] / 2
                        - parameters2["j_t"] / parameters2["r"], (0, 0))

                    # Convert the x and y values to lists
                    x1, y1 = list(x1), list(y1)
                    x2, y2 = list(x2), list(y2)

                    # Adjust the x values so the gears don't overlap
                    for i in range(len(x1)):
                        x1[i] -= parameters1["r"]
                    for i in range(len(x2)):
                        x2[i] += parameters2["r"]

                    # Clear the plot
                    self.axis.clear()

                    # Add the points on the line of centres
                    xc = [-parameters1["r"], parameters2["r"], 0]
                    yc = [0, 0, 0]

                    # Calculate the points on the line of action
                    xa = []
                    ya = []

                    angle = ((math.pi / 2) - math.radians(parameters2["alpha"])
                             - math.asin(parameters2["r"]
                             * math.sin(math.radians(parameters2["alpha"])
                             + math.pi / 2) / parameters2["r_a"]))
                    l = math.sqrt(parameters2["r_a"]**2 + parameters2["r"]**2
                                  - 2 * parameters2["r_a"] * parameters2["r"]
                                  * math.cos(angle))

                    xa.append(l * math.cos(math.radians(parameters1["alpha"])
                                           + math.pi / 2))
                    ya.append(l * math.sin(math.radians(parameters1["alpha"])
                                           + math.pi / 2))

                    angle = ((math.pi / 2) - math.radians(parameters1["alpha"])
                             - math.asin(parameters1["r"]
                             * math.sin(math.radians(parameters1["alpha"])
                             + math.pi / 2) / parameters1["r_a"]))
                    l = math.sqrt(parameters1["r_a"]**2 + parameters1["r"]**2
                                  - 2 * parameters1["r_a"] * parameters1["r"]
                                  * math.cos(angle))

                    xa.append(l * math.cos(math.radians(parameters2["alpha"])
                                           - math.pi / 2))
                    ya.append(l * math.sin(math.radians(parameters2["alpha"])
                                           - math.pi / 2))
                    
                    # Remove the path from the file name and set the title
                    if "\\" in fileNames[0]:
                        self.setTitle("{} and {}".format(
                            fileNames[0].split("\\")[-1].split(".")[0] ,
                            fileNames[1].split("\\")[-1].split(".")[0]))
                    else:
                        self.setTitle("{} and {}".format(
                            fileNames[0].split("/")[-1].split(".")[0],
                            fileNames[1].split("/")[-1].split(".")[0]))

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
                        self.lineOfCentres = InfiniteLine(self.axis, "b", y=0,
                                                          connect=False)
                        lines.append(self.lineOfCentres.line)
                        labels.append("Line of Centres")
                    if self.showAction.get():
                        def f(x):
                            return (- x /
                                    math.tan(math.radians(parameters1["alpha"])))
                            
                        self.lineOfAction = InfiniteLine(self.axis, "g", y=f,
                                                         connect=False)
                        lines.append(self.lineOfAction.line)
                        labels.append("Line of Action")
                    if self.showNormal.get():
                        self.normal = InfiniteLine(self.axis, "m", x=0,
                                                   connect=False)
                        lines.append(self.normal.line)
                        labels.append("Normal")

                    if self.showCentrePoints.get():
                        self.axis.plot(- parameters1["r"], 0, "bo")
                        self.axis.plot(parameters2["r"], 0, "bo")
                    if self.showPitchPoint.get():
                        self.axis.plot(0, 0, "bo")
                    if self.showActionPoints.get():
                        self.axis.plot(xa, ya, "go")

                    self.axis.callbacks.connect('xlim_changed',
                                                self.updateLimits)
                    self.axis.callbacks.connect('ylim_changed',
                                                self.updateLimits)

                    # Plot the points on the gear
                    self.gear1, = self.axis.plot(x1[:], y1[:], "r")
                    self.gear2, = self.axis.plot(x2[:], y2[:], "r")

                    # Adjust the number of columns of the legend
                    if len(lines) > 6:
                        cols = 4
                    elif len(lines) > 4 or len(lines) == 3:
                        cols = 3
                    else:
                        cols = 2

                    # Update the legend
                    self.axis.legend(lines, labels, loc='upper center',
                                     bbox_to_anchor=(0.5, -0.075),
                                     fancybox=True, shadow=True, ncol=cols)

                    # Hide the legend if it is empty
                    self.axis.get_legend().set_visible(len(lines) != 0)

                    # Start the animation loop
                    self.after(5, self.animate)
                else:
                    messagebox.showinfo("Incompatible Gears",
"""Incompatible Gears.
In order 2 for gears to mesh they must have the same module and pressure angle.""")
            else:
                # Select the first item in the list of file names
                fileName = fileNames[0]

                # Load the gear data from the xls file
                points, parameters = readData(fileName)

                # Convert the points into a list of x and y values
                x, y = zip(*points)

                # Clear the plot
                self.axis.clear()

                # Remove the path from the file name and set the title
                if "\\" in fileName:
                    self.setTitle(fileName.split("\\")[-1].split(".")[0])
                else:
                    self.setTitle(fileName.split("/")[-1].split(".")[0])

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

                # Plot the points on the gear
                self.axis.plot(x, y, "r")

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
The gear cannot be opened because it is already open in another program.
Close the program and try again.""")
            
        try:
            if not limits:
                # Reset the toolbar
                self.toolbar.update()
        except:
            pass

        try:
            if limits:
                self.axis.set_xlim(xlim)
                self.axis.set_ylim(ylim)
            
            # Update the canvas to show the gear
            self.canvas.draw()
        except:
            pass

    def updateLimits(self, *args, **kwargs):
        # Try to update the limits on each of the infinite lines
        try:
            self.lineOfAction.update()
        except:
            pass

        try:
            self.lineOfCentres.update()
        except:
            pass

        try:
            self.normal.update()
        except:
            pass

    def exportImage(self, *args, **kwargs):
        if "linewidth" in kwargs.keys():
            linewidth = kwargs["linewidth"]
        else:
            linewidth = 1

        if "size" in kwargs.keys():
            size_pixels = kwargs["size"]
        else:
            size_pixels = (1024, 1024)

        if "cross" in kwargs.keys():
            cross = kwargs["cross"]
        else:
            cross = True
        
        # Load the gear data from the xls file
        points, parameters = readData(self.fileNames[0])

        # Convert the points into a list of x and y values
        x, y = zip(*points)

        # Calculate the size in inches
        size_inches = (parameters["d_a"] / 25.4,
                       parameters["d_a"] / 25.4)

        # Calculate the dpi based on the 2 sizes
        resolution = size_pixels[0] / size_inches[0]

        # Create the figure to save as an image
        fig = plt.figure(frameon=False, dpi=resolution)
        fig.set_size_inches(*size_inches, forward=True)

        # Create an axes in the figure
        axes = plt.Axes(fig, [0., 0., 1., 1.])
        axes.set_axis_off()
        axes.margins(0, 0)
        fig.add_axes(axes)

        # Plot the gear points on the axes
        axes.plot(x, y, "k", linewidth=linewidth)

        # Plot invisible points to fix the boundries
        axes.plot([0, 0, -parameters["r_a"], parameters["r_a"]],
                  [-parameters["r_a"], parameters["r_a"], 0, 0],
                  "k", linewidth=linewidth, alpha=0)

        if parameters["r_f"] < parameters["r_b"]:
            R = parameters["r_f"]
        else:
            R = parameters["r_b"]

        if cross:
            # Plot the centre cross
            axes.plot([0, 0], [-R/4, R/4], "k",
                      linewidth=linewidth)
            axes.plot([-R/4, R/4], [0, 0], "k",
                      linewidth=linewidth)

        # Get the name of the file to save to
        if "\\" in self.fileNames[0]:
            fileName = self.fileNames[0].split("\\")[-1].replace(".xls", ".png")
        elif "/" in self.fileNames[0]:
            fileName = self.fileNames[0].split("/")[-1].replace(".xls", ".png")

        # Ask the user to select the file name to save as
        fileName = asksaveasfilename(parent=self,
                                     initialdir=os.getcwd() + "\\images",
                                     initialfile=fileName,
                                     filetypes=[("PNG image", "*.png"),
                                                ("JPEG image", "*.jpg")],
                                     defaultextension=".png")

        if fileName != "":
            if ".jpg" in fileName:
                # Save the image in a buffer
                buf = io.BytesIO()
                fig.savefig(buf, format="png")
                buf.seek(0)

                # Open the image using PIL and convert to a jpg
                image = Image.open(buf)
                image.convert("RGB").save(fileName, "JPEG")
            else:
                # Save the figure as a png
                fig.savefig(fileName, bbox_inches=0, transparent=True)

            imageViewer = ImageViewer(self, fileName)

            return True
        else:
            return False

    def animate(self, *args, **kwargs):
        if self.animationOn.get():
            # Get the current positions of the points
            x1, y1 = self.gear1.get_data()
            x2, y2 = self.gear2.get_data()

            # Calculate the ratio of speeds
            ratio = self.parameters1["z"] / self.parameters2["z"]

            # Rotate the points
            x1, y1 = rotatePointList(x1, y1,
                - self.parameters1["p"] / (10 * self.parameters1["r"]),
                (-self.parameters1["r"], 0))
            x2, y2 = rotatePointList(x2, y2,
                ratio * self.parameters1["p"] / (10 * self.parameters1["r"]),
                (self.parameters2["r"], 0))

            # Update the points
            self.gear1.set_data(x1, y1)
            self.gear2.set_data(x2, y2)

            # Update the canvas to show the new points
            self.canvas.draw()
        
            # Rebind the loop to create an animation
            self.after(5, self.animate)

    def updateAnimation(self, *args, **kwargs):
        if "animation" in kwargs.keys():
            if kwargs["animation"]:
                self.animationOn.set(kwargs["animation"])
                
                if self.animationOn.get():
                    # Start the animation loop
                    self.after(5, self.animate)
            else:
                self.animationOn.set(False)
        elif not self.animationOn.get():
            self.animationOn.set(True)
            # Start the animation loop
            self.after(5, self.animate)
        else:
            self.animationOn.set(False)

    def restartAnimation(self, *args, **kwargs):
        if self.animationStatus != None:
            self.animationOn.set(self.animationStatus)
            self.animationStatus = None

    def updateGraph(self, *args, **kwargs):
        # Reload the currently opened file
        self.openFile(self.fileNames, limits=True)

    def configure(self, event):
        if (event.width == self.winfo_width()
            and event.height == self.winfo_height()):
            # Record the status of the animation (on / off)
            if self.animationStatus == None:
                self.animationStatus = self.animationOn.get()
            self.animationOn.set(False)

            self.updateGraph(limits=True)

            # Restart the animation
            self.after(500, self.restartAnimation)

    def zoom(self, event):
        xlim = self.axis.get_xlim()
        ylim = self.axis.get_ylim()
        xpos = (xlim[0] + xlim[1]) / 2
        ypos = (ylim[0] + ylim[1]) / 2
        xrange = (xlim[1] - xlim[0]) / 2
        yrange = (ylim[1] - ylim[0]) / 2

        # Adjust the scale factor based on the scroll direction
        if event.button == "up":
            scale = 9 / 10
        elif event.button == "down":
            scale = 10 / 9

        # Update the zoom limits
        self.axis.set_xlim([xpos - xrange * scale, xpos + xrange * scale])
        self.axis.set_ylim([ypos - yrange * scale, ypos + yrange * scale])

        # Redraw the canvas
        self.canvas.draw()

    def setTitle(self, text):
        # Change the title of the window
        self.title("{} - {}".format(text, self.title().split(" - ")[-1]))
        
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

    def trochoid(self, t, R, x_0, y_0):
        # A function to generate the root fillet curve
        x = ((R + x_0) * math.cos(t) + (R * t + y_0) * math.sin(t))
        y = (- (R + x_0) * math.sin(t) + (R * t + y_0) * math.cos(t))

        return (x, y)

    def generateGear(self, *args, **kwargs):
        z = kwargs["z"]
        alpha = kwargs["alpha"]
        m = kwargs["m"]
        backlash = kwargs["backlash"]
        addendum = kwargs["addendum"]
        dedendum = kwargs["dedendum"]
        
        try:
            # Calculate the parameters for the gear
            parameters = calculateParameters(z, alpha, m, backlash, addendum,
                                             dedendum)

            # Calculate the points on the gear
            x, y = self.gearPoints(parameters, 0.075)

            # This adds the list of x and y values in coordinate form
            points = list(zip(x, y))

            # Ask the user to select the file name to save as
            fileName = asksaveasfilename(parent=self, initialdir="data",
                                         filetypes=[("Excel 97-2003 Workbook",
                                                     "*.xls")],
                                         defaultextension=".xls")
            # Save the gear points to an xls file
            writeData(fileName, points, parameters)

            self.openFile([fileName])

            return True
        except PermissionError:
            messagebox.showerror("Permission Error",
"""Permission Error.
The gear cannot be saved because the file is already open in another program.""")
        except FileNotFoundError:
            pass
        except:
            raise

        return False

    def gearPoints(self, parameters, step):
        # This is the main function to generate a gear

        # gap is the angle between the bases of 2 involute curves
        gap = (parameters["angle"] - ((parameters["s"] / parameters["r"])
            + 2 * (involute(getAlpha(parameters["r_b"], parameters["r"]))
            - involute(getAlpha(parameters["r_b"], parameters["r_b"])))))

        # If the base radius is smaller than the dedendum
        # set the cut off radius to the dedendum
        if parameters["r_f"] > parameters["r_b"]:
            R = parameters["r_f"]
        else:
            R = parameters["r_b"]

        # Calculate the point used to generate the trochoid curve
        x_0 = - (parameters["h_a"] + parameters["c"])
        y_0 = (0.25 * math.pi * parameters["m"]
               + x_0 * math.tan(math.radians(parameters["alpha"])))

        x = []
        y = []
        for i in range(parameters["z"]):
            # Generate the first part of the involute curve
            for r in frange(R, parameters["r_a"], step):
                alpha = getAlpha(parameters["r_b"], r)
                
                point = points(r, alpha)
                point = rotate(point, (parameters["angle"] * i) + gap / 2,
                               (0, 0))

                x.append(point[0])
                y.append(point[1])

            # Find the end points of the involute curves
            point1 = getCartesian(parameters["r_a"],
                                  (parameters["angle"] * i) + gap / 2
                                  + (involute(getAlpha(parameters["r_b"],
                                                       parameters["r_a"]))
                                     - involute(getAlpha(parameters["r_b"],
                                                         parameters["r_b"]))))
            point2 = getCartesian(parameters["r_a"],
                                  (parameters["angle"] * (i + 1)) - gap / 2
                                  - (involute(getAlpha(parameters["r_b"],
                                                       parameters["r_a"]))
                                     - involute(getAlpha(parameters["r_b"],
                                                         parameters["r_b"]))))

            m_1 = (point1[1] - point2[1]) / (point1[0] - point2[0])

            # Generate the top of the tooth
            for theta in frange((parameters["angle"] * i) + gap / 2
                                + (involute(getAlpha(parameters["r_b"],
                                                     parameters["r_a"]))
                                   - involute(getAlpha(parameters["r_b"],
                                                       parameters["r_b"]))),
                                (parameters["angle"] * (i + 1)) - gap / 2
                                - (involute(getAlpha(parameters["r_b"],
                                                     parameters["r_a"]))
                                   - involute(getAlpha(parameters["r_b"],
                                                       parameters["r_b"]))),
                                getDeltaTheta(parameters["r_a"], step)):
                point3 = getCartesian(parameters["r_a"], theta)

                m_2 = point3[1] / point3[0]

                point = [(point1[1] - m_1 * point1[0]) / (m_2 - m_1)]
                point.append(m_2 * point[0])

                x.append(point[0])
                y.append(point[1])
            
            # Generate the second part of the involute curve
            for r in frange(parameters["r_a"], R, step):
                alpha = getAlpha(parameters["r_b"], r)
                
                point = points(r, -alpha)
                point = rotate(point, (parameters["angle"] * (i + 1)) - gap / 2,
                               (0, 0))

                x.append(point[0])
                y.append(point[1])
            
            if R == parameters["r_b"]:
                # Generate the first part of the trochoid curve
                for theta in frange(math.pi, - y_0 / parameters["r"],
                                    3 * getDeltaTheta(parameters["r_b"], step)):
                    point = self.trochoid(- theta, parameters["r"], x_0, - y_0)
                    point = rotate(point, (parameters["angle"] * (i + 1))
                                   - (parameters["j_t"] / parameters["d"])
                                   - 2 * math.pi, (0, 0))

                    r, angle = getPolar(*point)
                        
                    if r < parameters["r_f"] or theta < - y_0 / parameters["r"]:
                        point = getCartesian(parameters["r_f"], angle)

                    if (r < parameters["r_b"]
                        and angle < parameters["angle"] * (i + 1)):
                        x.append(point[0])
                        y.append(point[1])

                # Find the angles for the end of the trochoid curves
                point = self.trochoid(y_0 / parameters["r"],
                                      parameters["r"], x_0, - y_0)
                point = rotate(point, (parameters["angle"] * (i + 1))
                               - 2 * math.pi, (0, 0))
                r, angle1 = getPolar(*point)
                point = self.trochoid(- y_0 / parameters["r"],
                                      parameters["r"], x_0, y_0)
                point = rotate(point, (parameters["angle"] * (i + 1))
                               - 2 * math.pi, (0, 0))
                r, angle2 = getPolar(*point)

                # Adjust the angles to get the correct range
                if angle1 > angle2:
                    angle1 -= 2 * math.pi

                # Generate the curve between the teeth
                for theta in frange(angle1, angle2,
                                    getDeltaTheta(parameters["r_f"], step)):
                    point = getCartesian(parameters["r_f"], theta)

                    x.append(point[0])
                    y.append(point[1])

                # Generate the second part of the trochoid curve
                for theta in frange(- y_0 / parameters["r"], math.pi,
                                    3 * getDeltaTheta(parameters["r_b"], step)):
                    point = self.trochoid(theta, parameters["r"], x_0, y_0)
                    point = rotate(point, (parameters["angle"] * (i + 1))
                                   + (parameters["j_t"] / parameters["d"])
                                   - 2 * math.pi, (0, 0))

                    r, angle = getPolar(*point)
                        
                    if r < parameters["r_f"] or theta < - y_0 / parameters["r"]:
                        point = getCartesian(parameters["r_f"], angle)

                    if (r < parameters["r_b"]
                        and angle > parameters["angle"] *
                        ((i + 1) % parameters["z"])):
                        x.append(point[0])
                        y.append(point[1])
            else:
                # Generate the curve between the teeth
                for theta in frange((parameters["angle"] * (i + 1)) - gap / 2,
                                    (parameters["angle"] * (i + 1)) + gap / 2,
                                    getDeltaTheta(R, step)):
                    point = getCartesian(R, theta)

                    x.append(point[0])
                    y.append(point[1])

        # Add the first values to the end to make the gear meet up
        x.append(x[0])
        y.append(y[0])
        
        return (x, y)

class InputFrame(tk.Toplevel):
    def __init__(self, parent, *args, defaults=None, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)
        self.title("New Gear")
        self.resizable(False, False)

        # Save the parent for later use
        self.master = parent

        # Create frames to organise the widgets
        self.inputFrame = tk.Frame(self)
        self.buttonFrame = tk.Frame(self)
        # Set the positions of the frames
        self.inputFrame.grid(row=0, column=0)
        self.buttonFrame.grid(row=1, column=0)

        # Create labels and entries for the required parameters
        self.label1 = tk.Label(self.inputFrame, text="Number of teeth: ")
        self.label1.grid(row=0, column=0, sticky="e")
        self.entry1 = ttk.Entry(self.inputFrame)
        self.entry1.grid(row=0, column=1, sticky="w", pady=2)
        self.label2 = tk.Label(self.inputFrame, text="Pressure angle: (°) ")
        self.label2.grid(row=1, column=0, sticky="e")
        self.entry2 = ttk.Entry(self.inputFrame)
        self.entry2.grid(row=1, column=1, sticky="w", pady=2)
        self.label3 = tk.Label(self.inputFrame, text="Module: (mm) ")
        self.label3.grid(row=2, column=0, sticky="e")
        self.entry3 = ttk.Entry(self.inputFrame)
        self.entry3.grid(row=2, column=1, sticky="w", pady=2)

        # Add the label to show the advanced parameters
        self.showAdvanced = False
        self.advanced = tk.Label(self.inputFrame, text=u"Advanced \u25BC")
        self.advanced.grid(row=3, column=1, sticky="e")
        self.advanced.bind("<Button-1>", self.toggleAdvanced)

        # Create labels and entries for the advanced parameters
        self.label4 = tk.Label(self.inputFrame, text="Backlash: (%) ")
        self.entry4 = ttk.Entry(self.inputFrame)
        self.label5 = tk.Label(self.inputFrame, text="Addendum: ")
        self.entry5 = ttk.Entry(self.inputFrame)
        self.label6 = tk.Label(self.inputFrame, text="Dedendum: ")
        self.entry6 = ttk.Entry(self.inputFrame)

        # Update the grid layout
        self.toggleAdvanced(show=self.showAdvanced)

        # Insert default values into the entries if defaults exist
        if defaults != None:
            if "z" in defaults.keys():
                if defaults["z"] != None:
                    self.entry1.insert(0, defaults["z"])
            if "alpha" in defaults.keys():
                if defaults["alpha"] != None:
                    self.entry2.insert(0, defaults["alpha"])
            if "m" in defaults.keys():
                if defaults["m"] != None:
                    self.entry3.insert(0, defaults["m"])
            if "backlash" in defaults.keys():
                if defaults["backlash"] != None:
                    self.entry4.insert(0, defaults["backlash"])
            if "addendum" in defaults.keys():
                if defaults["addendum"] != None:
                    self.entry5.insert(0, defaults["addendum"])
            if "dedendum" in defaults.keys():
                if defaults["dedendum"] != None:
                    self.entry6.insert(0, defaults["dedendum"])

        # Create a button to generate the gear
        self.button = ttk.Button(self.buttonFrame, text="Generate Gear",
                                 command=self.generateGear)
        self.button.pack(pady=2)

        # Bind the escape key to close the window
        self.bind("<Escape>", self.closeWindow)

        # Bring the frame into focus
        self.focus_force()

    def toggleAdvanced(self, *args, **kwargs):
        if "show" in kwargs.keys():
            self.showAdvanced = kwargs["show"]
        else:
            self.showAdvanced = not self.showAdvanced

        if self.showAdvanced:
            # Update the arrow direction
            self.advanced.config(text=u"Advanced \u25B2")
            
            # Add the advanced options to the grid
            self.label4.grid(row=3, column=0, sticky="e")
            self.entry4.grid(row=3, column=1, sticky="w", pady=2)
            self.label5.grid(row=4, column=0, sticky="e")
            self.entry5.grid(row=4, column=1, sticky="w", pady=2)
            self.label6.grid(row=5, column=0, sticky="e")
            self.entry6.grid(row=5, column=1, sticky="w", pady=2)

            # Update the position of the advanced label
            self.advanced.grid(row=6, column=1, sticky="e")
        else:
            # Update the arrow direction
            self.advanced.config(text=u"Advanced \u25BC")

            # Update the position of the advanced label
            self.advanced.grid(row=3, column=1, sticky="e")
            
            # Try to remove the advanced options to the grid
            try:
                self.label4.grid_forget()
                self.entry4.grid_forget()
                self.label5.grid_forget()
                self.entry5.grid_forget()
                self.label6.grid_forget()
                self.entry6.grid_forget()
            except:
                pass

    def generateGear(self, *args, **kwargs):
        try:
            # Read the values from the entries
            z = int(self.entry1.get())
            alpha = float(self.entry2.get())
            m = float(self.entry3.get())
            backlash = float(self.entry4.get()) / 100
            addendum = float(self.entry5.get())
            dedendum = float(self.entry6.get())

            # Check if the teeth are in proportion
            if addendum > dedendum:
                messagebox.showerror("Input Error",
"""Input Error.
There is an issue with the values you entered.
The addendum should be smaller than the dedendum.""")

                # Bring the frame into focus
                self.focus_force()

                return
        
            # Create a gear from the inputed values
            if self.master.generateGear(z=z, alpha=alpha, m=m,
                                        backlash=backlash, addendum=addendum,
                                        dedendum=dedendum):
                # Close the window if successful
                self.destroy()
            else:
                # Bring the frame into focus if not
                self.focus_force()
        except ValueError:
            messagebox.showerror("Input Error",
"""Input Error.
There is an issue with the values you entered.
Either some are missing or are in the wrong format.""")

            # Bring the frame into focus
            self.focus_force()
        except:
            raise

    def closeWindow(self, *args, **kwargs):
        self.destroy()

class ExportImageFrame(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)
        self.title("Export as Image")
        self.resizable(False, False)

        # Create a list of the possible sizes
        sizes = []
        sizeLabels = []
        for n in range(8, 17):
            sizes.append((2**n, 2**n))
            sizeLabels.append("{}x{}".format(2**n, 2**n))

        # Create a combobox to get the output size
        self.sizeLabel = tk.Label(self, text="Size: (px) ")
        self.sizeLabel.grid(row=0, column=0, sticky="e", pady=2)
        self.sizeSelecter = ttk.Combobox(self, values=sizeLabels,
                                         state="readonly")
        self.sizeSelecter.grid(row=0, column=1, sticky="ew", pady=2)
        self.sizeSelecter.set(sizeLabels[2])

        # Create an entry to get the linewidth
        self.linewidthLabel = tk.Label(self, text="Linewidth: ")
        self.linewidthLabel.grid(row=1, column=0, sticky="e", pady=2)
        self.linewidthEntry = ttk.Entry(self)
        self.linewidthEntry.grid(row=1, column=1, sticky="ew", pady=2)
        self.linewidthEntry.insert(0, 1)

        # Create a checkbutton to get the centre cross status
        self.showCross = tk.BooleanVar()
        self.showCross.set(True)

        self.crossCheck = ttk.Checkbutton(self, text="Centre cross",
                                          variable=self.showCross)
        self.crossCheck.grid(row=2, column=1, sticky="w", pady=2)

        # Create a button to export the image
        exportButton = ttk.Button(self, text="Export", command=self.export)
        exportButton.grid(row=3, column=0, columnspan=2, sticky="ns", pady=2)

        # Bind the escape key to close the window
        self.bind("<Escape>", self.closeWindow)

        # Bring the frame into focus
        self.focus_force()

    def export(self, *args, **kwargs):
        # Try to export the gear as a png file
        width = int(self.sizeSelecter.get().split("x")[0])
        if self.master.exportImage(linewidth=float(self.linewidthEntry.get()),
                                   size=(width, width),
                                   cross=self.showCross.get()):
            # If the export is successful close the window
            self.destroy()
        else:
            # Bring the frame into focus
            self.focus_force()

    def closeWindow(self, *args, **kwargs):
        self.destroy()

class ExportDXFFrame(tk.Toplevel):
    def __init__(self, *args, defaults=None, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)
        self.title("Export as DXF")
        self.resizable(False, False)

        # Create frames to organise the widgets
        self.inputFrame = tk.Frame(self)
        self.buttonFrame = tk.Frame(self)
        # Set the positions of the frames
        self.inputFrame.grid(row=0, column=0)
        self.buttonFrame.grid(row=1, column=0)

        # Create an entry to get the facewidth
        self.faceWidthLabel = tk.Label(self.inputFrame,
                                       text="Face Width: (mm) ")
        self.faceWidthLabel.grid(row=0, column=0, sticky="w", pady=2)
        self.faceWidthEntry = ttk.Entry(self.inputFrame)
        self.faceWidthEntry.grid(row=0, column=1, sticky="ew", pady=2)

        # Add the label to show the advanced parameters
        self.showAdvanced = False
        self.advanced = tk.Label(self.inputFrame, text=u"Advanced \u25BC")
        self.advanced.grid(row=1, column=1, sticky="e")
        self.advanced.bind("<Button-1>", self.toggleAdvanced)

        # Create an entry to get the helix angle
        self.helixAngleLabel = tk.Label(self.inputFrame,
                                        text="Helix Angle: (°) ")
        self.helixAngleEntry = tk.Entry(self.inputFrame)

        # Insert default values into the entries if defaults exist
        if defaults != None:
            if "width" in defaults.keys():
                if defaults["width"] != None:
                    self.faceWidthEntry.insert(0, defaults["width"])
            if "beta" in defaults.keys():
                if defaults["beta"] != None:
                    self.helixAngleEntry.insert(0, defaults["beta"])
        
        # Create a button to export the image
        exportButton = ttk.Button(self.buttonFrame, text="Export",
                                  command=self.export)
        exportButton.grid(row=3, column=0, columnspan=2, sticky="ns", pady=2)

        # Bind the escape key to close the window
        self.bind("<Escape>", self.closeWindow)

        # Bring the frame into focus
        self.focus_force()

    def export(self, *args, **kwargs):
        pass

    def toggleAdvanced(self, *args, **kwargs):
        if "show" in kwargs.keys():
            self.showAdvanced = kwargs["show"]
        else:
            self.showAdvanced = not self.showAdvanced

        if self.showAdvanced:
            # Update the arrow direction
            self.advanced.config(text=u"Advanced \u25B2")
            
            # Add the advanced options to the grid
            self.helixAngleLabel.grid(row=1, column=0, sticky="e", pady=2)
            self.helixAngleEntry.grid(row=1, column=1, sticky="ew", pady=2)

            # Update the position of the advanced label
            self.advanced.grid(row=2, column=1, sticky="e")
        else:
            # Update the arrow direction
            self.advanced.config(text=u"Advanced \u25BC")

            # Update the position of the advanced label
            self.advanced.grid(row=1, column=1, sticky="e")
            
            # Try to remove the advanced options to the grid
            try:
                self.helixAngleLabel.grid_forget()
                self.helixAngleEntry.grid_forget()
            except:
                pass

    def closeWindow(self, *args, **kwargs):
        self.destroy()

class ImageViewer(tk.Toplevel):
    def __init__(self, master, fileName, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)
        
        if "size" in kwargs.keys():
            size = kwargs["size"]
        else:
            size = (256, 256)

        # Allow the user to resize the image
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Get the name of the file for the title
        if "\\" in fileName:
            title = fileName.split("\\")[-1].split(".")[0]
        elif "/" in fileName:
            title = fileName.split("/")[-1].split(".")[0]

        self.title("{} - {}".format(title,
                                    self.master.title().split(" - ")[-1]))

        # Load the image to view
        self.image = Image.open(fileName)

        # Create a version of the image to go in the label
        copy = self.image.resize(size)
        photo = ImageTk.PhotoImage(copy)

        # Create the tkinter widget to hold the image
        self.panel = tk.Label(self, image=photo, width=size[0], height=size[1])
        self.panel.image = photo
        self.panel.grid(row=0, column=0, sticky="nsew")

        # Bind the events to the window
        self.bind("<Escape>", self.destroy)
        self.bind("<Configure>", self.resize)

    def resize(self, event):
        # Resize the image is the window is resized
        if event.width < event.height:
            size = (event.width, event.width)
        else:
            size = (event.height, event.height)
            
        # Create a version of the image to go in the label
        copy = self.image.resize(size)
        photo = ImageTk.PhotoImage(copy)

        # Update the tkinter widget with the new image
        self.panel.config(image=photo)
        self.panel.image = photo

class FormatFrame(tk.Toplevel):  
    def __init__(self, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)
        self.title("Format")
        self.resizable(False, False)

        self.gearColourLabel = tk.Label(self, text="Gear Colour: ")
        self.gearColourLabel.grid(row=0, column=0, sticky="e", pady=2)
        self.gearColour = tk.Button(self, background="red")
        self.gearColour.grid(row=0, column=1, pady=2)
        self.gearColour.grid_propagate(False)
        self.gearColour.config(width=self.gearColour.winfo_height())
        self.gearColour.bind("<Button-1>", self.getColour)

    def getColour(self, *args, **kwargs):
        colour = askcolor(parent=self)
        self.gearColour.config(background=colour[1])
        self.focus_force()

class LineSelector(tk.Frame):
    styles = ["solid", "dashed", "dotted", "dashdot"]
    
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.styleLabel = tk.Label(self, text="Line Style: ")
        self.styleLabel.grid(row=0, column=0, sticky="e")
        self.styleCombo = ttk.Combobox(self, values=self.styles)
        self.styleCombo.grid(row=0, column=1, sticky="ew")

class MenuBar(tk.Menu):
    def __init__(self, parent, *args, **kwargs):
        # Create the menubar and bind it to the parent window
        tk.Menu.__init__(self, master=parent)
        self.master.config(menu=self)

        # Create the export cascade
        self.exportMenu = tk.Menu(self, tearoff=False)
        # Add the button for each export type
        self.exportMenu.add_command(label="Export as Image",
                                    command=self.exportImage)
        self.exportMenu.add_command(label="Export as DXF",
                                    command=self.exportDXF)

        # Create the file menu
        # Create a sub-menu to go on the menubar
        self.fileMenu = tk.Menu(self, tearoff=False)
        # Bind the buttons to the menu
        self.fileMenu.add_command(label="New Gear", command=self.newGear,
                                  accelerator="Ctrl-N")
        self.fileMenu.add_command(label="Open...", command=self.openFile,
                                  accelerator="Ctrl+O")
        self.fileMenu.add_command(label="Open Multiple...",
                                  command=self.openMultiple,
                                  accelerator="Ctrl+Shift+O")
        self.fileMenu.add_separator()
        self.fileMenu.add_cascade(label="Export as...", menu=self.exportMenu)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Exit", command=self.closeWindow,
                                  accelerator="Alt+F4")
        # Add the sub-menu to the menubar
        self.add_cascade(label="File", menu=self.fileMenu)

        # Create the format menu
        self.add_command(label="Format", command=self.format)

        # Create the lines menu
        self.linesMenu = tk.Menu(self, tearoff=False)
        # Bind the lines checkbuttons to the menu
        self.linesMenu.add_checkbutton(label="Reference Circle",
                                       command=self.updateGraph,
                                       variable=self.master.showRef)
        self.linesMenu.add_checkbutton(label="Base Circle",
                                       command=self.updateGraph,
                                       variable=self.master.showBase)
        self.linesMenu.add_checkbutton(label="Tip Circle",
                                       command=self.updateGraph,
                                       variable=self.master.showTip)
        self.linesMenu.add_checkbutton(label="Root Circle",
                                       command=self.updateGraph,
                                       variable=self.master.showRoot)
        self.linesMenu.add_checkbutton(label="Line of Centres",
                                       command=self.updateGraph,
                                       variable=self.master.showCentres)
        self.linesMenu.add_checkbutton(label="Line of Action",
                                       command=self.updateGraph,
                                       variable=self.master.showAction)
        self.linesMenu.add_checkbutton(label="Normal", command=self.updateGraph,
                                       variable=self.master.showNormal)

        # Create the points menu
        self.pointsMenu = tk.Menu(self, tearoff=False)
        # Bind the points checkbuttons to the menu
        self.pointsMenu.add_checkbutton(label="Centre Points",
                                        command=self.updateGraph,
                                        variable=self.master.showCentrePoints)
        self.pointsMenu.add_checkbutton(label="Pitch Point",
                                        command=self.updateGraph,
                                        variable=self.master.showPitchPoint)
        self.pointsMenu.add_checkbutton(label="Action Points",
                                        command=self.updateGraph,
                                        variable=self.master.showActionPoints)

        # Create the options menu
        # Create a sub-menu to go on the menubar
        self.optionsMenu = tk.Menu(self, tearoff=False)
        # Bind the options to the menu
        self.optionsMenu.add_cascade(label="Lines", menu=self.linesMenu)
        self.optionsMenu.add_cascade(label="Points", menu=self.pointsMenu)
        self.optionsMenu.add_checkbutton(label="Animation",
                                         command=self.updateAnimation,
                                         variable=self.master.animationOn,
                                         accelerator="Space")
        # Add the sub-menu to the menubar
        self.add_cascade(label="Options", menu=self.optionsMenu)
    
        # Add the key bindings
        self.master.bind("<Control-n>", self.newGear)
        self.master.bind("<Control-o>", self.openFile)
        self.master.bind("<Control-Shift-KeyPress-O>", self.openMultiple)
        self.master.bind("<Alt-F4>", self.closeWindow)
        self.master.bind("<Control-W>", self.closeWindow)
        self.master.bind("<space>", self.toggleAnimation)

    def newGear(self, *args, **kwargs):
        # Ask the user to input the gear parameters
        InputFrame(self.master, defaults={"alpha": 20, "backlash": 4,
                                          "addendum": 1, "dedendum": 1.25},
                   padx=7, pady=5)

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
            self.master.openFile(fileNames)

    def openMultiple(self, *args, **kwargs):
        self.openFile(multiple=True)

    def exportImage(self, *args, **kwargs):
        ExportImageFrame(padx=7, pady=5)

    def exportDXF(self, *args, **kwargs):
        ExportDXFFrame(padx=7, pady=5, defaults={"beta": 0})

    def closeWindow(self, *args, **kwargs):
        self.master.destroy()

    def format(self, *args, **kwargs):
        FormatFrame()

    def updateGraph(self, *args, **kwargs):
        self.master.updateGraph()

    def updateAnimation(self, *args, **kwargs):
        self.master.updateAnimation(animation=self.master.animationOn.get())

    def toggleAnimation(self, *args, **kwargs):
        self.master.updateAnimation(
            animation=(not self.master.animationOn.get()))
        
# If this program is being run directly this code will be executed
# If this program is being imported this code will not be executed
if __name__ == "__main__":
    if len(sys.argv) == 1:
        # Get a list of xls files in the data directory
        xlsFiles = listXls()

        fileNames = [xlsFiles[0]]
    elif len(sys.argv) == 2:
        fileNames = [sys.argv[1]]
    elif len(sys.argv) > 2:
        fileNames = [sys.argv[1], sys.argv[2]]
    else:
        fileNames = None
    
    # Create a new tkinter window
    root = GearGUI(fileNames=fileNames)
    
    # Run the window
    root.mainloop()
