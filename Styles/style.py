#Aici sunt instructiunile de css pentru styling - specific intr-o variabile stilurile dorite pt anumite widget-uri
#si dupa in main pasez variabila corespunzatoare cu setStyleSheet()

EDITOR_STYLE = """
QPlainTextEdit {
    background-color: white;
    color: #70947c;
    font-size: 22px;
    border: 1px solid #5c5f77;
    border-radius: 5px;
    padding: 5px;
}

QPlainTextEdit:hover {
    border: 1px solid #ffffff;
}
"""

MAIN_WINDOW_STYLE = """
QMainWindow {
    background-color: #2e2f3e;
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

# Style for grid layouts (if needed for widgets)
GRID_LAYOUT_STYLE = """
QWidget {
    background-color: #2e2f3e;
    color: #ffffff;
}
"""

EDITOR_FONT_SIZE = 20

PLACEHOLDER_STYLE = """
QLabel {
    background-color: #d3d3d3;
    border: 1px solid #000;
    font-size: 14px;
    color: #000;
}
QTreeView {
    background-color: #d3d3d3;
    border: 1px solid #000;
    font-size: 14px;
    color: #000;
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
    background-color: #35374b;
    color: #70947c;
    font-size: 14px;
    border: 1px solid #5c5f77;
    border-radius: 5px;
    padding: 5px;
}
"""