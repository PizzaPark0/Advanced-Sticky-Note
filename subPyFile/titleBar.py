"""윈도우 타이틀 꾸미기
https://soma0sd.tistory.com/
"""
import os
from PySide2.QtWidgets import (QPushButton, QWidget, QLabel, QLineEdit, QApplication)
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

class MainTitleBar(QWidget):
    """제목 표시줄 위젯"""
    qss = """
        QWidget {
            color: #FFFFFF;
            background: #333333;
            height: 24px;
        }
        QLabel {
            color: #FFFFFF;
            background: #333333;
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

    def __init__(self, parent=None):
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

        label = QLabel("")
        label.setFixedHeight(self.bar_height)
        btn_minimize = self.create_tool_btn('underbar.png')
        btn_minimize.clicked.connect(self.show_minimized)
        btn_close = self.create_tool_btn('X.png')
        btn_close.clicked.connect(self.close)

        layout.addWidget(label)
        layout.addWidget(btn_minimize)
        layout.addWidget(btn_close)

        op=QGraphicsOpacityEffect(self); op.setOpacity(0); self.setGraphicsEffect(op)

    def create_tool_btn(self, icon_path):
        """제목표시줄 아이콘 생성"""
        icon = os.path.join('subPyFIle', 'img', icon_path)
        btn = QToolButton(self)
        btn.setIcon(QIcon(icon))
        btn.setIconSize(QSize(self.bar_height, self.bar_height))
        btn.setFixedSize(self.bar_height, self.bar_height)
        return btn

    def show_minimized(self):
        """버튼 명령: 최소화"""
        self.parent.showMinimized()

    def close(self):
        """버튼 명령: 닫기"""
        self.parent.openState = False
        self.parent.close()

    def mousePressEvent(self, event):
        """오버로딩: 마우스 클릭 이벤트
        - 제목 표시줄 클릭시 이동 가능 플래그
        """
        if event.button() == Qt.LeftButton:
            self.parent.is_moving = True
            self.parent.offset = event.pos()

    def mouseMoveEvent(self, event):
        """오버로딩: 마우스 이동 이벤트
        - 제목 표시줄 드래그시 창 이동
        """
        if self.parent.is_moving:
            self.parent.move(event.globalPos() - self.parent.offset)

    def mouseDoubleClickEvent(self, event):
        """오버로딩: 더블클릭 이벤트
        - 제목 표시줄 더블클릭시 최대화
        """
        if self.is_maximized:
            self.parent.showNormal()
            self.is_maximized = False
        else:
            self.parent.showMaximized()
            self.is_maximized = True

    def enterEvent(self, event: QEvent) -> None:
        op=QGraphicsOpacityEffect(self); op.setOpacity(1); self.setGraphicsEffect(op)
    
    def leaveEvent(self, event: QEvent) -> None:
        op=QGraphicsOpacityEffect(self); op.setOpacity(0); self.setGraphicsEffect(op)