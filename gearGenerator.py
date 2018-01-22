# Import required modules

# matplotlib is the module to generate the graphs
import matplotlib.pyplot as plt
# math is the module to use trigonometric functions etc.
import math
# pickle is used to save the data to a file
# I may try to change this to a csv file which would be better
import pickle
import csv
import random

def frange(start, end, step):
    # A function to return a list of float values
    # between 2 points with a certain step

    # If start is smaller than end the values will be ascending
    if start < end:
        values = []
        total = start
        while total < end:
            values.append(total)
            total += step
        values.append(end)
        return values

    # If start is greater than end the values will be descending
    elif start > end:
        values = []
        total = start
        while total > end:
            values.append(total)
            total -= step
        values.append(end)
        return values

def involute(alpha):
    return math.tan(alpha) - alpha

def getAlpha(r, rb):
    return math.acos(rb / r)

def getR(rb, alpha):
    # This is a rearranged version of getAlpha
    return rb / math.cos(alpha)

def pythagoras(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)    

def getDeltaTheta(r, s):
    return math.acos((2 * r**2 - s**2) / (2 * r**2))

def cartesian(r, theta):
    # Converts polar coordinates to cartesian coordinates
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    return (x, y)

def convertPolar(x, y):
    # Converts a list of x and y values to polar form
    a = []
    b = []
    for i in range(len(x)):
        a.append(math.sqrt(x[i]**2 + y[i]**2))
        b.append(math.atan(y[i] / x[i]))
    return (a, b)

def points(r, alpha):
    # This generates the curved part of the tooth
    if alpha > 0:
        x, y = cartesian(r, involute(alpha))
    else:
        x, y = cartesian(r, -involute(abs(alpha)))
    return (x, y)

def getPoints(rb, theta):
    # This is a cartesian version of points and is less good
    a = rb * math.cos(theta)
    b = rb * math.sin(theta)
    x = a + math.sin(theta) * theta * rb
    y = b - math.cos(theta) * theta * rb
    return (x, y)

def rotate(point, theta, centre):
    # This can be used to rotate a point about a centre
    x = (point[0] - centre[0]) * math.cos(theta) - (point[1] - centre[1]) * math.sin(theta)
    y = (point[0] - centre[0]) * math.sin(theta) + (point[1] - centre[1]) * math.cos(theta)
    return (x, y)

def rotatePoints(points, theta, centre):
    # This implements the rotate function for a list of points
    a = []
    b = []
    for p in points:
        point = rotate(p, theta, centre)
        a.append(point[0])
        b.append(point[1])
    return list(zip(a, b))

def rotatePointList(x, y, theta, centre):
    # This implements the rotate function on a list of x and y values
    a = []
    b = []
    for i in range(len(x)):
        point = rotate((x[i], y[i]), theta, centre)
        a.append(point[0])
        b.append(point[1])
    return (a, b)

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
    lines = []

    rb = 1
    R = 1.19
    n = 20
    gapRatio1 = 0.16
    step = 0.01
    angle = 2 * math.pi / n

    x, y = gearPoints(rb, R, n, gapRatio1, step)

    # This adds a dictionary of the gear parameters
    data = [{"rb": rb, "R": R, "n": n, "angle": angle}]
    data = []
    # This adds the list of x and y values in coordinate form
    data.extend(list(zip(x, y)))

    # This writes the gear points to a csv file to be read by the gearModel
    with open("gearData.csv", "w", newline="") as f:
        csvwriter = csv.writer(f, delimiter=",")

        for item in data:
            csvwriter.writerow([item[0], item[1]])

    # This writes the gear parameters to a csv file to be read by the gearModel
    with open("gearParameters.csv", "w", newline="") as f:
        csvwriter = csv.writer(f, delimiter=",")

        csvwriter.writerow(["rb", rb])
        csvwriter.writerow(["R", R])
        csvwriter.writerow(["n", n])
        csvwriter.writerow(["angle", angle])

    # This will draw 2 circles with radius rb and R
    # Uncomment this if you want to see how the gear lies on these circles
    """
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

    # This will draw the gear on a graph
    plt.plot(x, y, color="red")
    # The equal means that the graph will not be distorted
    plt.axis("equal")
    plt.show()
