from gearCore import *
import os
import numpy
from matplotlib import pyplot as plt

path = os.getcwd()+"\\data\\"
files = os.listdir(path)

count = 1
for file in files:
    print("{}: {}".format(count, file.split("\\")[-1]))
    count += 1

print()

filename1 = files[int(input("Gear 1: "))-1]
filename2 = files[int(input("Gear 2: "))-1]

percentage = float(input("\nPercentage distance: ")) / 100

points1, parameters1 = readData(path+filename1)
points2, parameters2 = readData(path+filename2)
points2 = rotatePoints(points2, parameters2["angle"]/2
                       - parameters2["j_t"]/parameters2["r"], (0, 0))

centre1 = (-parameters1["r"], 0)
centre2 = (parameters2["r"], 0)

points1 = list(map(lambda x: [x[0]+centre1[0], x[1]+centre1[1]], points1))
points2 = list(map(lambda x: [x[0]+centre2[0], x[1]+centre2[1]], points2))

# Calculate the points on the line of action
xa = []
ya = []

angle = ((numpy.pi / 2) - numpy.radians(parameters2["alpha"])
         - numpy.arcsin(parameters2["r"]
         * numpy.sin(numpy.radians(parameters2["alpha"])
         + numpy.pi / 2) / parameters2["r_a"]))
l = numpy.sqrt(parameters2["r_a"]**2 + parameters2["r"]**2
              - 2 * parameters2["r_a"] * parameters2["r"]
              * numpy.cos(angle))

xa.append(l * numpy.cos(numpy.radians(parameters1["alpha"])
                       + numpy.pi / 2))
ya.append(l * numpy.sin(numpy.radians(parameters1["alpha"])
                       + numpy.pi / 2))

angle = ((numpy.pi / 2) - numpy.radians(parameters1["alpha"])
         - numpy.arcsin(parameters1["r"]
         * numpy.sin(numpy.radians(parameters1["alpha"])
         + numpy.pi / 2) / parameters1["r_a"]))
l = numpy.sqrt(parameters1["r_a"]**2 + parameters1["r"]**2
              - 2 * parameters1["r_a"] * parameters1["r"]
              * numpy.cos(angle))

xa.append(l * numpy.cos(numpy.radians(parameters2["alpha"])
                       - numpy.pi / 2))
ya.append(l * numpy.sin(numpy.radians(parameters2["alpha"])
                       - numpy.pi / 2))

ratio = parameters1["z"] / parameters2["z"]
alpha = numpy.radians(parameters1["alpha"])

angles = numpy.linspace(0, 360, 180)
contactPoints = []

for a in angles:
    angle = numpy.radians(a)
    
    p1 = rotatePoints(points1, -angle, centre1)
    p2 = rotatePoints(points2, angle*ratio, centre2)

    inter1 = []
    for i in range(len(p1)-1):
        if p1[i][0] > 1.25*xa[0] and p1[i][0] < 1.25*xa[1] and p1[i][1] < 1.25*ya[0] and p1[i][1] > 1.25*ya[1]:
            y1 = p1[i][1] - (p1[i][0] * numpy.tan(numpy.pi/2+alpha))
            y2 = p1[i+1][1] - (p1[i+1][0] * numpy.tan(numpy.pi/2+alpha))
            sign = numpy.sign([y1, y2])
            if -1 in sign and 1 in sign:
                inter1.append(p1[i])

    inter2 = []
    for i in range(len(p2)-1):
        if p2[i][0] > 1.25*xa[0] and p2[i][0] < 1.25*xa[1] and p2[i][1] < 1.25*ya[0] and p2[i][1] > 1.25*ya[1]:
            y1 = p2[i][1] - (p2[i][0] * numpy.tan(numpy.pi/2+alpha))
            y2 = p2[i+1][1] - (p2[i+1][0] * numpy.tan(numpy.pi/2+alpha))
            sign = numpy.sign([y1, y2])
            if -1 in sign and 1 in sign:
                inter2.append(p2[i])

    contact = 0
    for p in inter1:
        for q in inter2:
            d = numpy.sqrt((p[0] - q[0])**2 + (p[1] - q[1])**2)
            #print(d/parameters1["r"])
            if (2* d) / (parameters1["r"] + parameters2["r"]) < percentage:
                contact += 1
            
    contactPoints.append(contact)

##x1, y1 = zip(*p1)
##plt.plot(x1, y1, "r")
##
##x2, y2 = zip(*p2)
##plt.plot(x2, y2, "r")
##
##x3 = numpy.linspace(1.25*xa[0], 1.25*xa[1], 100)
##y3 = x3 * numpy.tan(numpy.pi/2+alpha)
##plt.plot(x3, y3, "g")
##
##for point in inter1:
##    plt.plot(*point, "bo")
##
##for point in inter2:
##    plt.plot(*point, "bo")
##
##plt.axis("equal")
##plt.show()

print("Average number of contact points: {}".format(numpy.mean(contactPoints)))

plt.plot(angles, contactPoints)
plt.xlabel(u"Angle of Rotation (\u00B0)")
plt.ylabel("Number of Contact Points")
plt.title("{} and {}".format(filename1.replace(".xls", ""), filename2.replace(".xls", "")))
plt.title("Contact Ratio of {} and {} Tooth Gears".format(int(parameters1["z"]), int(parameters2["z"])))
plt.xticks(numpy.linspace(0, 360, 9))
plt.yticks(numpy.arange(min(contactPoints), max(contactPoints)+1, 1))
plt.show()
