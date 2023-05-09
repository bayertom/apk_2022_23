from PyQt6.QtCore import *
from PyQt6.QtGui import *

class QPoint3DF(QPointF):
    def __init__(self, x:float, y:float, z:float):
        super().__init__(x, y)
        self.__z = z

    def getZ(self):
        return self.__z

