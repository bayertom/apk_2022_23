from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from QPoint3DF import *
from Edge import *
from random import *

class Draw(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #Points, DT, contour lines, trinagles
        self.__points : List[QPoint3DF] = []
        self.__dt : List[Edge] = []


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

        #Set attributes, building
        qp.setPen(Qt.GlobalColor.black)
        qp.setBrush(Qt.GlobalColor.white)

        # Draw points
        r = 10
        for point in self.__points:
            qp.drawEllipse(int(point.x()) - r, int(point.y()) - r, 2*r, 2*r)


        #Draw building
        #qp.drawPolygon(self.__pol)

        # Set attributes, convex hull
        #qp.setPen(Qt.GlobalColor.blue)
        #qp.setBrush(Qt.GlobalColor.yellow)

        # Draw convex hull
        #qp.drawPolygon(self.__ch)

        # Set attributes, enclosing rectangle
        #qp.setPen(Qt.GlobalColor.red)
        #qp.setBrush(Qt.GlobalColor.yellow)

        # Draw building
        #qp.drawPolygon(self.__er)

        #End draw
        qp.end()
