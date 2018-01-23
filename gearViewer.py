# Import required modules

# This imports the core functions for working with gears
# We do not have to import csv, math etc. as this is done in gearCore
from gearCore import *
# matplotlib is the module to generate the graphs
import matplotlib.pyplot as plt
import os

# Create a list of all the files in the current directory
files = os.listdir()

# Find the files with a .csv file extension
csvFiles = []
for file in files:
    if file.split(".")[-1] == "csv" and "Data" in file:
        csvFiles.append(file)

print("CSV files in directory {}".format(os.getcwd()))

for i in range(len(csvFiles)):
    print("{}: {}".format(i + 1, csvFiles[i]))

run = True
while run:
    try:
        number = int(input("Enter the file number to open: "))
        if number <= len(csvFiles) and number > 0:
            run = False
    except:
        print("Invalid input.")

# Load the gear points from a csv file
data = readDataFromCSV(csvFiles[number - 1])

x = []
y = []
for item in data:
    x.append(item[0])
    y.append(item[1])

# This will draw the gear on a graph
plt.plot(x, y, color="red")
# The equal means that the graph will not be distorted
plt.axis("equal")
plt.title(csvFiles[number - 1])
plt.show()
