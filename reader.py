
import numpy as np
from numpy import ndarray

import renderer


class ObjLoader:
    polygonCoords: ndarray

    def __init__(self):
        self.vert_coords = []  # contains vertex\point coordinates in order
        self.polygonIndexes = []
        self.polygonCoords = []  # contains 3-unit arrays each of which contains point vectors for a given polygon
        self.polygonNumber = 0  # number of polygons
        self.radius = 0  # used for scale calculation

    def loadObj(self, file):
        self.polygonNumber=0
        for line in open(file, 'r'):
            if line.startswith('#'): continue  # ignores comments
            values = line.split()
            if not values: continue
            if values[0] == 'v':

                self.vert_coords.append([float(values[1]),float(values[2]),float(values[3])])
            if values[0] == 'f':
                self.polygonNumber += 1
                thisFaceIds=[]
                for val in values:
                    if val == 'f': continue
                    else:
                        idN = 0
                        for char in val:
                            if not (char.__eq__('/')):
                                idN = idN*10+int(char)
                            else:
                                break
                        thisFaceIds.append(idN)
                thisFace = []
                for id in thisFaceIds:
                    #print("coords:")
                    #print((self.vert_coords[id-1]))
                    thisFace.append([float(self.vert_coords[id-1][0]),float(self.vert_coords[id-1][1]),float(self.vert_coords[id-1][2])])
                self.polygonCoords.append(thisFace)
        self.radius = self.findRadius()


    def printVerts(self):
        print(self.vert_coords)

    def printFaces(self):
        print(self.polygonCoords)

    def findRadius (self):
        maxLen: float = 0
        for p in self.vert_coords:
            len=renderer.vectorLength3D(p)
            if(len > maxLen): maxLen = len
        return maxLen

