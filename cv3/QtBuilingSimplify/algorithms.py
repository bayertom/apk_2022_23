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
        while True:
            #Initialize maximum
            phi_max = 0
            i_max = -1

            #Find suitable point maximizing angle
            for i in range(len(pol)):

                if pj != pol[i]:
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

            #Stop condition
            if pj == q:
            	break

        return ch


    def rotate(self, pol:QPolygonF, sig:float)->QPolygonF:
        #Rotate polygon according to a given angle
        pol_rot = QPolygonF()

        #Process all polygon vertices
        for i in range(len(pol)):

            #Rotate point
            x_rot = pol[i].x() * cos(sig) - pol[i].y() * sin(sig)
            y_rot = pol[i].x() * sin(sig) + pol[i].y() * cos(sig)

            #Create QPoint
            vertex = QPointF(x_rot, y_rot)

            # Add vertex to rotated polygon
            pol_rot.append(vertex)

        return pol_rot


    def minMaxBox (self, pol: QPolygonF):
        #Create minmax box

        # Find extreme coordinates
        x_min = min(pol, key= lambda k: k.x()).x()
        x_max = max(pol, key = lambda k: k.x()).x()
        y_min = min(pol, key=lambda k: k.y()).y()
        y_max = max(pol, key=lambda k: k.y()).y()

        # Create minmax box vertices
        v1 = QPointF(x_min, y_min)
        v2 = QPointF(x_max, y_min)
        v3 = QPointF(x_max, y_max)
        v4 = QPointF (x_min, y_max)

        #Create min-max box
        minmax_box = QPolygonF([v1, v2, v3, v4])

        #Compute minmaxbox area
        area = (x_max - x_min) * (y_max - y_min)

        return minmax_box, area


    def minAreaEnclosingRectangle(self, pol: QPolygonF):
        # Create minimum area enclosing rectangle

        #Create convex hull
        ch = self.createCH(pol)

        #Get minmax box, area and sigma
        mmb_min, area_min = self.minMaxBox(ch)
        sigma_min = 0

        # Process all segments of ch
        for i in range(len(ch)-1):
            # Compute sigma
            dx = ch[i+1].x() - ch[i].x()
            dy = ch[i+1].y() - ch[i].y()
            sigma = atan2(dy,dx)

            #Rotate convex hull by sigma
            ch_rot = self.rotate(ch, sigma)

            # find minmaxbox over rotated ch
            mmb, area = self.minMaxBox(ch_rot)

            #actualize minimum area
            if area < area_min:
                area_min = area
                mmb_min = mmb
                sigma_min = sigma

        #Rotate minmax box
        er = self.rotate(mmb_min, sigma_min)

        #Resize rectangle

        return er


    def computeArea (self, pol : QPolygonF):
        #Comnpute area
        n = len(pol)
        area = 0

        #Process all vertices
        for i in range(n):
            #Area increment
            area += pol[i].x()*(pol[(i+1)%n].y()-pol[(i-1+n)%n].y())

        return 0.5*area


    def resizeRectangle(self, er: QPolygonF, pol:QPolygonF):
        #Building area
        Ab = abs(self.computeArea(pol))

        #Enclosing rectangle area
        A = abs(self.computeArea(er))

        # Fraction of Ab and A
        k = Ab/A

        #Center of mass
        x_t = (er[0].x() + er[1].x() + er[2].x() + er[3].x())/4
        y_t = (er[0].y() + er[1].y() + er[2].y() + er[3].y())/4

        #Vectors
        u1_x = er[0].x() - x_t
        u2_x = er[1].x() - x_t
        u3_x = er[2].x() - x_t
        u4_x = er[3].x() - x_t
        u1_y = er[0].y() - y_t
        u2_y = er[1].y() - y_t
        u3_y = er[2].y() - y_t
        u4_y = er[3].y() - y_t



