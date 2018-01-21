from vpython import *
import math
import pickle
from gearGenerator import *

class SpeedControl(slider):
    def __init__(self, *args, **kwargs):
        super().__init__(bind=self.updateSpeed, *args, **kwargs)

    def updateSpeed(self):
        pass

    def getSpeed(self):
        return self.value

def setCaption(text):
    scene.caption = text

def textOut(text):
    scene.append_to_caption("\n" + text)

scene = canvas(title="Gear simulation")
scene.select()

captionText = []

with open("gearData2.pkl", "rb") as f:
    data = pickle.load(f)

parameters = data[0]
data = data[1:]

gearProfile = shapes.points(pos=data)

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

setCaption("")
s = SpeedControl(min=0, max=0.1, value=0.01)

while True:
    gear1.rotate(angle=s.getSpeed(), axis=gear1.axis, origin=gear1.pos)
    gear2.rotate(angle=s.getSpeed(), axis=gear2.axis, origin=gear2.pos)
    
    rate(25)
