from PyQt5.QtWidgets import QPushButton, QWidget, QGridLayout
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QSize, Qt
from datatypes import OperationMode
from utilities import resource_path
from typing import Callable, NewType


ConverterWidget = NewType('ConverterWidget', QWidget)


class ModeButton(QPushButton):
    def __init__(self, icon_path: str, text: str, on_click: Callable) -> None:
        super().__init__()
        self.icon_path = icon_path
        self.text = text
        self.on_click = on_click
        self.init_ui()

    def init_ui(self) -> None:
        self.setText(self.text)
        pixmap = QPixmap(resource_path(self.icon_path))
        icon = QIcon(pixmap)
        self.clicked.connect(self.on_click)
        self.setIcon(icon)
        self.setIconSize(QSize(100, 100))
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("QPushButton {border-radius: 11px;"
                           "             background-color: whitesmoke;"
                           "             border: 1px solid lightgrey;"
                           "             padding: 5px;}\n"
                           "QPushButton:hover {background-color: lightgrey;}\n"
                           "QPushButton:pressed {background-color: grey;"
                           "                     color: whitesmoke}")


class ModeSelection(QWidget):
    def __init__(self, parent: ConverterWidget) -> None:
        super().__init__()
        self.parent = parent
        self.layout = QGridLayout()
        self.init_ui()

    def init_ui(self) -> None:
        elan_button = ModeButton('./img/elan.png',
                                 'Import ELAN File',
                                 on_click=self.on_click_elan)
        self.layout.addWidget(elan_button, 0, 0, 1, 1)
        scratch_button = ModeButton('./img/scratch.png',
                                    'Start From Scratch',
                                    on_click=self.on_click_scratch)
        self.layout.addWidget(scratch_button, 0, 1, 1, 1)
        self.setLayout(self.layout)

    def on_click_elan(self) -> None:
        self.parent.data.mode = OperationMode.ELAN
        self.parent.load_initial_widgets()

    def on_click_scratch(self) -> None:
        self.parent.data.mode = OperationMode.SCRATCH
        self.parent.load_third_stage_widgets(self.parent.components, self.parent.data)
