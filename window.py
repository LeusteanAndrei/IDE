from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QProcess
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QSplitter
from FileSystem.folder_open import initialize_sidebar_and_splitter
from FileSystem.file_methods import save_as_file
from Styles import style
import os, subprocess
from PyQt5.QtCore import QTimer
from Code_Runner import Code_Runner, Input, Output

import File_Tab, editor


class Ui_MainWindow(QtCore.QObject):

    def add_sections(self):
                # Sections (Zona 1)
        self.sectionLayout = QtWidgets.QHBoxLayout()
        self.sections = []

        # Section names
        self.section_names = [
            "Logo", "File", "Edit", "View", "Navigate", 
            "Code", "Tools", "Run", "Window", "Help"
        ]

        # Bbutton for each section
        for name in self.section_names:
            button = QtWidgets.QPushButton(name)
            button.setObjectName(name)
            self.sections.append(button)
            self.sectionLayout.addWidget(button)

    def add_algorithms_menu(self, MainWindow):
        self.fileMenu = QtWidgets.QMenu()
        self.actionNewFile = QtWidgets.QAction(MainWindow)
        self.actionNewFile.setObjectName("actionNewFile")
        self.actionOpenFile = QtWidgets.QAction(MainWindow)
        self.actionOpenFile.setObjectName("actionOpenFile")
        self.actionSaveFile = QtWidgets.QAction(MainWindow)
        self.actionSaveFile.setObjectName("actionSaveFile")
        self.actionSaveFileAs = QtWidgets.QAction(MainWindow)
        self.actionSaveFileAs.setObjectName("actionSaveFileAs")
        self.actionOpenFolder = QtWidgets.QAction(MainWindow)
        self.actionOpenFolder.setObjectName("actionOpenFolder")

        self.fileMenu.addAction(self.actionNewFile)
        self.fileMenu.addAction(self.actionOpenFile)
        self.fileMenu.addAction(self.actionSaveFile)
        self.fileMenu.addAction(self.actionSaveFileAs)
        self.fileMenu.addAction(self.actionOpenFolder)

        #Alg de Sortare
        self.algorithmsMenu = QtWidgets.QMenu()
        self.menuSorting = QtWidgets.QMenu("Sorting", self.algorithmsMenu)
        self.actionBubbleSort = QtWidgets.QAction(MainWindow)
        self.actionBubbleSort.setObjectName("actionBubbleSort")
        self.actionInsertionSort = QtWidgets.QAction(MainWindow)
        self.actionInsertionSort.setObjectName("actionInsertionSort")
        self.actionQuickSort = QtWidgets.QAction(MainWindow)
        self.actionQuickSort.setObjectName("actionQuickSort")
        self.actionMergeSort = QtWidgets.QAction(MainWindow)
        self.actionMergeSort.setObjectName("actionMergeSort")
        self.menuSorting.addAction(self.actionBubbleSort)
        self.menuSorting.addAction(self.actionInsertionSort)
        self.menuSorting.addAction(self.actionQuickSort)
        self.menuSorting.addAction(self.actionMergeSort)

        #Alg de Cautare
        self.menuSearching = QtWidgets.QMenu("Searching", self.algorithmsMenu)
        self.actionBinarySearch = QtWidgets.QAction(MainWindow)
        self.actionBinarySearch.setObjectName("actionBinarySearch")
        self.actionLinearSearch = QtWidgets.QAction(MainWindow)
        self.actionLinearSearch.setObjectName("actionLinearSearch")
        self.menuSearching.addAction(self.actionBinarySearch)
        self.menuSearching.addAction(self.actionLinearSearch)

        #Structuri de Date
        self.menuDataStructures = QtWidgets.QMenu("Data Structures", self.algorithmsMenu)
        self.actionLinkedList = QtWidgets.QAction(MainWindow)
        self.actionLinkedList.setObjectName("actionLinkedList")
        self.actionStack = QtWidgets.QAction(MainWindow)
        self.actionStack.setObjectName("actionStack")
        self.actionQueue = QtWidgets.QAction(MainWindow)
        self.actionQueue.setObjectName("actionQueue")
        self.menuDataStructures.addAction(self.actionLinkedList)
        self.menuDataStructures.addAction(self.actionStack)
        self.menuDataStructures.addAction(self.actionQueue)

        #Alg de Grafuri
        self.menuGraphAlgorithms = QtWidgets.QMenu("Graph Algorithms", self.algorithmsMenu)
        self.actionBFS = QtWidgets.QAction(MainWindow)
        self.actionBFS.setObjectName("actionBFS")
        self.actionDFS = QtWidgets.QAction(MainWindow)
        self.actionDFS.setObjectName("actionDFS")
        self.menuGraphAlgorithms.addAction(self.actionBFS)
        self.menuGraphAlgorithms.addAction(self.actionDFS)

        #Alg de Programare Dinamica
        self.menuDynamicProgramming = QtWidgets.QMenu("Dynamic Programming", self.algorithmsMenu)
        self.actionFibonacci = QtWidgets.QAction(MainWindow)
        self.actionFibonacci.setObjectName("actionFibonacci")
        self.actionKnapsack = QtWidgets.QAction(MainWindow)
        self.actionKnapsack.setObjectName("actionKnapsack")
        self.menuDynamicProgramming.addAction(self.actionFibonacci)
        self.menuDynamicProgramming.addAction(self.actionKnapsack)

        #Alg Diversi
        self.menuOther = QtWidgets.QMenu("Other", self.algorithmsMenu)
        self.actionPrimeCheck = QtWidgets.QAction(MainWindow)
        self.actionPrimeCheck.setObjectName("actionPrimeCheck")
        self.actionGCD = QtWidgets.QAction(MainWindow)
        self.actionGCD.setObjectName("actionGCD")
        self.menuOther.addAction(self.actionPrimeCheck)
        self.menuOther.addAction(self.actionGCD)

        # Add submenus to the Algorithms menu
        self.algorithmsMenu.addMenu(self.menuSorting)
        self.algorithmsMenu.addMenu(self.menuSearching)
        self.algorithmsMenu.addMenu(self.menuDataStructures)
        self.algorithmsMenu.addMenu(self.menuGraphAlgorithms)
        self.algorithmsMenu.addMenu(self.menuDynamicProgramming)
        self.algorithmsMenu.addMenu(self.menuOther)

    def connect_buttons(self):
        for button in self.sections:
            if button.objectName() == "File":
                button.setMenu(self.fileMenu)
            elif button.objectName() == "Code":
                button.setMenu(self.algorithmsMenu)

    def setup_buttons(self):
        # Shortcut Buttons (Area 2)
        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.buttons = []

        for i in range(1, 6):
            button = QtWidgets.QPushButton(str(i))  # momentan e doar nr ca placeholder
            self.buttons.append(button)
            self.buttonLayout.addWidget(button)

        # Adaugare spatiu (nu intrebati ce inseamna paramaetrii aia)
        self.buttonLayout.addItem(QtWidgets.QSpacerItem(50, 50, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum))

        for i in range(6, 8):
            button = QtWidgets.QPushButton(str(i))  # Button text as placeholder
            self.buttons.append(button)
            self.buttonLayout.addWidget(button)

        self.buttonLayout.addItem(QtWidgets.QSpacerItem(50, 50, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum))

        for i in range(8, 14):
            button = QtWidgets.QPushButton(str(i))  # Button text as placeholder
            self.buttons.append(button)
            self.buttonLayout.addWidget(button)

        self.buttonLayout.addItem(QtWidgets.QSpacerItem(50, 50, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum))

        #Butonul de AI Assistant - sincer cam confusing ca asta e butonul 20 si e de fapt buttons[14] da am zis sa fie ca in poza anitei
        button = QtWidgets.QPushButton('20')  # Button text as placeholder
        self.buttons.append(button)
        self.buttonLayout.addWidget(button)
        self.buttonLayout.addItem(QtWidgets.QSpacerItem(50, 50, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum))

        for i in range(14, 18):
            button = QtWidgets.QPushButton(str(i))  # Button text as placeholder
            self.buttons.append(button)
            self.buttonLayout.addWidget(button)
        self.buttonLayout.addItem(QtWidgets.QSpacerItem(50, 50, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum))
        
        for i in range(18, 20):
            button = QtWidgets.QPushButton(str(i))  # Button text as placeholder
            self.buttons.append(button)
            self.buttonLayout.addWidget(button)
        
        # Add the button layout to the grid
        self.gridLayout.addLayout(self.buttonLayout, 1, 0, 1, 2)

        self.buttons[17].clicked.connect(self.code_runner.abort_run)

    def setupUi(self, MainWindow):
 
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")


        self.add_sections()  # Call the method to add sections
        self.code_runner = Code_Runner(self)  
        self.add_algorithms_menu(MainWindow)  # Call the method to add algorithms menu
        self.connect_buttons()  # Call the method to connect buttons



        # Add the section layout to the grid
        #aicea va zic sincer ca m am folosit de copilot si nu sunt chiar sigur cum functioneaza grid-ul
        self.gridLayout.addLayout(self.sectionLayout, 0, 0, 1, 2)


        #Shortcut Buttons (Area 2)
        self.setup_buttons()


        self.file_tab_bar = File_Tab.File_Tab_Bar(ui = self)  # Use the custom tab bar class

         #Editor (Zona 4) - legat si de file navigator - Zona 3
        self.plainTextEdit = editor.Editor() 

        self.editor_layout = QtWidgets.QVBoxLayout()
        self.editor_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        self.editor_layout.setSpacing(0)  # Remove spacing
        self.editor_layout.addWidget(self.file_tab_bar)
        self.editor_layout.addWidget(self.plainTextEdit)


        self.editor_container = QtWidgets.QWidget() #container ca file bar sa fie doar deasupra editorului, nu si deasupra sidebar-ului cand e deschis
        self.editor_container.setLayout(self.editor_layout)
        self.editor_container.plainTextEdit = self.plainTextEdit  # Store reference to plainTextEdit

        self.splitter, self.tree_view, self.file_model = initialize_sidebar_and_splitter(self.editor_container,self) #functia din folder_open.py care initializeaza sidebar-ul si splitter-ul
        self.splitter.setSizes([250, 950])
        self.gridLayout.addWidget(self.splitter, 2, 0, 1, 2)  # Add splitter to the grid layout

        self.terminal = File_Tab.Terminal( ui = self)  # Use the custom terminal class
        self.terminal.installEventFilter(self)  # Install event filter for terminal input handling


        self.tab_widget = QtWidgets.QTabWidget()
        self.tab_widget.setObjectName("tab_widget")
        self.tab_widget.addTab(self.terminal, "Terminal")
        self.tab_widget.addTab(self.code_runner.input, "Input")
        self.tab_widget.addTab(self.code_runner.output, "Output")
        self.tab_widget.setTabVisible(2, False)

        self.terminal_splitter = QSplitter(Qt.Vertical) #aici ar trebui sa functioneze splitterul la fel ca in cazul file navigator doar ca pe vertical
        self.terminal_splitter.addWidget(self.splitter) #in orice caz e destul de glitched so idk if im doing it right
        self.terminal_splitter.addWidget(self.tab_widget) #am separat terminal (zona 5) de splitterul anterior (zonele 3+4)
        # self.terminal_splitter.setSizes([1, 4])
        self.terminal_splitter.setSizes([1000, 100])


        self.gridLayout.addWidget(self.terminal_splitter, 2, 0, 1, 2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    
    #Functiile Handler pt functiile din FileSystem/file_methods.py
    def handle_new_file(self):
        """Handle the New File action."""
        import FileSystem.file_methods as fm

        # Call the new_file function to create a new file
        new_file_name = fm.new_file(self.plainTextEdit.text_edit)

        if new_file_name:
            # Check if the file is already opened
            if new_file_name not in self.file_tab_bar.opened_files:
                # Add the file to the opened files list
                self.file_tab_bar.opened_files.append(new_file_name)

                # Add a new tab to the file_tab_bar
                self.file_tab_bar.addTab(new_file_name)

                # Initialize the file state
                self.file_tab_bar.file_states[len(self.file_tab_bar.opened_files) - 1] = {
                    "file_path": new_file_name,
                    "saved": False
                }


                # Switch to the new tab
                self.file_tab_bar.setCurrentIndex(len(self.file_tab_bar.opened_files) - 1)

    def handle_open_file(self):
        """Handle the Open File action."""
        import FileSystem.file_methods as fm

        # Call the open_file function and get the file path
        file_path = fm.open_file(self.plainTextEdit.text_edit)

        if file_path:
            # Check if the file is already opened
            if file_path not in self.file_tab_bar.opened_files:
                # Add the file to the opened files list
                self.file_tab_bar.opened_files.append(file_path)

                # Add a new tab to the file_tab_bar
                self.file_tab_bar.addTab(os.path.basename(file_path))

                # Initialize the file state
                self.file_tab_bar.file_states[len(self.file_tab_bar.opened_files) - 1] = {
                    "file_path": file_path,
                    "saved": True
                }

                # Switch to the newly opened tab
                self.file_tab_bar.setCurrentIndex(len(self.file_tab_bar.opened_files) - 1)
            else:
                # If the file is already opened, switch to its tab
                index = self.file_tab_bar.opened_files.index(file_path)
                self.file_tab_bar.setCurrentIndex(index)

    def handle_save_file(self):
        """Handle the Save File action."""
        import FileSystem.file_methods as fm

        current_index = self.file_tab_bar.currentIndex()
        file_state = self.file_tab_bar.file_states[current_index]

        # Call the save_file function
        file_path, saved = fm.save_file(
            self.plainTextEdit.text_edit,
            file_state["file_path"],
            file_state["saved"],
            self.plainTextEdit.highlighter
        )

        # Update the file state
        self.file_tab_bar.file_states[current_index]["file_path"] = file_path
        self.file_tab_bar.file_states[current_index]["saved"] = saved

    def handle_save_file_as(self):
        """Handle the Save File As action."""
        import FileSystem.file_methods as fm

        current_index = self.file_tab_bar.currentIndex()
        file_state = self.file_tab_bar.file_states[current_index]

        # Call the save_as_file function
        file_path, saved = fm.save_as_file(
            self.plainTextEdit.text_edit,
            file_state["file_path"]
        )

        # Update the file state
        self.file_tab_bar.file_states[current_index]["file_path"] = file_path
        self.file_tab_bar.file_states[current_index]["saved"] = saved

        # Update the tab name
        self.file_tab_bar.setTabText(current_index, os.path.basename(file_path))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "C++ IDE"))
        # Set menu titles (for algorithms)
        self.algorithmsMenu.setTitle(_translate("MainWindow", "Algorithms"))
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

        #Set menu titles (for files)
        self.fileMenu.setTitle(_translate("MainWindow", "File"))
        self.actionNewFile.setText(_translate("MainWindow", "New File"))
        self.actionOpenFile.setText(_translate("MainWindow", "Open File"))
        self.actionSaveFile.setText(_translate("MainWindow", "Save File"))
        self.actionSaveFileAs.setText(_translate("MainWindow", "Save File As"))
        self.actionOpenFolder.setText(_translate("MainWindow", "Open Folder"))

    def eventFilter(self, obj, event):
        if obj == self.terminal :
            self.terminal.handle_event(event)
        return super().eventFilter(obj, event)




    #Asta ar fi trebuit sa fie o functie care sa te impiedice sa stergi chestiile din terminal gen path-ul sau comenzile rulate anterior
    #pt ca momentan "terminalul" asta e doar un glorified text editor si practic poti sa iti cam bati joc de el
    # def keyPressEvent(self, event):
    #     cursor = self.terminal.textCursor()
    #     cursor.movePosition(QTextCursor.StartOfBlock, QTextCursor.KeepAnchor)
    #     current_line = cursor.selectedText()

    #     # Prevent editing the prompt or previous commands
    #     if not current_line.startswith(f"{self.current_directory}> "):
    #         event.ignore()
    #         return

    #     # Allow typing only after the prompt
    #     if event.key() in (Qt.Key_Backspace, Qt.Key_Delete):
    #         if cursor.positionInBlock() <= len(f"{self.current_directory}> "):
    #             event.ignore()
    #             return

    #     super(QtWidgets.QPlainTextEdit, self.terminal).keyPressEvent(event)
