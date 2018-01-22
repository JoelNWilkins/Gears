# Import required modules

# vpython is the module for 3D graphics
from vpython import *
# math is the module to use trigonometric functions etc.
import math
# csv is the module used to read and write to csv files
import csv
# This imports functions from the gear generating program
from gearGenerator import *

class SpeedControl(slider):
    # A class to control the slider which changes the gear speed
    
    def __init__(self, *args, **kwargs):
        # Initiate the slider object
        super().__init__(bind=self.updateSpeed, *args, **kwargs)

    def updateSpeed(self):
        # Does nothing but required as the slider needs a binding
        pass

    def getSpeed(self):
        # Returns the value of the slider
        return self.value

def setCaption(text):
    scene.caption = text

def textOut(text):
    scene.append_to_caption("\n" + text)

# Create a new scene and select it to be shown
scene = canvas(title="Gear simulation")
scene.select()

# A list of the items in the caption
captionText = []

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

# Create a 2D profile of the gear
gearProfile = shapes.points(pos=data)

# extrusion is used to project a 2D shape to 3D
# Rotate the gears so that they face the camera
setCaption("Building gear 1...")
gear1 = extrusion(path=[vector(-0.05, 0, 0), vector(0.05, 0, 0)], shape=gearProfile, axis=vector(0, 0, 0))
gear1.pos = vector(-1.1, 0, 0)
gear1.rotate(angle=math.pi/2, axis=vector(0, 1, 0), origin=gear1.pos)

setCaption("Building gear 2...")
gear2 = extrusion(path=[vector(-0.05, 0, 0), vector(0.05, 0, 0)], shape=gearProfile, axis=vector(0, 0, 0))
gear2.pos = vector(1.1, 0, 0)
gear2.rotate(angle=math.pi/2, axis=vector(0, 1, 0), origin=gear2.pos)
gear2.rotate(angle=math.pi, axis=vector(1, 0, 0), origin=gear2.pos)
gear2.rotate(angle=parameters["angle"]/2, axis=gear2.axis, origin=gear2.pos)

# Clear the caption and create the speed control slider
setCaption("")
s = SpeedControl(min=0, max=0.1, value=0.01)

while True:
    # Rotate the gears depending on the speed
    gear1.rotate(angle=s.getSpeed(), axis=gear1.axis, origin=gear1.pos)
    gear2.rotate(angle=s.getSpeed(), axis=gear2.axis, origin=gear2.pos)
    
    # Slow down the program to avoid using too much CPU power
    rate(25)
