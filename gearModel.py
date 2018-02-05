# Import required modules

# This imports the core functions for working with gears
# We do not have to import csv, math etc. as this is done in gearCore
from gearCore import *
from gearGenerator import *

# Create a list of all the files in the data directory
path = os.getcwd() + "\\data"
files = os.listdir(path)

# Find the files with a .csv file extension
csvFiles = []
for file in files:
    if file.split(".")[-1] == "csv" and "Data" in file:
        csvFiles.append(file)

print("CSV files in directory {}".format(path))

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

# Get the number of the file to open
fileToOpen = csvFiles[number - 1]
fileNumber = fileToOpen.split(".")[-2].split("gearData")[-1]


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
    scene.caption = text

def textOut(text):
    scene.append_to_caption("\n" + text)

# Create a new scene and select it to be shown
scene = canvas(title="Gear simulation")
scene.select()

# A list of the items in the caption
captionText = []

# Load the gear points from a csv file
data = readDataFromCSV(path + "\\gearData{}.csv".format(fileNumber))

# Load the parameters from a csv file
parameters = readParametersFromCSV(path + "\\gearParameters{}.csv".format(fileNumber))

# Create a 2D profile of the gear
gearProfile = shapes.points(pos=data)

# extrusion is used to project a 2D shape to 3D
# Rotate the gears so that they face the camera
setCaption("Building gear 1...")
gear1 = extrusion(path=[vector(-0.05, 0, 0), vector(0.05, 0, 0)], shape=gearProfile, axis=vector(0, 0, 0))
gear1.pos = vector(-1.1, 0, 0)
gear1.rotate(angle=math.pi/2, axis=vector(0, 1, 0), origin=gear1.pos)
gear1.angle = 0

setCaption("Building gear 2...")
gear2 = extrusion(path=[vector(-0.05, 0, 0), vector(0.05, 0, 0)], shape=gearProfile, axis=vector(0, 0, 0))
gear2.pos = vector(1.1, 0, 0)
gear2.rotate(angle=math.pi/2, axis=vector(0, 1, 0), origin=gear2.pos)
gear2.rotate(angle=math.pi, axis=vector(1, 0, 0), origin=gear2.pos)
gear2.rotate(angle=parameters["angle"]/2, axis=gear2.axis, origin=gear2.pos)
gear2.angle = parameters["angle"] / 2

gearProfile1 = []
for point in data:
    gearProfile1.append([point[0] + gear1.pos.x, point[1] + gear1.pos.y])

gearProfile2 = []
for point in data:
    gearProfile2.append([point[0] + gear2.pos.x, point[1] + gear2.pos.y])

# Clear the caption and create the speed control slider
setCaption("")
s = SpeedControl(min=0, max=0.1, value=0.01)

while True:
    # Rotate the gears depending on the speed
    gear1.rotate(angle=s.getSpeed(), axis=gear1.axis, origin=gear1.pos)
    gear2.rotate(angle=s.getSpeed(), axis=gear2.axis, origin=gear2.pos)
    gear1.angle += s.getSpeed()
    gear2.angle += s.getSpeed()

    var = intersecting(gearPoints1=gearProfile1, centre1=[gear1.pos.x, gear1.pos.y], angle1=gear1.angle,
                       gearPoints2=gearProfile2, centre2=[gear2.pos.x, gear2.pos.y], angle2=gear2.angle)
    
    # Slow down the program to avoid using too much CPU power
    rate(25)
