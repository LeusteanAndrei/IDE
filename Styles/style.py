#Aici sunt instructiunile de css pentru styling - specific intr-o variabila stilurile dorite pt anumite widget-uri
#si dupa in main pasez variabila corespunzatoare cu setStyleSheet()

# EDITOR_STYLE = """
# QPlainTextEdit {
#     color: white;
#     border: 1px solid #5c5f77;
#     border-radius: 5px;
#     padding: 5px;
# }

# QPlainTextEdit:hover {
#     border: 1px solid #ffffff;
# }
# """
EDITOR_STYLE = """
    color: white;
    border: 1px solid #5c5f77;
    border-radius: 5px;
    padding: 5px;

"""


MAIN_WINDOW_STYLE = """
QMainWindow {
    background-color: #344955;
}
"""

BUTTON_STYLE = """
QPushButton#FunctionButton {
    color: #000;
    background-color: #344955;
    border: 1px solid #50727B;
    border-radius: 10px;
    padding: 8px 0px;
    font-family: 'Roboto Mono', 'Roboto', monospace;
    font-size: 22px;
    margin: 0 6px;
}
QPushButton#FunctionButton:hover, QPushButton#FunctionButton:checked {
    color: #344955;
    background-color: #78A083;
    border: 2px solid #344955;
}
"""

# Style for grid layouts (if needed for widgets)
GRID_LAYOUT_STYLE = """
QWidget {
    background-color: #344955;
    color: #e0e0e0;
}
"""

EDITOR_FONT_SIZE = 20

PLACEHOLDER_STYLE = """
QLabel {
    background-color: #344955;
    color: #78A083;
    font-family: 'Roboto Mono', 'Roboto', monospace;
    font-size: 14px;
    border: 1px solid #50727B;
}
QTreeView {
    background-color: #23272b;
    color: #e0e0e0;
    font-family: 'Roboto Mono', 'Roboto', monospace;
    font-size: 14px;
    border: 1px solid #50727B;
}
"""
MENU_STYLE = """
    QMenu {
        background-color: #344955;
        border: 2px solid #78A083;
        border-radius: 10px;
        padding: 8px;
        min-width: 200px;
    }
    QMenu::item {
        background-color: transparent;
        color: #78A083;
        padding: 8px 24px;
        border-radius: 8px;
        min-width: 180px;
    }
    QMenu::item:selected {
        background-color: #78A083;
        color: #344955;
    }
            QMenu::item:disabled {
            background-color: #78A083;
            color: #344955;
            font-weight: bold;
        }
    """

MENU_BUTTON_STYLE = """
    QPushButton {
        background-color: #344955;
        color: #78A083;
        border: 2px solid #78A083;
        border-radius: 15px;
        padding: 12px 10px;
        font-size: 25px;
        min-width: 70px;
        min-height: 40px;
    }
    QPushButton:hover, QPushButton:checked {
        background-color: #78A083;
        color: #344955;
        border: 2px solid #344955;
    }
    QPushButton::menu-indicator {
        image: none;
        width: 0px;
        height: 0px;
    }
    """

SMALL_MENU_BUTTON_STYLE = """
    QPushButton {
        background-color: #344955;
        color: #78A083;
        border: 2px solid #78A083;
    }
    QPushButton:hover, QPushButton:checked {
        background-color: #78A083;
        color: #344955;
        border: 2px solid #344955;
    }
    QPushButton::menu-indicator {
        image: none;
        width: 0px;
        height: 0px;
    }
    """

BUTTON_STYLE = """
QPushButton {
    background-color: #5c5f77;
    color: #ffffff;
    border: 1px solid #35374b;
    border-radius: 5px;
    padding: 5px;
}
QPushButton:hover {
    background-color: #6d6f8a;
    border: 1px solid #ffffff;
}
"""


TERMINAL_STYLE = """
QPlainTextEdit {
    background-color: #181b1f;
    color: #e0e0e0;
    font-family: 'Roboto Mono', 'Roboto', monospace;
    font-size: 14px;
    border: 1px solid #344955;
    border-radius: 5px;
    padding: 5px;
}
"""

FILE_TAB_STYLE = """
QTabWidget::pane {
    background: #23272b;
    border-top: 2px solid #78A083;
    margin-left: 10px;
}

QTabBar {
    margin-top: 8px;
    qproperty-drawBase: 0;
}

QTabBar::tab {
    background: transparent;
    border: none;
    min-width: 0px;
    min-height: 0px;
    padding: 0px;
    margin: 0px;
}
QTabBar::tab:selected {
    background: transparent;
    border: none;
}
QTabBar::tab:!selected {
    background: transparent;
    border: none;
}
QTabBar::tab:hover {
    background: transparent;
    color: inherit;
    border: none;
}

QTabBar::close-button {
    subcontrol-origin: padding;
    subcontrol-position: right;
    image: url(none);
    background: transparent;
    color: #344955;
    border: none;
    border-radius: 8px;
    width: 18px;
    height: 18px;
    margin-left: 4px;
    margin-right: 2px;
    font-size: 16px;
}

QTabBar::close-button:hover {
    background: #e57373;
    color: #fff;
}
"""


FONT_DROPDOWN_STYLE = """
    QFontComboBox {
        background-color: #282c34;
        color: #f8f8f2;
        border: 1px solid #44475a;
    }
    QFontComboBox QAbstractItemView {
        background-color: #232629;
        color: #f8f8f2;
        selection-background-color: #44475a;
        selection-color: #ffffff;
    }
"""
SETTINGS_STYLE ="""
    QDialog {
        background-color:  #2e2f3e;
        color: #f8f8f2;
    }
    QLabel {
        color: #f8f8f2;
    }
    QSpinBox, QFontComboBox, QHBoxLayout, QFontComboBox {
        background-color:  #2e2f3e;
        color: #f8f8f2;
        border: 1px solid #44475a;
    }
    QPushButton {
    background-color: #5c5f77;
    color: #ffffff;
    border: 1px solid #35374b;
    border-radius: 5px;
    padding: 5px;
}
    QPushButton:hover {
    background-color: #6d6f8a;
    border: 1px solid #ffffff;
}
"""

COMPLETION_POPUP_STYLE = """
            QListWidget {
                background: #23272e;
                color: #e6e6e6;
                border: 1px solid #444;
                border-radius: 6px;
                font-size: 14px;
                padding: 4px 0;
                selection-background-color: #3d4250;
                selection-color: #ffffff;
            }
            QListWidget::item {
                padding: 6px 16px;
                border: none;
            }
            QListWidget::item:selected {
                background: #3d4250;
                color: #ffffff;
            }
            QListWidget::item:hover {
                background: #2a2f3a;
                color: #ffffff;
            }"""