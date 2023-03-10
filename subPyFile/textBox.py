import sys
from PySide2.QtWidgets import (QPushButton, QWidget, QLabel, QLineEdit, QApplication)
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import subPyFile.BaseWidget as BaseWidget
import subPyFile.quickKey as quickKey

class TextBox(BaseWidget.BlankBox):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowIcon(QIcon('subPyFile/img/icon_T.png'))

    def initUI(self):

        self.textEdit = QTextEdit('', self)
        self.textEdit.move(0,0)
        self.textEdit.resize(self.width(), self.height())
        self.textEdit.lower()
        self.textEdit.setFont(QFont('Malgun Gothic', 10))
        self.textEdit.setFrameStyle(QFrame.NoFrame)

        tempF = self.textEdit.font(); tempF.setPointSize(12); self.textEdit.setFont(tempF)

        self.setWindowTitle('TextBox')
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)

        sc1 = QShortcut(QKeySequence(quickKey.QuickKey.ctrl_r), self.textEdit, self.fontSizeUp)
        sc2 = QShortcut(QKeySequence(quickKey.QuickKey.ctrl_e), self.textEdit, self.fontSizeDown)

        self.textEdit.setFocus()

    def fontSizeUp(self):
        tempF = self.textEdit.font()
        tempF.setPointSize(tempF.pointSize()+3)
        self.textEdit.setFont(tempF)

    def fontSizeDown(self):
        tempF = self.textEdit.font()
        try:
            tempF.setPointSize(tempF.pointSize()-3)
        except:
            pass
        self.textEdit.setFont(tempF)

    def mouseMoveEvent(self, event) -> None:
        self.textEdit.resize(self.width(), self.height())        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TextBox()
    ex.show()
    app.exec_()