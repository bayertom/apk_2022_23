from qpoint3df import *

class Edge:
    def __init__(self, start:QPoint3DF, end:QPoint3DF):
        self.__start = start
        self.__end = end

    def getStart(self):
        #Return start point
        return self.__start

    def getEnd(self):
        #Return end point
        return self.__end

    def switchOrientation(self):
        #Create new edge with an opposite orientation
        return Edge(self.__end, self.__start)

