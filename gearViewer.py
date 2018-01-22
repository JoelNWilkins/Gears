# Import required modules

# matplotlib is the module to generate the graphs
import matplotlib.pyplot as plt
# This imports the core functions for working with gears
# We do not have to import csv, math etc. as this is done in gearCore
from gearCore import *

# Load the gear points from a csv file
data = readDataFromCSV("gearData.csv")

# Load the parameters from a csv file
parameters = readParametersFromCSV("gearParameters.csv")

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
