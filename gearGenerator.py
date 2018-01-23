# Import required modules

# This imports the core functions for working with gears
# We do not have to import csv, math etc. as this is done in gearCore
from gearCore import *
# Also import the gearViewer program to display what the gear looks like
from gearViewer import *
from tkinter import ttk
import random

class InputFrame(tk.Frame):
    # A frame containing the input fields for the parameters

    def __init__(self, root):
        # Create a frame in the root window
        tk.Frame.__init__(self, root)

        # Save the root for later use
        self.root = root

        label = tk.Label(self, text="""This is where the user would input values to generate the gear.
The user would also be able to press generate on this page.
I need to add a save option to the file menu to save the data.""")
        label.pack()

        """
        label1 = tk.Text(self, width=5, height=2, borderwidth=0, background=self.cget("background"))
        label1.tag_configure("subscript", offset=-4)
        label1.insert("insert", "r", "", "b", "subscript", ":")
        label1.configure(state="disabled")
        label1.grid(row=0, column=0, sticky="e")
        entry1 = tk.Entry(self)
        entry1.grid(row=0, column=1, sticky="n")
        """

def gearPoints(rb, R, n, gapRatio1, step):
    # This is the main function to generate a gear
    # The 2nd and 4th sections may have to be commented out
    # if the gear is being used in the 3D model
    # Including them can cause the model to not run
    
    angle = 2 * math.pi / n
    # gap1 is the angle of the gap between the teeth
    gap1 = gapRatio1 * angle
    # gap2 is the angle of the top of the tooth
    gap2 = angle - (2 * involute(getAlpha(R, rb))) - gap1

    x = []
    y = []
    for i in range(n):
        # Generate the leading curve
        for r in frange(rb, R, step):
            alpha = getAlpha(r, rb)
            point = points(r, alpha)
            point = rotate(point, (angle * i) + gap1, (0, 0))
            x.append(point[0])
            y.append(point[1])
        """
        # Generate the curve on top of the tooth
        for theta in frange((angle * i) + gap1 + involute(getAlpha(R, rb)), (angle * i) + involute(getAlpha(R, rb)) + gap2, getDeltaTheta(R, step)):
            point = cartesian(R, theta)
            x.append(point[0])
            y.append(point[1])"""
        
        # Generate the trailing curve
        for r in frange(R, rb, step):
            alpha = getAlpha(r, rb)
            point = points(r, -alpha)
            point = rotate(point, (angle * (i + 1)) - gap1, (0, 0))
            x.append(point[0])
            y.append(point[1])
        """
        # Generate the curve between the teeth
        for theta in frange((angle * (i + 1)) - gap1, (angle * (i + 1)) + gap1, getDeltaTheta(rb, step)):
            point = cartesian(rb, theta)
            x.append(point[0])
            y.append(point[1])"""

    # Add the first values to the end to make the gear meet up
    x.append(x[0])
    y.append(y[0])
    return (x, y)

def circlePoints(r, step):
    # This function will return a list of points for a circle of radius r
    x = []
    y = []
    for theta in frange(0, 2 * math.pi, getDeltaTheta(r, step)):
        point = cartesian(r, theta)
        x.append(point[0])
        y.append(point[1])
    return (x, y)

def inside(point, centre, a, b):
    # This function works out if a point is inside a gear
    d = pythagoras(point, centre)
    try:
        theta = math.atan((point[1] - centre[1]) / (point[0] - centre[0]))
    except ZeroDivisionError:
        # An exception for if the point has the same x value as the centre
        theta = math.pi / 2
    diff = []
    for item in b:
        diff.append(abs(item - theta))
    i = diff.index(min(diff))
    if round(d, 3) < round(a[i], 3):
        return True
    elif round(d, 3) == round(a[i], 3):
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
    # Set the parameters to generate the gear
    rb = 1
    R = 1.19
    n = 20
    gapRatio1 = 0.16
    step = 0.01
    angle = 2 * math.pi / n

    # Generate the gear from the parameters
    x, y = gearPoints(rb, R, n, gapRatio1, step)

    # This adds the list of x and y values in coordinate form
    data = list(zip(x, y))

    # This creates a dictionary of the gear parameters
    parameters = {"rb": rb, "R": R, "n": n, "angle": angle}

    run = True
    while run:
        number = int(input("Enter the file number to save as: "))
        if type(number) == int:
            run = False

    # This writes the gear points to a csv file to be read by the gearModel
    fileName = "data\\gearData{}.csv".format(number)
    saveDataToCSV(fileName, data)

    # This writes the gear parameters to a csv file to be read by the gearModel
    saveParametersToCSV("data\\gearParameters{}.csv".format(number), parameters)

    # This will draw 2 circles with radius rb and R
    # Uncomment this if you want to see how the gear lies on these circles
    """
    lines = []
    lines.append(circlePoints(rb, step))
    lines.append(circlePoints(R, step))

    for line in lines:
        plt.plot(line[0], line[1], color="blue")
    """
    
    # Generate some random points and test if they are inside the gear
    # This is to test the inside function
    """
    a, b = convertPolar(x, y)
    pointsToCheck = [(1, 0), (0, 1)]
    for i in range(100):
        pointsToCheck.append((random.uniform(-2, 2), random.uniform(-2, 2)))

    for p in pointsToCheck:
        var = inside(p, (0, 0), a, b)
        if var == True:
            # The point will be green if it is inside
            plt.plot(p[0], p[1], "go")
        if var == None:
            # The point will be yellow if it is just touching the gear
            plt.plot(p[0], p[1], "yo")
        if var == False:
            # The point will be red if it is outside the gear
            plt.plot(p[0], p[1], "ro")
    """

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
    frame2 = GraphFrame(root, fileName=fileName)
    notebook.add(frame2, text="Viewer")
    menubar = MenuBar(root, frame2)
    # Run the window
    root.mainloop()
