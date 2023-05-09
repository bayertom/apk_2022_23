from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

class Draw(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #Query point and polygon
        self.__add_L = True
        self.__L = QPolygonF()
        self.__B = QPolygonF()
        self.__LD = QPolygonF()

        self.__add_vertex = True

        #p1 = QPointF(0, 150)
        #p2 = QPointF(100, 100)
        #p3 = QPointF(200, 150)
        #self.__L.append(p1)
        #self.__L.append(p2)
        #self.__L.append(p3)

        #p4 = QPointF(0, 100)
        #p5 = QPointF(100, 90)
        #p6 = QPointF(200, 100)

        #self.__B.append(p4)
        #self.__B.append(p5)
        #self.__B.append(p6)

    def mousePressEvent(self, e:QMouseEvent):
        #Left mouse button click
        x = e.position().x()
        y = e.position().y()

        #Create new point
        p = QPointF(x, y)

        #Add point to L
        if self.__add_L:
            self.__L.append(p)

        #Add point to B
        else:
            self.__B.append(p)

        #Repaint screen
        self.repaint()

    def paintEvent(self, e:QPaintEvent):
        #Draw polygon

        #Create graphic object
        qp = QPainter(self)

        #Start draw
        qp.begin(self)

        #Set attributes
        qp.setPen(Qt.GlobalColor.black)

        #Draw L
        qp.drawPolyline(self.__L)

        # Set attributes
        qp.setPen(Qt.GlobalColor.blue)

        # Draw B
        qp.drawPolyline(self.__B)

        # Set attributes
        qp.setPen(Qt.GlobalColor.red)

        # Draw LD
        qp.drawPolyline(self.__LD)

        #End draw
        qp.end()

    def switchSource(self):
        #Move point or add vertex
        self.__add_vertex = not(self.__add_vertex)

    def getL(self):
        return self.__L

    def getB(self):
        return self.__B

    def setLD(self, LD_):
        self.__LD = LD_

    def setSource(self, status):
        self.__add_L = status

    def clearAll(self):
        self.__L.clear()
        self.__B.clear()
        self.__LD.clear()

