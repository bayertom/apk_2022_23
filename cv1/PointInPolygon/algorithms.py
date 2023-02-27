from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

class Algorithms:

    def __init__(self):
        pass

    def getPointPolygonPositionR(self, q, pol):
        k = 0
        n = len(pol)

        #Proces all vertices
        for i in range(n):
            #Reduce coordinate
            xir = pol[i].x() - q.x()
            yir = pol[i].y() - q.y()
            xi1r = pol[(i+1)%n].x() - q.x()
            yi1r = pol[(i+1)%n].y() - q.y()

            #Suitable segment
            if (yi1r > 0) and (yir <= 0) or (yir >0 ) and (yi1r <=0):

                #Compute intersection
                xm = (xi1r*yir - xir*yi1r)/(yi1r - yir)

                #Increment amount of intersections
                if xm > 0:
                    k += 1

        #Point is inside
        if k % 2 == 1:
            return 1

        #Point is outside
        return 0
