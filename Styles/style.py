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

FILE_TAB_STYLE = """ 
QTabWidget::pane { /* The tab widget frame */
    background: #35374b;
    border: none; /* Remove the border around the tab bar */
    margin-left: 10px; /* Add left margin to align with the editor */
}

QTabBar::tab {
    background: #35374b;
    color: #ffffff;
    padding: 5px 10px; /* Adjust padding for better spacing */
    margin: 0px; /* Remove margin between tabs */
    border-radius: 3px; /* Slightly rounded corners */
    width: 120px; /* Fixed width for tabs */
}

QTabBar::tab:selected { /* Style for the selected tab */
    background: #5c5f77;
    color: #ffffff;
}

QTabBar::tab:hover { /* Style for hover effect */
    background: #4a4d63;
    color: #ffffff;
}

QTabBar::close-button {
    background: #5c5f77; /* Gray background for visibility */
    content: "X"; 
    color: #ffffff; /* White "X" text */
    border: none; /* Remove border */
    border-radius: 3px; /* Match tab corners */
    width: 16px; /* Fixed size for the close button */
    height: 16px;
    margin: 0px; /* Align with the tab */
    text-align: center; /* Center the "X" */
    font-size: 12px; /* Adjust font size */
}

QTabBar::close-button:hover {
    background: #4a4d63; /* Darker gray on hover */
    color: #ffffff;
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