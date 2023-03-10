import sys
import os
from PySide2.QtWidgets import (QPushButton, QWidget, QLabel, QLineEdit, QApplication)
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import subPyFile.BaseWidget as BaseWidget
import subPyFile.quickKey as quickKey

class Label(QLabel): #Pyside의 QLabel 오버라이드. 드래그앤 드롭 이벤트 추가함
    def __init__(self, title, parent):
        super().__init__(title, parent)
        self.setAcceptDrops(True)
        self._pixmap = QPixmap(os.path.join('img', 'blank.png'))
        self.setPixmap(self._pixmap)

    def dragEnterEvent(self, e):
        m = e.mimeData()
        if m.hasUrls():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        m = e.mimeData()
        if m.hasUrls():
            if m.urls()[0].toLocalFile():
                self._pixmap = QPixmap(m.urls()[0].toLocalFile())
                
                self.setPixmap(self._pixmap)
                self.parent().resize(self._pixmap.width(), self._pixmap.height())
                self.resize(self._pixmap.width(), self._pixmap.height())
                self.move(0,0)
                self.parent().sizeRate = 1

                self.activateWindow()

class ImageBox(BaseWidget.BlankBox):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowTitle('ImageBox')
        self.setWindowIcon(QIcon('subPyFile/img/icon_I.png'))
        self.sizeRate = 1

    def pasteClip(self):
        clip = QApplication.clipboard().pixmap()
        if clip:
            self.label._pixmap = QPixmap(clip)
            self.label.setPixmap(self.label._pixmap)
        else:
            return
        self.resize(self.label._pixmap.width(), self.label._pixmap.height())
        self.label.resize(self.label._pixmap.width(), self.label._pixmap.height())
        self.label.move(0,0)
        self.sizeRate = 1

    def moveImage(self, dx, dy):
        def moveWhere():
            self.label.move(self.label.x() + dx, self.label.y() + dy)
        return moveWhere

    def resizePixmap(self, rate):
        def magnitude():
            self.sizeRate*=rate
            newWidth = self.label._pixmap.width()*self.sizeRate
            newHeight = self.label._pixmap.height()*self.sizeRate
            if newWidth<10 and newHeight<10:
                newWidth=10; newHeight=10
            self.label.resize(newWidth, newHeight)
            self.label.setPixmap(self.label._pixmap.scaled(newWidth, newHeight))
        return magnitude

    def initUI(self):

        self.label = Label("", self)
        self.label.move(0,0)
        self.label.resize(self.width(), self.height())
        self.label.lower()
        self.label.sizePolicy().MinimumExpanding = 1
        self.label.minimumSize = 1

        sc1 = QShortcut(QKeySequence(quickKey.QuickKey.ctrl_v), self.label, self.pasteClip)

        sc1 = QShortcut(QKeySequence(quickKey.QuickKey.upArrow), self.label, self.moveImage(0, -10))
        sc2 = QShortcut(QKeySequence(quickKey.QuickKey.downArrow), self.label, self.moveImage(0, 10))
        sc3 = QShortcut(QKeySequence(quickKey.QuickKey.rightArrow), self.label, self.moveImage(10, 0))
        sc4 = QShortcut(QKeySequence(quickKey.QuickKey.leftArrow), self.label, self.moveImage(-10, 0))
        
        sc5 = QShortcut(QKeySequence(quickKey.QuickKey.ctrl_r), self.label, self.resizePixmap(103/100))
        sc6 = QShortcut(QKeySequence(quickKey.QuickKey.ctrl_e), self.label, self.resizePixmap(100/103))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageBox()
    ex.show()
    app.exec_()