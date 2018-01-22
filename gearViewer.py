# Import required modules

# matplotlib is the module to generate the graphs
import matplotlib.pyplot as plt
# math is the module to use trigonometric functions etc.
import math
# csv is the module used to read and write to csv files
import csv
# This imports functions from the gear generating program
from gearGenerator import *

# Load the gear points from a csv file
data = []
with open("gearData.csv", "r", newline="") as f:
    csvreader = csv.reader(f, delimiter=",")

    for row in csvreader:
        data.append([])
        for cell in row:
            data[-1].append(float(cell))

# Load the parameters from a csv file
parameters = {}
with open("gearParameters.csv", "r", newline="") as f:
    csvreader = csv.reader(f, delimiter=",")

    intValues = ["n"]
    for row in csvreader:
        if row[0] in intValues:
            parameters[row[0]] = int(row[1])
        else:
            parameters[row[0]] = float(row[1])

x = []
y = []
for item in data:
    x.append(item[0])
    y.append(item[1])

# This will draw the gear on a graph
plt.plot(x, y, color="red")
# The equal means that the graph will not be distorted
plt.axis("equal")
plt.show()
