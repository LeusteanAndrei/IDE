from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt, QPoint

class CustomTitleBar(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setFixedHeight(40)
        self.setStyleSheet('''
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #23272b, stop:1 #263445);
            }
        ''')
        self.init_ui()
        self.start = QPoint(0, 0)
        self.pressing = False

    def init_ui(self):
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 0)
        layout.setSpacing(10)

        # Icon
        icon_label = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap('icons/c++icon.png')
        icon_label.setPixmap(pixmap.scaled(28, 28, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        icon_label.setFixedSize(32, 32)
        icon_label.setStyleSheet("background: transparent;")
        layout.addWidget(icon_label)

        # Title
        self.title_label = QtWidgets.QLabel('Tuc++')
        self.title_label.setStyleSheet('''
            QLabel {
                color: #aee9d1;
                font-size: 20px;
                font-weight: bold;
                letter-spacing: 1.5px;
                background: transparent;
            }
        ''')
        layout.addWidget(self.title_label)
        layout.addStretch()

        # Minimize button
        self.min_btn = QtWidgets.QPushButton('–')
        self.min_btn.setFixedSize(32, 32)
        self.min_btn.setStyleSheet(self.button_style())
        self.min_btn.clicked.connect(self.minimize)
        layout.addWidget(self.min_btn)

        # Maximize/Restore button
        self.max_btn = QtWidgets.QPushButton('□')
        self.max_btn.setFixedSize(32, 32)
        self.max_btn.setStyleSheet(self.button_style())
        self.max_btn.clicked.connect(self.maximize_restore)
        layout.addWidget(self.max_btn)

        # Close button
        self.close_btn = QtWidgets.QPushButton('✕')
        self.close_btn.setFixedSize(32, 32)
        self.close_btn.setStyleSheet(self.button_style(close=True))
        self.close_btn.clicked.connect(self.close_window)
        layout.addWidget(self.close_btn)

    def button_style(self, close=False):
        if close:
            return '''
                QPushButton {
                    background: #23272b;
                    color: #e57373;
                    border: none;
                    border-radius: 8px;
                    font-size: 18px;
                }
                QPushButton:hover {
                    background: #e57373;
                    color: #fff;
                }
            '''
        return '''
            QPushButton {
                background: #23272b;
                color: #aee9d1;
                border: none;
                border-radius: 8px;
                font-size: 18px;
            }
            QPushButton:hover {
                background: #78A083;
                color: #23272b;
            }
        '''

    def minimize(self):
        if self.parent:
            self.parent.showMinimized()

    def maximize_restore(self):
        if self.parent:
            if self.parent.isMaximized():
                self.parent.showNormal()
            else:
                self.parent.showMaximized()

    def close_window(self):
        if self.parent:
            self.parent.close()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start = event.globalPos()
            self.pressing = True
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.pressing and self.parent:
            delta = event.globalPos() - self.start
            self.parent.move(self.parent.pos() + delta)
            self.start = event.globalPos()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.pressing = False
        super().mouseReleaseEvent(event) 