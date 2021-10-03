# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from numpy import double
from p5 import *

import math
import numpy as np
import matplotlib.pyplot as plt

from reader import ObjLoader
from renderer import AsteroidRenderer


# global variables
rend = AsteroidRenderer()
ol = ObjLoader()
intensityArray: float = []
phasePoints: float = []
magPoints: float = []

bg = Color(140, 128, 255)
width = 800
height = 800

def setup():
    size(width, height)



    print("Welcome to Potato Asteroid Light Curve Application (PALCA)! \n (c) 2021 U. Vasylyshin, E. Dudka, O. Lukina, A. Sportko, M. Tatarovsky, G. Titov \n It is a tool to visualize how an asteriod would reflect light under given circumstances!\n");
    q=input("Do you want to define custom input? (Y/N)")
    if q.__eq__("Y") or q.__eq__("y"):
        rend.asteroidAlbedo = float(input("Please input: 1) Asteroid albedo (from 0 to 1) = "));
        rend.sunAstDistance = float(input("\nPlease input: 2) Distance between the light source and the asteroid (in AU) = "));
        rend.astCamDistance = float(input("\nPlease input: 3) Distance between the asteroid and the camera (in AU) = "));
        rend.solarLuminosity = float(input("\nPlease input: 4) Solar luminosity (in solar luminosity units) = "));
        x = float(input("\nPlease input: 5.1) Light direction as a vector (please input x value) = "));
        y = float(input("\nPlease input: 5.2) Light direction as a vector (please input y value) = "));
        z = float(input("\nPlease input: 5.3) Light direction as a vector (please input z value) = "));
        rend.emissionDirRaw = [x, y, z];
    PathToFile = input("Please input: Path to .obj file (expected scale - polygons defined in km) = ");
    ol.loadObj(PathToFile)

def toMagnitude(efSurf):
    return (-2.5*log(rend.solarLuminosity*efSurf/((rend.sunAstDistance*rend.astCamDistance)**2),10)+15.5)


def draw():


    fill(bg)
    rect(0, 0, width, height)
    with push_matrix():

        translate(width/2, height/2)
        no_stroke()
        rend.render(ol)


    screensh = p5.renderer.fbuffer.read(mode='color', alpha=False)
    intensity: float = 0
    effectiveSurface:float=0
    pixelsCounted = 0


    if (rend.angle < 2 * PI):
        for x in range(0, width):
            for y in range(0, height):
                pixelsCounted += 1
                p = screensh[x, y]

                if (p[0] == p[1]):
                    intensity += p[0] / 255
        if not (rend.angle == 0):
            intensEfSurf = (intensity/(rend.scale*rend.scale))*rend.asteroidAlbedo
            intensityArray.append(intensEfSurf)
            phasePoints.append(rend.angle*57.3)
            magPoints.append(toMagnitude(intensEfSurf))

            print("intensity:")
            print(intensEfSurf)


    rend.rotateStep()

    if (rend.angle > 2*PI) and (rend.rendered == 0):
        #print(intensityArray)
        rend.rendered == 1
        #plt.scatter(phasePoints, intensityArray)
        #plt.scatter(phasePoints, magPoints)

        fig, (ax1, ax2) = plt.subplots(2)
        fig.suptitle('Effective reflective surface (km^2), stellar magnitude')
        ax1.plot(phasePoints, intensityArray)
        ax2.plot(phasePoints, magPoints)

        plt.show()





run(sketch_setup=None, sketch_draw=None, frame_rate=30, mode='P2D')
# run()
