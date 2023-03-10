import sys
import os

from PySide2.QtWidgets import (QPushButton, QWidget, QLabel, QLineEdit, QApplication)
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import subPyFile.dropImageBox as dropImageBox
import subPyFile.textBox as textBox
import subPyFile.ControllerTitlebar as ControllerTitlebar
import subPyFile.ControllerMainControl as ControllerMainControl

import ctypes
myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

class MainController(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.initUI()
        self.setWindowIcon(QIcon('subPyFile/img/icon_M.png'))
        self.setWindowTitle('Sticky Note')

        self.boxList = []
        self.tempSaveDir = os.path.join('saveData')

        self.openLastSave()
        
    def initUI(self):
        self.setFixedWidth(180)
        self.title_bar = ControllerTitlebar.MainTitleBar(self, titleName='Sticky Note')
        self.title_bar.resize(180, self.title_bar.height())
        self.mainWidget = ControllerMainControl.MainControl(self, titleName='')
        self.mainWidget.resize(180, self.title_bar.height())
        self.mainWidget.move(0, 35)
        self.mainWidget.lower()
        self.setFixedHeight(self.title_bar.height()*2)
        self.title_bar.show()
        self.mainWidget.show()

    def showImageBox(self):
        self.boxList.append(dropImageBox.ImageBox())
        self.boxList[-1].show()

    def showTextBox(self):
        self.boxList.append(textBox.TextBox())
        self.boxList[-1].show()

    def openLastSave(self): #SaveData폴더에 저장된 마지막 역사를 복원함
        for i in sorted(os.listdir(self.tempSaveDir)):
            if i[-1]=='g':
                continue
            with open(os.path.join(self.tempSaveDir, i), 'r') as f:
                data = f.readlines()
                self.reSpawnImageBox(data)
                self.reSpawnTextBox(data)
    
    def reSpawnImageBox(self, dataList):
        if dataList[1]!='ImageBox\n':
            return
        i_box = dropImageBox.ImageBox()
        i_box.resize(int(dataList[2]), int(dataList[3]))
        i_box.move(int(dataList[4]), int(dataList[5]))
        i_box.label.move(int(dataList[6]), int(dataList[7]))
        i_box.label.resize(int(dataList[8]), int(dataList[9]))
        i_box.label._pixmap = QPixmap(os.path.join(self.tempSaveDir, dataList[0].rstrip('\n')+'.png'))
        i_box.label.setPixmap(i_box.label._pixmap.scaled(i_box.label._pixmap.width()*float(dataList[11]), i_box.label._pixmap.height()*float(dataList[11])))
        i_box.sizeRate = float(dataList[11])
        i_box.topHintState = True if dataList[12]=='True' else False; i_box.setWindowFlag(Qt.WindowStaysOnTopHint, i_box.topHintState)
        self.boxList.append(i_box)
        self.boxList[-1].show()

    
    def reSpawnTextBox(self, dataList):
        if dataList[1]!='TextBox\n':
            return
        i_box = textBox.TextBox()
        i_box.resize(int(dataList[2]), int(dataList[3]))
        i_box.move(int(dataList[4]), int(dataList[5]))
        i_box.textEdit.resize(int(dataList[2]), int(dataList[3]))
        tempF = i_box.textEdit.font(); tempF.setPointSize(int(dataList[6])); i_box.textEdit.setFont(tempF)
        i_box.topHintState = True if dataList[7]=='True\n' else False; i_box.setWindowFlag(Qt.WindowStaysOnTopHint, i_box.topHintState)
        i_box.textEdit.setText(''.join(dataList[8:]))
        self.boxList.append(i_box)
        self.boxList[-1].show()
        

    def closeEvent(self, event: QCloseEvent) -> None:
        for f in os.listdir(self.tempSaveDir): #새 임시파일 저장 전 초기화
            os.remove(os.path.join(self.tempSaveDir, f))

        #메인컨트롤을 닫을 때, 열려 있던 모든 메모를 닫고 파일에 저장함
        for n, i in enumerate(self.boxList):
            if not i.openState:
                continue
            boxType = str(type(i))
            if boxType=="<class 'subPyFile.textBox.TextBox'>":
                tempData = self.getTextBoxData(i, f"{n}_textW.txt")
                with open(os.path.join(self.tempSaveDir, tempData[0]), 'w') as f:
                    f.write('\n'.join(map(str, tempData)))

            elif boxType=="<class 'subPyFile.dropImageBox.ImageBox'>":
                tempData = self.getImageBoxData(i, f"{n}_imageW.txt")
                tempData[10].save(os.path.join(self.tempSaveDir, tempData[0]+'.png'), 'PNG')
                with open(os.path.join(self.tempSaveDir, tempData[0]), 'w') as f:
                    f.write('\n'.join(map(str, tempData)))

            i.close()
        self.boxList.clear()
    
    def getTextBoxData(self, widget, w_name):
        widgetSaveName = w_name

        widgetType = 'TextBox'
        widgetSize_X = widget.width()
        widgetSize_Y = widget.height()
        widgetPos_X = widget.pos().x()
        widgetPos_Y = widget.pos().y()
        fontsize = widget.textEdit.font().pointSize()
        topHint = widget.topHintState
        textInEdit = widget.textEdit.toPlainText()
        

        return (
            widgetSaveName,
            widgetType,
            widgetSize_X,
            widgetSize_Y,
            widgetPos_X,
            widgetPos_Y,
            fontsize,
            topHint,
            textInEdit
            )

    def getImageBoxData(self, widget, w_name):
        widgetSaveName = w_name

        widgetType = 'ImageBox'
        widgetSize_X = widget.width()
        widgetSize_Y = widget.height()
        widgetPos_X = widget.pos().x()
        widgetPos_Y = widget.pos().y()
        labelPos_X = widget.label.pos().x()
        labelPos_Y = widget.label.pos().y()
        labelSize_X = widget.label.width()
        labelSize_Y = widget.label.height()
        pixmapInLabel = widget.label._pixmap
        pixmapSize = widget.sizeRate
        topHint = widget.topHintState

        return (
            widgetSaveName,
            widgetType,
            widgetSize_X,
            widgetSize_Y,
            widgetPos_X,
            widgetPos_Y,
            labelPos_X,
            labelPos_Y,
            labelSize_X,
            labelSize_Y,
            pixmapInLabel,
            pixmapSize,
            topHint,
            )

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainController()
    ex.show()
    app.exec_()
