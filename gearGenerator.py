import matplotlib.pyplot as plt
import math
import pickle
#import csv

def frange(start, end, step):
    if start < end:
        values = []
        total = start
        while total < end:
            values.append(total)
            total += step
        values.append(end)
        return values
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
    return rb / math.cos(alpha)

def pythagoras(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)    

def getDeltaTheta(r, s):
    return math.acos((2 * r**2 - s**2) / (2 * r**2))

def cartesian(r, theta):
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    return (x, y)

def points(r, alpha):
    if alpha > 0:
        x, y = cartesian(r, involute(alpha))
    else:
        x, y = cartesian(r, -involute(abs(alpha)))
    return (x, y)

def getPoints(rb, theta):
    a = rb * math.cos(theta)
    b = rb * math.sin(theta)
    x = a + math.sin(theta) * theta * rb
    y = b - math.cos(theta) * theta * rb
    return (x, y)

def rotate(point, theta, centre=(0, 0)):
    x = (point[0] - centre[0]) * math.cos(theta) - (point[1] - centre[1]) * math.sin(theta)
    y = (point[0] - centre[0]) * math.sin(theta) + (point[1] - centre[1]) * math.cos(theta)
    return (x, y)

def gearPoints(rb, R, n, gapRatio1, step):
    angle = 2 * math.pi / n
    gap1 = gapRatio1 * angle
    gap2 = angle - (2 * involute(getAlpha(R, rb))) - gap1
    print(gap1, gap2)

    x = []
    y = []
    
    for i in range(n):
        #Generate the leading curve
        for r in frange(rb, R, step):
            alpha = getAlpha(r, rb)
            point = points(r, alpha)
            point = rotate(point, (angle * i) + gap1)
            x.append(point[0])
            y.append(point[1])
        """
        #Generate the curve on top of the tooth
        for theta in frange((angle * i) + gap1 + involute(getAlpha(R, rb)), (angle * i) + involute(getAlpha(R, rb)) + gap2, getDeltaTheta(R, step)):
            point = cartesian(R, theta)
            x.append(point[0])
            y.append(point[1])"""
        
        #Generate the trailing curve
        for r in frange(R, rb, step):
            alpha = getAlpha(r, rb)
            point = points(r, -alpha)
            point = rotate(point, (angle * (i + 1)) - gap1)
            x.append(point[0])
            y.append(point[1])
        """
        #Generate the curve between the teeth
        for theta in frange((angle * (i + 1)) - gap1, (angle * (i + 1)) + gap1, getDeltaTheta(rb, step)):
            point = cartesian(rb, theta)
            x.append(point[0])
            y.append(point[1])"""

    x.append(x[0])
    y.append(y[0])

    return (x, y)

def circlePoints(r, step):
    x = []
    y = []

    for theta in frange(0, 2 * math.pi, getDeltaTheta(r, step)):
        point = cartesian(r, theta)
        x.append(point[0])
        y.append(point[1])

    return (x, y)

def convertPolar(x, y):
    a = []
    b = []
    for i in range(len(x)):
        a.append(math.sqrt(x[i]**2 + y[i]**2))
        b.append(math.atan(y[i] / x[i]))
    return (a, b)

def rotatePoints(points, theta, centre=(0, 0)):
    a = []
    b = []
    for p in points:
        point = rotate(p, theta, centre=centre)
        a.append(point[0])
        b.append(point[1])
    return list(zip(a, b))

def rotatePointList(x, y, theta, centre=(0, 0)):
    a = []
    b = []
    for i in range(len(x)):
        point = rotate((x[i], y[i]), theta, centre=centre)
        a.append(point[0])
        b.append(point[1])
    return (a, b)

def inside(point, centre, a, b):
    d = pythagoras(point, centre)
    try:
        theta = math.atan((point[1] - centre[1]) / (point[0] - centre[0]))
    except ZeroDivisionError:
        theta = math.atan((point[1] - centre[1]) / 0.0001)
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
    x = []
    y = []
    for point in gearPoints1:
        x.append(point[0])
        y.append(point[1])
        
    a, b = rotatePointList(x, y, angle1, centre=centre1)
    gearPoints2 = rotatePoints(gearPoints2, angle2, centre=centre2)
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

if __name__ == "__main__":
    lines = []

    rb = 1
    R = 1.19
    n = 20
    gapRatio1 = 0.16
    step = 0.05
    angle = 2 * math.pi / n

    x, y = gearPoints(rb, R, n, gapRatio1, step)

    data = [{"rb": rb, "R": R, "n": n, "angle": angle}]
    data = []
    data.extend(list(zip(x, y)))
    """
    for i in range(len(x)):
        data.append([x[i], y[i]])
    """

    with open("gearData2.pkl", "wb") as f:
        pickle.dump(data, f)

    """
    with open("gearData2.csv", "wb") as f:
        csvout = csv.writer(f, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)

        for item in data:
            print(item)
            csvout.writerow([item[0], item[1]])
    """

    """
    lines.append(circlePoints(rb, step))
    lines.append(circlePoints(R, step))

    for line in lines:
        plt.plot(line[0], line[1], color="blue")
    """

    print(len(x))

    a, b = convertPolar(x, y)
    pointsToCheck = [(1, 0)]
    import random
    for i in range(100):
        pointsToCheck.append((random.uniform(-2, 2), random.uniform(-2, 2)))

    for p in pointsToCheck:
        var = inside(p, (0, 0), a, b)
        if var == True:
            plt.plot(p[0], p[1], "go")
        if var == None:
            plt.plot(p[0], p[1], "yo")
        if var == False:
            plt.plot(p[0], p[1], "ro")

    plt.plot(x, y, color="red")
    plt.axis("equal")
    plt.show()
