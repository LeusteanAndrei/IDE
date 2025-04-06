from window import *
import sys
from Highlighter.highlighter import cPlusPlusHighlighter
from algorithms import ALGORITHMS
from file_methods import *
from shortcuts import ShortcutManager
from folder_open import initialize_sidebar_and_splitter, open_folder

def insert_algorithm(editor, algorithm_code):
    """Insert algorithm code at the current cursor position in the editor"""
    cursor = editor.textCursor()
    cursor.insertText(algorithm_code)
    editor.setTextCursor(cursor)

def get_current_editor(tab_widget): #asta e pt ca am incercat sa fac posibilitatea de a avea mai multe taburi deschise - momentan a fost cam fail
    """Get the current editor from the active tab"""
    return tab_widget.currentWidget()

if __name__ == "__main__":
    f = open("testingCode.cpp", "r")
    testText = f.readlines()
    test = "".join(testText)
    f.close()

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    editor = ui.plainTextEdit
    editor.setPlainText(test)

    editor.setStyleSheet("background-color: lightgray;")
    font = editor.font()
    font.setPointSize(20)
    editor.setFont(font)    
    highlighter = cPlusPlusHighlighter(editor.document())
    
    #Sidebar and splitter initialization for opening folders
    splitter, tree_view, file_model = initialize_sidebar_and_splitter(MainWindow, editor)

    # Initialize the ShortcutManager - see the shortcuts.py file for more details :)
    shortcut_manager = ShortcutManager(MainWindow)
    # Add shortcuts
    shortcut_manager.add_shortcut("Ctrl+S", lambda: save_file(editor))
    shortcut_manager.add_shortcut("Ctrl+N", lambda: new_file(editor))
    
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
        lambda: open_folder(file_model, tree_view)
    )

    editor.show()
    sys.exit(app.exec_())
