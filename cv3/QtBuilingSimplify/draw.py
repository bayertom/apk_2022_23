from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

class Draw(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #Building, convex hull and enclosing rectangle
        self.__pol = QPolygonF()

    def mousePressEvent(self, e:QMouseEvent):
        #Left mouse button click
        x = e.position().x()
        y = e.position().y()

        #Add point to polygon
        p = QPointF(x,y)

        #Append p to polygon
        self.__pol.append(p)

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
        qp.setBrush(Qt.GlobalColor.white)

        #Draw polygon
        qp.drawPolygon(self.__pol)

        #End draw
        qp.end()

    def getPolygon(self):
        #Get polygon
        return self.__pol

