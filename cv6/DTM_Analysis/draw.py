from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from QPoint3DF import *
from Edge import *
from triangle import *
from random import *
from math import *

class Draw(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #Points, DT, contour lines, trinagles
        self.__points : list[QPoint3DF] = []
        self.__dt : list[Edge] = []
        self.__contours: list[Edge] = []
        self.__triangles: list[Triangle] = []


    def mousePressEvent(self, e:QMouseEvent):
        #Left mouse button click
        x = e.position().x()
        y = e.position().y()
        z = random() * 100

        #Create point
        p = QPoint3DF(x,y,z)

        #Append p to point cloude
        self.__points.append(p)

        #Repaint screen
        self.repaint()

    def paintEvent(self, e:QPaintEvent):
        #Draw polygon

        #Create graphic object
        qp = QPainter(self)

        #Start draw
        qp.begin(self)

        #Set attributes, edges
        #qp.setPen(Qt.GlobalColor.black)
        #qp.setBrush(Qt.GlobalColor.white)

        # Draw points
        r = 10
        for point in self.__points:
            qp.drawEllipse(int(point.x()) - r, int(point.y()) - r, 2*r, 2*r)

        #Draw aspect
        k = 510 / pi

        #Process triangles one by one
        for t in self.__triangles:
            #Get triangle slope
            slope = t.getSlope()

            #Convert to color
            col = 255 - int(slope * k)

            #Create color
            color = QColor(col, col, col)
            qp.setBrush(color)

            #Create polygon
            pol = QPolygonF([t.getP1(), t.getP2(), t.getP3()])

            #Draw polygon
            qp.drawPolygon(pol)

        # Set attributes
        qp.setPen(Qt.GlobalColor.green)

        #Draw triangles
        for edge in self.__dt:
            qp.drawLine(int(edge.getStart().x()), int(edge.getStart().y()), int(edge.getEnd().x()), int(edge.getEnd().y()))

        # Set attributes
        qp.setPen(Qt.GlobalColor.darkRed)

        # Draw contour lines
        for edge in self.__contours:
            qp.drawLine(int(edge.getStart().x()), int(edge.getStart().y()), int(edge.getEnd().x()), int(edge.getEnd().y()))



        # Set attributes
        # qp.setPen(Qt.GlobalColor.blue)
        # qp.setBrush(Qt.GlobalColor.yellow)

        #End draw
        qp.end()

    def setDT(self, dt : list[Edge]):
        self.__dt = dt

    def setContours(self, contours : list[Edge]):
        self.__contours = contours

    def setSlope(self, triangles : list[Triangle]):
        self.__triangles = triangles

    def getPoints(self):
        return self.__points

    def getDT(self):
        return self.__dt
