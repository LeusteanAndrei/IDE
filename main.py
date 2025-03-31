from window import *
import sys
from Highlighter.highlighter import cPlusPlusHighlighter
from algorithms import ALGORITHMS


def insert_algorithm(editor, algorithm_code):
    """Insert algorithm code at the current cursor position in the editor"""
    cursor = editor.textCursor()
    cursor.insertText(algorithm_code)
    editor.setTextCursor(cursor)


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
    
    editor.show()
    sys.exit(app.exec_())
