import numpy as np
import math
from p5 import *


class AsteroidRenderer:
    def __init__(self):
        self.sunAstDistance = 5.2  # distance to asteroid from sun
        self.astCamDistance = 5.2 # distance from asteroid to observer in AU
        self.asteroidAlbedo = 0.04
        self.solarLuminosity = 1  # sun luminosity in sun luminosities

        # camera is orthographic only
        self.cameraPos = np.array([0, 0, 10])  # where the vantage point is
        self.cameraTarget = np.array([0, 0, 0])  # point the camera is looking at
        self.cameraDir = []  # vector from Pos to Target
        self.objectRot = np.array([0, 0, 0], float)  # object rotation in radian euler angles
        self.objectPos = np.array([0, 0, 0], float)  # object center position, don`t use it, potato always is at origin, no reason to move it
        self.emissionDirRaw = np.array([0, 0, 1])  # Vector that points from (0,0,0) along light direction
        self.vectorOlega = self.emissionDirRaw * (1 / vectorLength3D(self.emissionDirRaw))
        self.scale = 200
        self.rotationMatrix = np.array([])
        self.rotationAxis = np.array([0, 0, 1], float)
        self.angle: float = 0
        self.frames: int = 30  # number of frames used for curve scan
        self.rendered = 0  # whether the object was rendered



    def render(self, obj):
        self.scale = 400 / obj.radius

        faces = self.sortFaces(obj)
        for f in faces:

            self.renderFace(f)
        screen = load_pixels()


    def rotateStep(self):
        self.angle+=2*PI/self.frames

    def renderFace(self, faceCoords):
        # recieves a face coords array and renders the face

        self.emissionDirRaw = np.array([0, 0, 1])  # Vector that points from (0,0,0) along light direction
        self.emissionDir = self.emissionDirRaw * (1 / vectorLength3D(self.emissionDirRaw))

        s1 = np.array(self.absoluteVertCoords(faceCoords[1])) - np.array(self.absoluteVertCoords(faceCoords[0]))
        s2 = np.array(self.absoluteVertCoords(faceCoords[2])) - np.array(self.absoluteVertCoords(faceCoords[1]))

        normalRaw = np.array(np.cross(s1, s2))
        if not (vectorLength3D(normalRaw)==0):
            normal = normalRaw * (1 / vectorLength3D(normalRaw))
        else:
            s3 = -s1-s2
            normalRaw = np.array(np.cross(s2, s3))
            normal = normalRaw * (1 / vectorLength3D(normalRaw))


        if (normal[2] > 0):

            # print(normal)
            # print(self.emissionDir)
            cosBeta: float = np.dot(self.vectorOlega, normal)
            effectiveNormIntesity: float = cosBeta * self.asteroidAlbedo
            fill(255 * cosBeta)

            projectedFaceCoords = []  # array with face cords projections onscreen
            for i in range(0, 3):
                projectedFaceCoords.append(self.project(faceCoords[i]))

            triangle(projectedFaceCoords[0], projectedFaceCoords[1], projectedFaceCoords[2])

    def project(self, vertex):

        globalpos = np.array([])

        # self.calculateRotMatrix()

        # globalpos=self.objectPos+np.dot(self.rotationMatrix,np.transpose(vertex))
        globalpos = self.absoluteVertCoords(vertex)
        pos = np.append(globalpos[0], globalpos[1]) * self.scale

        return pos

    def calculateRotMatrix(self):
        # self.rotationMatrix = np.array([[math.cos(self.objectRot[0]) * math.cos(self.objectRot[2]) - math.sin(self.objectRot[0]) * math.cos(self.objectRot[1]) * math.sin(self.objectRot[2]),-math.cos(self.objectRot[0]) * math.sin(self.objectRot[2]) - math.sin(self.objectRot[0]) * math.cos(self.objectRot[1]) * math.cos(self.objectRot[2]),math.sin(self.objectRot[0]) * math.sin(self.objectRot[1])],
        #                               [math.sin(self.objectRot[0]) * math.cos(self.objectRot[2]) + math.cos(self.objectRot[0]) * math.cos(self.objectRot[1]) * math.sin(self.objectRot[2]), -math.sin(self.objectRot[0]) * math.sin(self.objectRot[2]) + math.cos(self.objectRot[0]) * math.cos(self.objectRot[1]) * math.cos(self.objectRot[2]), -math.cos(self.objectRot[0]) * math.sin(self.objectRot[1])],
        #                             [math.sin(self.objectRot[1]) * math.sin(self.objectRot[2]), math.sin(self.objectRot[1]) * math.cos(self.objectRot[2]), math.cos(self.objectRot[2])]])
        normalizedAxis = self.rotationAxis * (1 / vectorLength3D(self.rotationAxis))
        x = normalizedAxis[0]
        y = normalizedAxis[1]
        z = normalizedAxis[2]
        self.rotationMatrix = np.array([[cos(self.angle) + x * x * (1 - cos(self.angle)),
                                         x * y * (1 - cos(self.angle)) - z * sin(self.angle),
                                         x * z * (1 - cos(self.angle)) + y * sin(self.angle)],
                                        [y * x * (1 - cos(self.angle)) + z * sin(self.angle),
                                         cos(self.angle) + y * y * (1 - cos(self.angle)),
                                         y * z * (1 - cos(self.angle)) - x * sin(self.angle)],
                                        [z * x * (1 - cos(self.angle)) - y * sin(self.angle),
                                         z * y * (1 - cos(self.angle)) + x * sin(self.angle),
                                         cos(self.angle) + z * z * (1 - cos(self.angle))]])

    def absoluteVertCoords(self, vertCoords):
        # self.calculateRotMatrix()

        globalpos = self.objectPos + np.dot(self.rotationMatrix, np.transpose(vertCoords))
        return (globalpos)

    def sortFaces(self, object):  # facecoords 3d list faces-vertexinfaces
        # print("start_sort")
        self.calculateRotMatrix()
        notSorted = True
        notSortedI = False
        faceCoords = object.polygonCoords
        # bubble sorts faces from farthest to closest
        while (notSorted):
            # print("iteration start")
            if not (notSortedI): notSorted = False
            notSortedI = False
            for face in range(0, object.polygonNumber - 1):
                # print(faceCoords[face])
                zf1 = self.getPolygonCenterZ(faceCoords[face])
                zf2 = self.getPolygonCenterZ(faceCoords[face + 1])
                # print(zf1)
                # print (zf2)
                if (zf1 > zf2):
                    temp = faceCoords[face]
                    faceCoords[face] = faceCoords[face + 1]
                    faceCoords[face + 1] = temp
                    # print ("sorted pair")
                    notSortedI = True
                    notSorted = True
                # else: print("found sorted pair")
            # print("facearray")
            # for face in range(0, object.polygonNumber):
            # print(faceCoords[face])
            # print(self.getPolygonCenterZ(faceCoords[face]))

        return (faceCoords)

    def getPolygonCenterCoords(self, faceCoords):
        return (0.33 * (np.array(faceCoords[0]) + np.array(faceCoords[1]) + np.array(faceCoords[2])))

    def getPolygonCenterZ(self, faceCoords):
        z = 0.33 * (self.absoluteVertCoords(faceCoords[0])[2] + self.absoluteVertCoords(faceCoords[1])[2] +
                    self.absoluteVertCoords(faceCoords[2])[2])

        return (z)


def vectorLength2D(x):
    length = math.sqrt(x[0] ** 2 + x[1] ** 2)
    return length


def vectorLength3D(x):
    length = float(math.sqrt(x[0] ** 2 + x[1] ** 2 + x[2] ** 2))
    return length
