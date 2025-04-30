from window import *
import sys
from Highlighter.highlighter import cPlusPlusHighlighter
from algorithms import ALGORITHMS
from FileSystem.file_methods import *
from shortcuts import ShortcutManager
from FileSystem.folder_open import initialize_sidebar_and_splitter, open_folder
from Styles import style
from Functions.toggle_terminal import toggle_terminal

def insert_algorithm(editor, algorithm_code):
    """Insert algorithm code at the current cursor position in the editor"""
    cursor = editor.textCursor()
    cursor.insertText(algorithm_code)
    editor.setTextCursor(cursor)

def get_current_editor(tab_widget): #asta e pt ca am incercat sa fac posibilitatea de a avea mai multe taburi deschise - momentan a fost cam fail
    """Get the current editor from the active tab"""
    return tab_widget.currentWidget()

if __name__ == "__main__":
    # f = open("testingCode.cpp", "r")
    # testText = f.readlines()
    # test = "".join(testText)
    # f.close()

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    MainWindow.setStyleSheet(style.MAIN_WINDOW_STYLE)
    MainWindow.show()

    # pe aici am aplicat styling-ul ala mizerabil
    ui.tree_view.setStyleSheet(style.PLACEHOLDER_STYLE)
    ui.terminal.setStyleSheet(style.PLACEHOLDER_STYLE)

    for button in ui.buttons:
        button.setStyleSheet(style.BUTTON_STYLE)

    ui.buttons[19].clicked.connect(lambda: toggle_terminal(ui.terminal, ui.terminal_splitter)) #terminal toggle button (ultimul din zona 2)

    editor = ui.plainTextEdit.text_edit
    # editor.setPlainText(test)
    

    editor.setStyleSheet(style.EDITOR_STYLE)
    # editor.setStyleSheet()
    font = editor.font()
    font.setPointSize(style.EDITOR_FONT_SIZE)
    editor.setFont(font)    
    highlighter = cPlusPlusHighlighter(ui.plainTextEdit, editor.document())
    ui.plainTextEdit.highlighter = highlighter

    ui.terminal.setStyleSheet(style.TERMINAL_STYLE)
    
    #DISCLAIMER LIST (vai mama mea)
    #1. Terminalul odata ascuns nu mai reuseste sa fie afisat - de aia il si las not hidden initial ca macar sa se vada si sa poata fi testat:))
    #2. Also terminaul se suprapune peste editor si orice am incercat nu am reusit sa il fac sa stea in continuarea lui (cum e la file explorer de ex)
    #3. Din cauza asta de multe ori lucrurile se glitch-uiesc si nu se mai vede tot codul din editor - daca fac fereasta minimized si dupa maximized iar in general isi revine
    #4. A da si in minimized terminalul nici macar nu apare :( (mai vezi alte precizari legate de terminal si in windows.py la declararea lui)


    # Initialize the ShortcutManager - see the shortcuts.py file for more details :)
    shortcut_manager = ShortcutManager(MainWindow)
    
    # Add shortcuts with descriptive names and default key sequences
    shortcut_manager.add_shortcut("New File", "Ctrl+N", lambda: new_file(editor))
    shortcut_manager.add_shortcut("Open File", "Ctrl+O", lambda: open_file(editor))
    shortcut_manager.add_shortcut("Save File", "Ctrl+S", lambda: save_file(editor))
    shortcut_manager.add_shortcut("Save File As", "Ctrl+Shift+S", lambda: save_as_file(editor))
    shortcut_manager.add_shortcut("Open Folder", "Ctrl+K", lambda: open_folder(ui.file_model, ui.tree_view))
    shortcut_manager.add_shortcut("Run Code", "F5", lambda: ui.run_code())
    
    # Connect button 1 to open the shortcut settings dialog
    ui.buttons[0].setText("Shortcuts")
    ui.buttons[0].setToolTip("Configure keyboard shortcuts")
    ui.buttons[0].clicked.connect(shortcut_manager.show_config_dialog)
    
    # Connect algorithm actions to their respective functions
    # Sorting algorithms
    ui.actionBubbleSort.triggered.connect(
        lambda: insert_algorithm(editor, ALGORITHMS["Sorting"]["Bubble Sort"]))
    ui.actionInsertionSort.triggered.connect(
        lambda: insert_algorithm(editor, ALGORITHMS["Sorting"]["Insertion Sort"]))
    ui.actionQuickSort.triggered.connect(
        lambda: insert_algorithm(editor, ALGORITHMS["Sorting"]["Quick Sort"]))
    ui.actionMergeSort.triggered.connect(
        lambda: insert_algorithm(editor, ALGORITHMS["Sorting"]["Merge Sort"]))
    
    # Searching algorithms
    ui.actionBinarySearch.triggered.connect(
        lambda: insert_algorithm(editor, ALGORITHMS["Searching"]["Binary Search"]))
    ui.actionLinearSearch.triggered.connect(
        lambda: insert_algorithm(editor, ALGORITHMS["Searching"]["Linear Search"]))
    
    # Data structures
    ui.actionLinkedList.triggered.connect(
        lambda: insert_algorithm(editor, ALGORITHMS["Data Structures"]["Linked List"]))
    ui.actionStack.triggered.connect(
        lambda: insert_algorithm(editor, ALGORITHMS["Data Structures"]["Stack"]))
    ui.actionQueue.triggered.connect(
        lambda: insert_algorithm(editor, ALGORITHMS["Data Structures"]["Queue"]))
    
    # Graph algorithms
    ui.actionBFS.triggered.connect(
        lambda: insert_algorithm(editor, ALGORITHMS["Graph Algorithms"]["BFS"]))
    ui.actionDFS.triggered.connect(
        lambda: insert_algorithm(editor, ALGORITHMS["Graph Algorithms"]["DFS"]))
    
    # Dynamic programming
    ui.actionFibonacci.triggered.connect(
        lambda: insert_algorithm(editor, ALGORITHMS["Dynamic Programming"]["Fibonacci"]))
    ui.actionKnapsack.triggered.connect(
        lambda: insert_algorithm(editor, ALGORITHMS["Dynamic Programming"]["Knapsack"]))
    
    # Other algorithms
    ui.actionPrimeCheck.triggered.connect(
        lambda: insert_algorithm(editor, ALGORITHMS["Other"]["Prime Check"]))
    ui.actionGCD.triggered.connect(
        lambda: insert_algorithm(editor, ALGORITHMS["Other"]["GCD"]))
    

    # Connect Files actions to their respective functions
    ui.actionNewFile.triggered.connect(
        lambda: new_file(editor)
    )
    ui.actionOpenFile.triggered.connect(
        lambda: open_file(editor)
    )
    ui.actionSaveFile.triggered.connect(
        lambda: save_file(editor)
    )
    ui.actionSaveFileAs.triggered.connect(
        lambda: save_as_file(editor)
    )
    ui.actionOpenFolder.triggered.connect(
        lambda: (open_folder(ui.file_model, ui.tree_view), ui.tree_view.show())
    )

    editor.show()
    sys.exit(app.exec_())
