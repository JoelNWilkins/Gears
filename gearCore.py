# Import required modules

# math is the module to use trigonometric functions etc.
import math
# csv is the module used to read and write to csv files
import csv
# xlrd and xlwt are the excel workbook reader and writer modules
import xlrd
import xlwt

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
    # This function generates the curve for the tooth
    return math.tan(alpha) - alpha

def getAlpha(r_b, r):
    # This finds the angle to input into the involute function
    return math.acos(r_b / r)

def getR(r_b, alpha):
    # This is a rearranged version of getAlpha
    return r_b / math.cos(alpha)

def getDistance(point1, point2):
    # This uses pythagoras' theorem to find the distance between 2 points
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)    

def getDeltaTheta(r, s):
    # This finds the angle between points on the curve
    return math.acos((2 * r**2 - s**2) / (2 * r**2))

def getCartesian(r, theta):
    # Converts polar coordinates to cartesian coordinates
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    return (x, y)

def getPolar(x, y):
    # Converts cartesian coordinates to polar coordinates
    r = math.sqrt(x**2 + y**2)
    theta = math.atan(y / x)
    return (r, theta)

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
        x, y = getCartesian(r, involute(alpha))
    else:
        x, y = getCartesian(r, -involute(abs(alpha)))
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

def circlePoints(r, step):
    # This function will return a list of points for a circle of radius r
    x = []
    y = []
    for theta in frange(0, 2 * math.pi, getDeltaTheta(r, step)):
        point = getCartesian(r, theta)
        x.append(point[0])
        y.append(point[1])
    return (x, y)

def calculateParameters(z, alpha, m):
    d = m * z
    r = d / 2
    d_b = d * math.cos(math.radians(alpha))
    r_b = d_b / 2
    h_a = m
    h_f = 1.25 * m
    h = h_a + h_f
    c = h - 2 * h_a
    h_w = h - c
    r_a = r + h_a
    d_a = 2 * r_a
    r_f = r - h_f
    d_f = 2 * r_f
    p = math.pi * m
    p_b = p * math.cos(math.radians(alpha))
    s = p / 2
    s_b = p_b / 2
    angle = 2 * math.pi / z

    parameters = {"z": z, "alpha": alpha, "m": m, "d": d, "r": r, "d_b": d_b,
                  "r_b": r_b, "h_a": h_a, "h_f": h_f, "h": h, "c": c,
                  "h_w": h_w, "r_a": r_a, "d_a": d_a, "r_f": r_f, "d_f": d_f,
                  "p": p, "p_b": p_b, "s": s, "s_b": s_b, "angle": angle}

    return parameters

def readData(fileName):
    # Read from an xls file
    # Open the file as a workbook
    workbook = xlrd.open_workbook(fileName)

    # Open the 2 sheets containing the data
    pointsSheet = workbook.sheet_by_name("Points")
    parametersSheet = workbook.sheet_by_name("Parameters")

    # Iterate through the points and add them to a list of x and y values
    points = []
    for row in range(pointsSheet.nrows):
        points.append([])
        points[row].append(pointsSheet.cell(row, 0).value)
        points[row].append(pointsSheet.cell(row, 1).value)

    # Iterate through the parameters and create a dictionary of parameters
    parameters = {}
    for row in range(parametersSheet.nrows):
        parameters[parametersSheet.cell(row, 0).value] = parametersSheet.cell(row, 1).value

    return points, parameters

def writeData(fileName, points, parameters):
    # Write to an xls file
    # Create a new workbook
    workbook = xlwt.Workbook()

    # Add the 2 sheets to contain the data
    pointsSheet = workbook.add_sheet("Points")
    parametersSheet = workbook.add_sheet("Parameters")

    # Iterate through the points and add them to the points sheet
    for i in range(len(points)):
        pointsSheet.write(i, 0, points[i][0])
        pointsSheet.write(i, 1, points[i][1])

    # Iterate through the parameters and add them to the parameters sheet
    i = 0
    for key in parameters.keys():
        parametersSheet.write(i, 0, key)
        parametersSheet.write(i, 1, parameters[key])
        i += 1

    # Save the workbook to a file
    workbook.save(fileName)

if __name__ == "__main__":
    print("This module is intended to be imported and not run directly.")
