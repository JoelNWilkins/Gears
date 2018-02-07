# Import required modules

# This imports the core functions for working with gears
# We do not have to import math etc. as this is done in gearCore
from gearCore import *
from gearGenerator import *

# Get a list of xls files in the data directory
xlsFiles = listXls()
path = os.getcwd() + "\\data"

print("XLS files in directory {}".format(path))

for i in range(len(xlsFiles)):
    print("{}: {}".format(i + 1, xlsFiles[i]))

run = True
while run:
    try:
        number1 = int(input("Enter the file number to open for gear 1: "))
        if number1 <= len(xlsFiles) and number1 > 0:
            run = False
    except:
        print("Invalid input.")

run = True
while run:
    try:
        number2 = int(input("Enter the file number to open for gear 2: "))
        if number2 <= len(xlsFiles) and number2 > 0:
            run = False
    except:
        print("Invalid input.")

# vpython is the module for 3D graphics
# vpython must be imported after the file has been chosen
from vpython import *

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
    # Set the text to appear under the window
    scene.caption = text

def textOut(text):
    # Add to the text to appear under the window
    scene.append_to_caption("\n" + text)

# Create a new scene and select it to be shown
scene = canvas(title="Gear simulation")
scene.select()

# A list of the items in the caption
captionText = []

# Load the gear data from an xls file
points1, parameters1 = readData(xlsFiles[number1-1])
points2, parameters2 = readData(xlsFiles[number2-1])

# Calculate the face width of the largest gear
if parameters1["z"] > parameters2["z"]:
    faceWidth = 0.1 * parameters1["r"]
else:
    faceWidth = 0.1 * parameters2["r"]

setCaption("Building gear 1...")
# Create a 2D profile of the gear
profile = shapes.points(pos=points1)
# extrusion is used to project a 2D shape to 3D
gear1 = extrusion(path=[vector(-faceWidth/2, 0, 0), vector(faceWidth/2, 0, 0)],
                  shape=profile, axis=vector(0, 0, 0))#, color=vector(255, 0, 0))
gear1.profile = profile
# Set the position of gear so the pitch point is at the origin
gear1.pos = vector(-parameters1["r"], 0, 0)
# Rotate the gear so that it faces the camera
gear1.rotate(angle=math.pi/2, axis=vector(0, 1, 0), origin=gear1.pos)
gear1.angle = 0

setCaption("Building gear 2...")
# Create a 2D profile of the gear
profile = shapes.points(pos=points2)
# extrusion is used to project a 2D shape to 3D
gear2 = extrusion(path=[vector(-faceWidth/2, 0, 0), vector(faceWidth/2, 0, 0)],
                  shape=profile, axis=vector(0, 0, 0))#, color=vector(0, 0, 255))
gear2.profile = profile
# Set the position of the gear so the pitch point is at the origin
gear2.pos = vector(parameters2["r"], 0, 0)
# Rotate the gear so that it faces the camera
gear2.rotate(angle=math.pi/2, axis=vector(0, 1, 0), origin=gear2.pos)
gear2.rotate(angle=math.pi, axis=vector(1, 0, 0), origin=gear2.pos)
gear2.rotate(angle=parameters2["angle"]/2, axis=gear2.axis, origin=gear2.pos)
gear2.angle = parameters2["angle"] / 2

# Clear the caption and create the speed control slider
setCaption("")
s = SpeedControl(min=0, max=0.1, value=0.01)

while True:
    # Rotate the gears depending on the speed
    gear1.rotate(angle=s.getSpeed(), axis=gear1.axis, origin=gear1.pos)
    gear2.rotate(angle=s.getSpeed() * parameters1["z"] / parameters2["z"],
                 axis=gear2.axis, origin=gear2.pos)
    gear1.angle += s.getSpeed()
    gear2.angle += s.getSpeed() * parameters1["z"] / parameters2["z"]

    # Slow down the program to avoid using too much CPU power
    rate(25)
