from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):

        screenSize = QtWidgets.QDesktopWidget().screenGeometry()
        screenWidth = screenSize.width()
        screenHeight = screenSize.height()

        MainWindow.showMaximized()

        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        # MainWindow.resize(screenWidth, screenHeight)
        # MainWindow.resize(1105, 632)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setGeometry(QtCore.QRect(50, 0, screenWidth - 100, screenHeight - 100))
        # self.plainTextEdit.setGeometry(QtCore.QRect(50, 0, 1051, 571))
        self.plainTextEdit.setObjectName("plainTextEdit")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1105, 26))
        self.menubar.setObjectName("menubar")
        
        # Add Algorithm menu
        self.menuAlgorithms = QtWidgets.QMenu(self.menubar)
        self.menuAlgorithms.setObjectName("menuAlgorithms")
        
        # Add sub-menus for each algorithm category
        self.menuSorting = QtWidgets.QMenu(self.menuAlgorithms)
        self.menuSorting.setObjectName("menuSorting")
        
        self.menuSearching = QtWidgets.QMenu(self.menuAlgorithms)
        self.menuSearching.setObjectName("menuSearching")
        
        self.menuDataStructures = QtWidgets.QMenu(self.menuAlgorithms)
        self.menuDataStructures.setObjectName("menuDataStructures")
        
        self.menuGraphAlgorithms = QtWidgets.QMenu(self.menuAlgorithms)
        self.menuGraphAlgorithms.setObjectName("menuGraphAlgorithms")
        
        self.menuDynamicProgramming = QtWidgets.QMenu(self.menuAlgorithms)
        self.menuDynamicProgramming.setObjectName("menuDynamicProgramming")
        
        self.menuOther = QtWidgets.QMenu(self.menuAlgorithms)
        self.menuOther.setObjectName("menuOther")
        
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        
        # Add the Algorithm menu to the menu bar
        self.menubar.addAction(self.menuAlgorithms.menuAction())
        
        # Add the category sub-menus to the Algorithm menu
        self.menuAlgorithms.addAction(self.menuSorting.menuAction())
        self.menuAlgorithms.addAction(self.menuSearching.menuAction())
        self.menuAlgorithms.addAction(self.menuDataStructures.menuAction())
        self.menuAlgorithms.addAction(self.menuGraphAlgorithms.menuAction())
        self.menuAlgorithms.addAction(self.menuDynamicProgramming.menuAction())
        self.menuAlgorithms.addAction(self.menuOther.menuAction())
        
        # Create actions for algorithms (we'll connect these in main.py)
        self.actionBubbleSort = QtWidgets.QAction(MainWindow)
        self.actionBubbleSort.setObjectName("actionBubbleSort")
        self.actionInsertionSort = QtWidgets.QAction(MainWindow)
        self.actionInsertionSort.setObjectName("actionInsertionSort")
        self.actionQuickSort = QtWidgets.QAction(MainWindow)
        self.actionQuickSort.setObjectName("actionQuickSort")
        self.actionMergeSort = QtWidgets.QAction(MainWindow)
        self.actionMergeSort.setObjectName("actionMergeSort")
        
        self.actionBinarySearch = QtWidgets.QAction(MainWindow)
        self.actionBinarySearch.setObjectName("actionBinarySearch")
        self.actionLinearSearch = QtWidgets.QAction(MainWindow)
        self.actionLinearSearch.setObjectName("actionLinearSearch")
        
        self.actionLinkedList = QtWidgets.QAction(MainWindow)
        self.actionLinkedList.setObjectName("actionLinkedList")
        self.actionStack = QtWidgets.QAction(MainWindow)
        self.actionStack.setObjectName("actionStack")
        self.actionQueue = QtWidgets.QAction(MainWindow)
        self.actionQueue.setObjectName("actionQueue")
        
        self.actionBFS = QtWidgets.QAction(MainWindow)
        self.actionBFS.setObjectName("actionBFS")
        self.actionDFS = QtWidgets.QAction(MainWindow)
        self.actionDFS.setObjectName("actionDFS")
        
        self.actionFibonacci = QtWidgets.QAction(MainWindow)
        self.actionFibonacci.setObjectName("actionFibonacci")
        self.actionKnapsack = QtWidgets.QAction(MainWindow)
        self.actionKnapsack.setObjectName("actionKnapsack")
        
        self.actionPrimeCheck = QtWidgets.QAction(MainWindow)
        self.actionPrimeCheck.setObjectName("actionPrimeCheck")
        self.actionGCD = QtWidgets.QAction(MainWindow)
        self.actionGCD.setObjectName("actionGCD")
        
        # Add actions to their respective menus
        self.menuSorting.addAction(self.actionBubbleSort)
        self.menuSorting.addAction(self.actionInsertionSort)
        self.menuSorting.addAction(self.actionQuickSort)
        self.menuSorting.addAction(self.actionMergeSort)
        
        self.menuSearching.addAction(self.actionBinarySearch)
        self.menuSearching.addAction(self.actionLinearSearch)
        
        self.menuDataStructures.addAction(self.actionLinkedList)
        self.menuDataStructures.addAction(self.actionStack)
        self.menuDataStructures.addAction(self.actionQueue)
        
        self.menuGraphAlgorithms.addAction(self.actionBFS)
        self.menuGraphAlgorithms.addAction(self.actionDFS)
        
        self.menuDynamicProgramming.addAction(self.actionFibonacci)
        self.menuDynamicProgramming.addAction(self.actionKnapsack)
        
        self.menuOther.addAction(self.actionPrimeCheck)
        self.menuOther.addAction(self.actionGCD)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "C++ IDE"))
        
        # Set menu titles
        self.menuAlgorithms.setTitle(_translate("MainWindow", "Algorithms"))
        self.menuSorting.setTitle(_translate("MainWindow", "Sorting"))
        self.menuSearching.setTitle(_translate("MainWindow", "Searching"))
        self.menuDataStructures.setTitle(_translate("MainWindow", "Data Structures"))
        self.menuGraphAlgorithms.setTitle(_translate("MainWindow", "Graph Algorithms"))
        self.menuDynamicProgramming.setTitle(_translate("MainWindow", "Dynamic Programming"))
        self.menuOther.setTitle(_translate("MainWindow", "Other"))
        
        # Set action titles
        self.actionBubbleSort.setText(_translate("MainWindow", "Bubble Sort"))
        self.actionInsertionSort.setText(_translate("MainWindow", "Insertion Sort"))
        self.actionQuickSort.setText(_translate("MainWindow", "Quick Sort"))
        self.actionMergeSort.setText(_translate("MainWindow", "Merge Sort"))
        
        self.actionBinarySearch.setText(_translate("MainWindow", "Binary Search"))
        self.actionLinearSearch.setText(_translate("MainWindow", "Linear Search"))
        
        self.actionLinkedList.setText(_translate("MainWindow", "Linked List"))
        self.actionStack.setText(_translate("MainWindow", "Stack"))
        self.actionQueue.setText(_translate("MainWindow", "Queue"))
        
        self.actionBFS.setText(_translate("MainWindow", "BFS"))
        self.actionDFS.setText(_translate("MainWindow", "DFS"))
        
        self.actionFibonacci.setText(_translate("MainWindow", "Fibonacci"))
        self.actionKnapsack.setText(_translate("MainWindow", "Knapsack"))
        
        self.actionPrimeCheck.setText(_translate("MainWindow", "Prime Check"))
        self.actionGCD.setText(_translate("MainWindow", "GCD"))


# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     MainWindow = QtWidgets.QMainWindow()
#     ui = Ui_MainWindow()
#     ui.setupUi(MainWindow)
#     MainWindow.show()
#     editor = ui.plainTextEdit

#     from Highlighter.highlighter import cPlusPlusHighlighter


#     # editor.setPlainText(" ".join(cPlusPlusHighlighter.operators) + "\n" +
#     #                     " ".join(cPlusPlusHighlighter.braces) + "\n" +
#     #                     " ".join(cPlusPlusHighlighter.keywords) + "\n"
#     #                     +"this" + "\n" +
#     #                     "class nume_clasa" + "\n" 
#     #                     +"0x123456789ABCDEF" + "\n" +
#     #                     "0b1010101010101" + "\n" +
#     #                     "167.386516358618" + "\n" +
#     #                     "167.386516358618e+12" + "\n" +
#     #                     "167.386516358618e-12" + "\n" +
#     #                     "+123123132434525"+ "\n" +
#     #                     "-123123132434525"+ "\n" 
#     #                     +"\\\\ifwa7f9a7f bfq i34fi1bq346fg 91374tiawdjawwgyfgq" + "\n" +
#     #                     "\"string\""+ "\n" +
#     #                     "'char'" + "\n"     
#     #                     )
#     editor.setStyleSheet("background-color: lightgray;")
#     font = editor.font()
#     font.setPointSize(20)  # Set the desired font size
#     editor.setFont(font)    
#     highlighter = cPlusPlusHighlighter(editor.document())
#     editor.show()
#     sys.exit(app.exec_())
