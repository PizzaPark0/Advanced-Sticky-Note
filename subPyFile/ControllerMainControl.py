"""윈도우 타이틀 꾸미기
https://soma0sd.tistory.com/
"""
import os
from PySide2.QtWidgets import (QPushButton, QWidget, QLabel, QLineEdit, QApplication)
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

class MainControl(QWidget):
    """제목 표시줄 위젯"""
    qss = """
        QWidget {
            color: #0000FF;
            background: #000033;
            height: 24px;
        }
        QLabel {
            color: #FFFFFF;
            background: #555555;
            font-size: 16px;
            padding: 5px 5px;
        }
        QToolButton {
            background: #333333;
            border: none;
        }
        QToolButton:hover{
            background: #444444;
        }
    """

    def __init__(self, parent=None, titleName=''):
        super().__init__(parent)
        self.bar_height = 36
        self.resize(self.width(), 35)
        self.parent = parent
        self.has_clicked = False
        self.is_maximized = False
        self.setStyleSheet(self.qss)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        btn_newImageBox = self.create_tool_btn('image.png')
        btn_newTextBox = self.create_tool_btn('text.png')

        btn_newImageBox.clicked.connect(self.parent.showImageBox)
        btn_newTextBox.clicked.connect(self.parent.showTextBox)

        label = QLabel(titleName)
        label.setFixedHeight(self.bar_height)

        layout.addWidget(btn_newImageBox)
        layout.addWidget(btn_newTextBox)
        layout.addWidget(label)

    def create_tool_btn(self, icon_path):
        """제목표시줄 아이콘 생성"""
        icon = os.path.join('subPyFIle', 'img', icon_path)
        btn = QToolButton(self)
        btn.setIcon(QIcon(icon))
        btn.setIconSize(QSize(self.bar_height, self.bar_height))
        btn.setFixedSize(self.bar_height, self.bar_height)
        return btn