# Import required modules

# math is the module to use trigonometric functions etc.
import math
# csv is the module used to read and write to csv files
import csv

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

def saveDataToCSV(fileName, data):
    # This writes the gear points to a csv file to be read by the gearModel
    try:
        with open(fileName, "w", newline="") as f:
            csvwriter = csv.writer(f, delimiter=",")

            for item in data:
                csvwriter.writerow([item[0], item[1]])
    except PermissionError:
        print("{} is already open, please close the file to run the program.".format(fileName))

def saveParametersToCSV(fileName, parameters):
    # This writes the gear parameters to a csv file to be read by the gearModel
    try:
        with open(fileName, "w", newline="") as f:
            csvwriter = csv.writer(f, delimiter=",")

            for key in parameters.keys():
                csvwriter.writerow([key, parameters[key]])
    except PermissionError:
        print("{} is already open, please close the file to run the program.".format(fileName))

def readDataFromCSV(fileName):
    # Load the gear points from a csv file
    try:
        data = []
        with open(fileName, "r", newline="") as f:
            csvreader = csv.reader(f, delimiter=",")

            for row in csvreader:
                data.append([])
                for cell in row:
                    data[-1].append(float(cell))
        return data
    except PermissionError:
        print("{} is already open, please close the file to run the program.".format(fileName))

def readParametersFromCSV(fileName):
    # Load the parameters from a csv file
    try:
        parameters = {}
        with open(fileName, "r", newline="") as f:
            csvreader = csv.reader(f, delimiter=",")

            intValues = ["n"]
            for row in csvreader:
                if row[0] in intValues:
                    parameters[row[0]] = int(row[1])
                else:
                    parameters[row[0]] = float(row[1])
        return parameters
    except PermissionError:
        print("{} is already open, please close the file to run the program.".format(fileName))

if __name__ == "__main__":
    print("This module is intended to be imported and not run directly.")
