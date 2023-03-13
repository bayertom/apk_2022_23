from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from math import *

class Algorithms:

    def __init__(self):
        pass

    def getPointPolygonPositionR(self, q, pol):
        k = 0
        n = len(pol)

        # proces all vertices
        for i in range(n):
            #reduce coordinate
            xir = pol[i].x() - q.x()
            yir = pol[i].y() - q.y()
            xi1r = pol[(i+1)%n].x() - q.x()
            yi1r = pol[(i+1)%n].y() - q.y()

            #Suitable segment
            if (yi1r > 0) and (yir <= 0) or (yir >0 ) and (yi1r <=0):

                #compute intersection
                xm = (xi1r*yir - xir*yi1r)/(yi1r - yir)

                # increment amount of intersections
                if xm > 0:
                    k += 1

        # point is inside
        if k % 2 == 1:
            return 1

        return 0

    def get2LinesAngle(self, p1:QPointF,p2:QPointF,p3:QPointF,p4:QPointF):
        ux = p2.x() - p1.x()
        uy = p2.y() - p1.y()
        vx = p4.x() - p3.x()
        vy = p4.y() - p3.y()

        #Dot product
        dp = ux*vx + uy*vy

        #Norms
        nu = (ux**2 + uy**2)**0.5
        nv = (vx**2 + vy**2)**0.5

        return acos(dp/(nu*nv))

    def createCH(self, pol:QPolygonF):
        #Create CH using Jarvis scan
        ch = QPolygonF()

        #Find pivot
        q = min(pol, key = lambda k : k.y())

        #Initialize pj-1, pj
        pj1 = QPointF(q.x() - 1, q.y())
        pj = q

        #Add q to convex hull
        ch.append(q)

        # Jarvis scan
        while pj1 != q:
            #Initialize maximum
            phi_max = 0
            i_max = -1

            #Find suitable point maximizing angle
            for i in range(len(pol)):

                #Measure angle
                phi = self.get2LinesAngle(pj, pj1, pj, pol[i])

                #Actualize phi_max
                if phi > phi_max:
                    phi_max = phi
                    i_max = i

            # Append point to CH
            ch.append(pol[i_max])

            #Actualize last two points
            pj1 = pj
            pj = pol[i_max]

        return ch

