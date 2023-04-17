from QPoint3DF import *

class Triangle:
    def __init__(self, p1:QPoint3DF, p2:QPoint3DF, p3:QPoint3DF, slope:float, aspect:float):
        self.__p1 = p1
        self.__p2 = p2
        self.__p3 = p3
        self.__slope = slope
        self.__aspect = aspect

    def getP1(self):
        return self.__p1

    def getP2(self):
        return self.__p2

    def getP3(self):
        return self.__p3

    def getSlope(self):
        return self.__slope

    def getAspect(self):
        return self.__aspect