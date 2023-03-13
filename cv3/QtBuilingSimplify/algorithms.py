from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from operator import attrgetter
from typing import List
from math import *

class Algorithms:
    def __init__(self):
        pass

    def get2LinesAngle(self, p1 : QPoint, p2 : QPoint, p3 : QPoint, p4 : QPoint ):
        # Compute angle formed by two lines

        # Coordinate differences
        ux = p2.x() - p1.x()
        uy = p2.y() - p1.y()
        vx = p4.x() - p3.x()
        vy = p4.y() - p3.y()

        # Dot product
        dp = ux * vx + uy * vy

        # Norms
        nu = (ux * ux + uy * uy)**0.5
        nv = (vx * vx + vy * vy)**0.5

        # Angle
        return abs(acos(dp / (nu * nv)))


    def chJarvis(self, points : QPolygon)->QPolygon:
        # Create Convex Hull using Jarvis Scan Algorithm
        ch = QPolygon()

        #Find pivot q
        q = min(points, key=lambda k: k.y())

        # Initialize pj, pjj
        pj = q;
        pjj = QPoint(0, q.y());

        #Add q into Convex Hull
        ch.append(q);

        #Find all points of Convex hull
        while (True):

            # Initialize i_max, om_max
            i_max : int = -1
            o_max : float = 0

            # Find suitable point maximizing angle omega
            for i in range(len(points)):
                # Compute omega
                if points[i] != pj:
                    omega = self.get2LinesAngle(pj, pjj, pj, points[i])

                    # Actualize maximum
                    if omega > o_max:
                        o_max = omega
                        i_max = i

            # Add point to convex hull
            ch.append(points[i_max])

            # Assign points
            pjj = pj
            pj = points[i_max]

            #Stopping condition
            if pj == q:
                break

        return ch


    def rotate(self, pol : QPolygon, sigma:float)->QPolygon:
        #Rotate points by angle
        polr = QPolygon()
        for i in range(len(pol)):
            #Rotate point
            xr = pol[i].x() * cos(sigma) - pol[i].y() * sin(sigma);
            yr = pol[i].x() * sin(sigma) + pol[i].y() * cos(sigma);

            #Create point
            pr = QPoint(int(xr), int(yr));

            #Add point to the list
            polr.append(pr);

        return polr


    def minMaxBox(self, pol : QPolygon):
        # Return vertices of min - max box and its area
        area = 0;

        #Return vertices with extreme coordinates
        xmin = min(pol, key=lambda k: k.x()).x()
        xmax = max(pol, key=lambda k: k.x()).x()
        ymin = min(pol, key=lambda k: k.y()).y()
        ymax = max(pol, key=lambda k: k.y()).y()

        #Create min - max box vertices
        v1 = QPoint(xmin, ymin)
        v2 = QPoint(xmax, ymin)
        v3 = QPoint(xmax, ymax)
        v4 = QPoint(xmin, ymax)

        # Create min - max box
        mmb = QPolygon([v1, v2, v3, v4])

        #Compute min - max box area
        area = (xmax - xmin) * (ymax - ymin)

        return mmb, area


    def minAreaEnclosingRectangle(self, pol : QPolygon):
        #Create minimum area enclosing rectangle
        ch = self.chJarvis(pol);
        n = len(ch)

        #Initialize area_min
        sigma_min = 0
        mmb_min, area_min = self.minMaxBox(ch);

        #Process all convex hull segments
        for i in range(n-1):
            #Take a segment
            dx = ch[(i + 1)].x() - ch[i].x();
            dy = ch[(i + 1)].y() - ch[i].y();

	        #Compute its direction
            sigma = atan2(dy, dx);

            # Rotate by - sigma
            chr = self.rotate(ch, -sigma);

            # Create min - max box
            mmb, area = self.minMaxBox(chr);

            #Update minimum
            if area < area_min:
                area_min = area
                sigma_min = sigma
                mmb_min = mmb

        #Create enclosing rectangle, rotate sigma_min
        er = self.rotate(mmb_min, sigma_min);

        #Resize rectangle, preserve area of the building
        err = self.resizeRectangle(pol, er);

        return err;


    def wallAverage(self, pol : QPolygon):
        # Create enclosing rectangle using wall average
        sigma = 0
        si_sum = 0

        # Compute initial direction
        dx = pol[1].x() - pol[0].x();
        dy = pol[1].y() - pol[0].y();
        sigma0 = atan2(dy, dx);

        #Compute direction of segments
        n = len(pol)
        for i in range(n-1):
            dxi = pol[(i + 1)].x() - pol[i].x();
            dyi = pol[(i + 1)].y() - pol[i].y();
            sigmai = atan2(dyi, dxi);
            lengthi = (dxi * dxi + dyi * dyi)**0.5;

            #Compute direction differences
            dsigmai = sigmai - sigma0;
            if dsigmai < 0:
                dsigmai += 2 * pi;

            #Compute fraction
            ki = round(dsigmai / (pi / 2));

            #Compute reminder
            ri = dsigmai-ki * (pi / 2);

            #Weighted average sums
            sigma += ri * lengthi;
            si_sum += lengthi;

        #Weighted average
        sigma = sigma0 + sigma / si_sum;

        #Rotate by - sigma
        polr = self.rotate(pol, -sigma);

        #Create min - max box
        mmb, area = self.minMaxBox(polr);

        #Create enclosing rectangle
        er = self.rotate(mmb, sigma);

        #Resize rectangle, preserve area of the building
        err = self.resizeRectangle(pol, er);

        return err;


    def LH(self, points : List[QPoint]):
        #Get area of building by L-Huillier formula
        n = len(points)
        area = 0;

        #Proces all vertices of the building
        for i in range(n):
            area += points[i].x() * (points[(i + 1) % n].y() - points[(i - 1 + n) % n].y());

        return 0.5 * abs(area)


    def resizeRectangle(self, points : List [QPoint], er : QPolygon):
        #Resize rectangle to given area

        #Building area
        AB = self.LH(points);

        #Rectangle area
        AR = self.LH(er);

        #Fraction of areas
        k = AB / AR;

        #Center of mass
        xc = (er[0].x() + er[1].x() + er[2].x() + er[3].x()) / 4;
        yc = (er[0].y() + er[1].y() + er[2].y() + er[3].y()) / 4;

        #Compute vector components
        u1x = er[0].x() - xc;
        u1y = er[0].y() - yc;
        u2x = er[1].x() - xc;
        u2y = er[1].y() - yc;
        u3x = er[2].x() - xc;
        u3y = er[2].y() - yc;
        u4x = er[3].x() - xc;
        u4y = er[3].y() - yc;

        #Create new rectangle vertices
        v1_ = QPoint(int(xc + sqrt(k) * u1x), int(yc + sqrt(k) * u1y))
        v2_ = QPoint(int(xc + sqrt(k) * u2x), int(yc + sqrt(k) * u2y))
        v3_ = QPoint(int(xc + sqrt(k) * u3x), int(yc + sqrt(k) * u3y))
        v4_ = QPoint(int(xc + sqrt(k) * u4x), int(yc + sqrt(k) * u4y))

        #Add vertices
        er_res = QPolygon([v1_, v2_, v3_, v4_]);

        return er_res