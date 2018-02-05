# Import required modules

# This imports the core functions for working with gears
# We do not have to import csv, math etc. as this is done in gearCore
from gearCore import *
# Also import the gearViewer program to display what the gear looks like
from gearViewer import *

class InputFrame(tk.Frame):
    # A frame containing the input fields for the parameters

    def __init__(self, root):
        # Create a frame in the root window
        tk.Frame.__init__(self, root)

        # Save the root for later use
        self.root = root

        # Create labels and entries for the input parameters
        self.label1 = tk.Label(self, text="Number of teeth: ")
        self.label1.grid(row=0, column=0, sticky="e")
        self.entry1 = tk.Entry(self)
        self.entry1.grid(row=0, column=1, sticky="w")
        self.label2 = tk.Label(self, text="Pressure angle: ")
        self.label2.grid(row=1, column=0, sticky="e")
        self.entry2 = tk.Entry(self)
        self.entry2.grid(row=1, column=1, sticky="w")
        self.label3 = tk.Label(self, text="Module: ")
        self.label3.grid(row=2, column=0, sticky="e")
        self.entry3 = tk.Entry(self)
        self.entry3.grid(row=2, column=1, sticky="w")

        # Create a button to generate the gear
        self.button = tk.Button(self, text="Generate gear", command=self.generateGear)
        self.button.grid(row=3, column=0)

    def generateGear(self, *args, **kwargs):
        # Read the values from the entries
        z = int(self.entry1.get())
        alpha = float(self.entry2.get())
        m = float(self.entry3.get())

        # Calculate the parameters for the gear
        parameters = calculateParameters(z, alpha, m)

        # Calculate the points on the gear
        # The 0.16 value should be replaced with a variable
        x, y = gearPoints(parameters["r_b"], parameters["r_a"], parameters["z"],
                          parameters["p"], 0.01)

        # This adds the list of x and y values in coordinate form
        points = list(zip(x, y))

        # Ask the user to select the file name to save as
        fileName = asksaveasfilename(initialdir="data", filetypes=[("Excel 97-2003 Workbook","*.xls")], defaultextension=".csv")
        # Save the gear points to a csv file
        writeData(fileName, points, parameters)

def gearPoints(r_b, r_a, z, gapRatio1, step):
    # This is the main function to generate a gear
    # The 2nd and 4th sections may have to be commented out
    # if the gear is being used in the 3D model
    # Including them can cause the model to not run
    
    angle = 2 * math.pi / z
    # gap1 is the angle of the gap between the teeth
    gap1 = gapRatio1 * angle
    # gap2 is the angle of the top of the tooth
    gap2 = angle - (2 * involute(getAlpha(r_b, r_a))) - gap1

    x = []
    y = []
    for i in range(z):
        # Generate the leading curve
        for r in frange(r_b, r_a, step):
            alpha = getAlpha(r_b, r)
            point = points(r, alpha)
            point = rotate(point, (angle * i) + gap1, (0, 0))
            x.append(point[0])
            y.append(point[1])
        """
        # Generate the curve on top of the tooth
        for theta in frange((angle * i) + gap1 + involute(getAlpha(r_b, r_a)), (angle * i) + involute(getAlpha(r_b, r_a)) + gap2, getDeltaTheta(r_a, step)):
            point = cartesian(r_a, theta)
            x.append(point[0])
            y.append(point[1])"""
        
        # Generate the trailing curve
        for r in frange(r_a, r_b, step):
            alpha = getAlpha(r_b, r)
            point = points(r, -alpha)
            point = rotate(point, (angle * (i + 1)) - gap1, (0, 0))
            x.append(point[0])
            y.append(point[1])
        """
        # Generate the curve between the teeth
        for theta in frange((angle * (i + 1)) - gap1, (angle * (i + 1)) + gap1, getDeltaTheta(r_b, step)):
            point = cartesian(r_b, theta)
            x.append(point[0])
            y.append(point[1])"""

    # Add the first values to the end to make the gear meet up
    x.append(x[0])
    y.append(y[0])
    return (x, y)

def inside(point, centre, a, b):
    # This function works out if a point is inside a gear
    d = getDistance(point, centre)
    try:
        theta = math.atan((point[1] - centre[1]) / (point[0] - centre[0]))
    except ZeroDivisionError:
        # An exception for if the point has the same x value as the centre
        theta = math.pi / 2
    diff = []
    for item in b:
        diff.append(abs(item - theta))
    i = diff.index(min(diff))
    if d < a[i]:
        return True
    elif d == a[i]:
        return True
    else:
        return False

def intersecting(gearPoints1, centre1, angle1, gearPoints2, centre2, angle2):
    # This function tries to determine if 2 gears intersect or are touching
    x = []
    y = []
    for point in gearPoints1:
        x.append(point[0])
        y.append(point[1])
        
    a, b = rotatePointList(x, y, angle1, centre1)
    gearPoints2 = rotatePoints(gearPoints2, angle2, centre2)
    for point in gearPoints2:
        var = inside(point, centre1, a, b)
        if var == True:
            plt.plot(point[0], point[1], "ro")
            #return True
        else:
            plt.plot(point[0], point[1], "go")
            #pass
    plt.show()
    #return False

# If this program is being run directly this code will be executed
# If this program is being imported this code will not be executed
if __name__ == "__main__":
    # Create a list of all the files in the data directory
    path = os.getcwd() + "\\data"
    files = os.listdir(path)

    # Find the files with a .xls file extension
    xlsFiles = []
    for file in files:
        if file.split(".")[-1] == "xls":
            xlsFiles.append(path + "\\" + file)

    # This is for if no xls files are found
    if len(xlsFiles) == 0:
        xlsFiles.append(None)

    # Create a new tkinter window
    root = tk.Tk()
    root.title("Gear Generator")
    # Add notebook to manage different pages
    notebook = ttk.Notebook(root)
    notebook.pack()
    # Add the InputFrame
    frame1 = InputFrame(root)
    notebook.add(frame1, text="Generator")
    # Add the GraphFrame and MenuBar objects
    frame2 = GraphFrame(root, fileName=xlsFiles[0])
    notebook.add(frame2, text="Viewer")
    menubar = MenuBar(root, frame2)
    # Run the window
    root.mainloop()
