import sys
from PySide2.QtWidgets import (QPushButton, QWidget, QLabel, QLineEdit, QApplication)
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import subPyFile.titleBar as titleBar
import subPyFile.quickKey as quickKey

class SideGrip(QWidget):
    def __init__(self, parent, edge):
        QWidget.__init__(self, parent)
        if edge ==Qt.LeftEdge:
            self.setCursor(Qt.SizeHorCursor)
            self.resizeFunc = self.resizeLeft
        elif edge == Qt.TopEdge:
            self.setCursor(Qt.SizeVerCursor)
            self.resizeFunc = self.resizeTop
        elif edge == Qt.RightEdge:
            self.setCursor(Qt.SizeHorCursor)
            self.resizeFunc = self.resizeRight
        elif edge == Qt.BottomEdge:
            self.setCursor(Qt.SizeVerCursor)
            self.resizeFunc = self.resizeBottom
        self.mousePos = None

    def resizeLeft(self, delta):
        window = self.window()
        width = max(window.minimumWidth(), window.width() - delta.x())
        geo = window.geometry()
        geo.setLeft(geo.right() - width)
        window.setGeometry(geo)

    def resizeTop(self, delta):
        window = self.window()
        height = max(window.minimumHeight(), window.height() - delta.y())
        geo = window.geometry()
        geo.setTop(geo.bottom() - height)
        window.setGeometry(geo)

    def resizeRight(self, delta):
        window = self.window()
        width = max(window.minimumWidth(), window.width() + delta.x())
        window.resize(width, window.height())

    def resizeBottom(self, delta):
        window = self.window()
        height = max(window.minimumHeight(), window.height() + delta.y())
        window.resize(window.width(), height)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mousePos = event.pos()

    def mouseMoveEvent(self, event):
        if self.mousePos is not None:
            delta = event.pos() - self.mousePos
            self.resizeFunc(delta)

    def mouseReleaseEvent(self, event):
        self.mousePos = None

class BlankBox(QDialog):
    _gripSize = 8
    def __init__(self, parent=None):

        QDialog.__init__(self, parent)
        self.topHintState = True
        self.openState = True

        self.resize(300, 300)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Window)
        self.setStyleSheet('QDialog { background-color: white;}')

        self.titlebar_widget = titleBar.MainTitleBar(self)
        self.titlebar_widget.setObjectName("windowTitle")
        self.titlebar_widget.resize(self.width(), self.titlebar_widget.height())

        self.shadow = QGraphicsDropShadowEffect(self)
        self.setGraphicsEffect(self.shadow)

        self.sideGrips = [
            SideGrip(self, Qt.LeftEdge), 
            SideGrip(self, Qt.TopEdge), 
            SideGrip(self, Qt.RightEdge), 
            SideGrip(self, Qt.BottomEdge)
        ]

        self.cornerGrips = [QSizeGrip(self) for i in range(4)]
        for i in self.cornerGrips:
            op=QGraphicsOpacityEffect(i); op.setOpacity(0); i.setGraphicsEffect(op)

        sc1 = QShortcut(QKeySequence(quickKey.QuickKey.ctrl_tab), self, self.toggleTopHint)

    def toggleTopHint(self):
        if self.topHintState:
            self.topHintState = False
            self.setWindowFlag(Qt.WindowStaysOnTopHint, False)
            self.show()
        else:
            self.topHintState = True          
            self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
            self.show()

    @property
    def gripSize(self):
        return self._gripSize

    def setGripSize(self, size):
        if size == self._gripSize:
            return
        self._gripSize = max(2, size)
        self.updateGrips()

    def updateGrips(self):
        self.setContentsMargins(*[self.gripSize] * 4)

        outRect = self.rect()
        # an "inner" rect used for reference to set the geometries of size grips
        inRect = outRect.adjusted(self.gripSize, self.gripSize,
            -self.gripSize, - self.gripSize)

        # top left
        self.cornerGrips[0].setGeometry(
            QRect(outRect.topLeft(), inRect.topLeft()))
        # top right
        self.cornerGrips[1].setGeometry(
            QRect(outRect.topRight(), inRect.topRight()).normalized())
        # bottom right
        self.cornerGrips[2].setGeometry(
            QRect(inRect.bottomRight(), outRect.bottomRight()))
        # bottom left
        self.cornerGrips[3].setGeometry(
            QRect(outRect.bottomLeft(), inRect.bottomLeft()).normalized())

        # left edge
        self.sideGrips[0].setGeometry(
            0, inRect.top(), self.gripSize, inRect.height())
        # top edge
        self.sideGrips[1].setGeometry(
            inRect.left(), 0, inRect.width(), self.gripSize)
        # right edge
        self.sideGrips[2].setGeometry(
            inRect.left() + inRect.width(), 
            inRect.top(), self.gripSize, inRect.height())
        # bottom edge
        self.sideGrips[3].setGeometry(
            self.gripSize, inRect.top() + inRect.height(), 
            inRect.width(), self.gripSize)

    def resizeEvent(self, event):
        QWidget.resizeEvent(self, event)
        self.updateGrips()
        self.titlebar_widget.resize(self.width(), self.titlebar_widget.height())
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = BlankBox()
    ex.show()
    app.exec_()