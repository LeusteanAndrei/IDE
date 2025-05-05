from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QProcess
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QSplitter
from FileSystem.folder_open import initialize_sidebar_and_splitter
from FileSystem.file_methods import save_as_file
from Styles import style
import os, subprocess

class Ui_MainWindow(QtCore.QObject): #am convertit la chestia asta ca sa mearga terminalul:))
    def setupUi(self, MainWindow):


        # screenSize = QtWidgets.QDesktopWidget().screenGeometry()
        # screenWidth = screenSize.width()
        # screenHeight = screenSize.height()
        # maximizedWidth = screenWidth - 100
        # maximizedHeight = screenHeight - 100

        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")


        # Sections (Zona 1)
        self.sectionLayout = QtWidgets.QHBoxLayout()
        self.sections = []

        # Section names
        section_names = [
            "Logo", "File", "Edit", "View", "Navigate", 
            "Code", "Tools", "Run", "Window", "Help"
        ]

        # Bbutton for each section
        for name in section_names:
            button = QtWidgets.QPushButton(name)
            button.setObjectName(name)
            self.sections.append(button)
            self.sectionLayout.addWidget(button)
        
        #Adaugam functia care ruleaza cod pe butonul de Run
        self.run_button = self.sections[section_names.index("Run")]
        self.run_button.clicked.connect(lambda: self.run_code())

        #In sectiunea de Code am adaugat momentan dropdwon-urile pt algoritmi
        #Sectiuea de File - functiile pt sistemul de fisiere
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

        # Asociere meniuri cu butoanele corespunzatoare
        for button in self.sections:
            if button.objectName() == "File":
                button.setMenu(self.fileMenu)
            elif button.objectName() == "Code":
                button.setMenu(self.algorithmsMenu)


        # Add the section layout to the grid
        #aicea va zic sincer ca m am folosit de copilot si nu sunt chiar sigur cum functioneaza grid-ul
        self.gridLayout.addLayout(self.sectionLayout, 0, 0, 1, 2)


        #Shortcut Buttons (Area 2)
        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.buttons = []

        #le am pus pe bucati ca sa pot sa pun spatiile alea intre grupurile de butoane
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

        #Opened files tab
        #bara unde vor fi afisate fisierle deschise
        self.file_tab_bar = QtWidgets.QTabBar()
        self.file_tab_bar.setObjectName("file_tab_bar")
        self.file_tab_bar.setTabsClosable(True)
        self.file_tab_bar.setMovable(True)
        self.file_tab_bar.setFixedHeight(25)
        self.file_tab_bar.setStyleSheet(style.FILE_TAB_STYLE)
        self.file_tab_bar.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)  # Fix the size
        self.file_tab_bar.setLayoutDirection(Qt.LeftToRight) 

        self.opened_files = []  # Aici ar trebui sa fie adaugate dinamic fisierele deschise
        self.file_states={} #pt a retine care au fost salvate si path-ul lor

         # Cand deschidem editorul, adaugam un tab default numit Untitled
         # ca sa fie rulat codul din el intai ne va obliga sa il salvam
        default_file_name = "Untitled"
        self.file_tab_bar.addTab(default_file_name)
        self.opened_files.append(default_file_name)
        self.file_states[0] = {
            "file_path": None,  # No file path yet
            "saved": False      # File is not saved
        }
        self.file_tab_bar.setCurrentIndex(0)  # Set the default file as the active tab

        # self.file_tab_bar.addTab("filename1.cpp") #astea sunt hardcoded for testing purposes
        # self.file_tab_bar.addTab("filename2.cpp")
        # self.file_tab_bar.addTab("filename3.cpp")

        # Connect the close button signal
        self.file_tab_bar.tabCloseRequested.connect(self.close_tab) #inchidem tab

         #Editor (Zona 4) - legat si de file navigator - Zona 3
        import editor
        self.plainTextEdit = editor.Editor() 
        self.plainTextEdit.setObjectName("plainTextEdit")

        self.editor_layout = QtWidgets.QVBoxLayout()
        self.editor_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        self.editor_layout.setSpacing(0)  # Remove spacing
        self.editor_layout.addWidget(self.file_tab_bar)
        self.editor_layout.addWidget(self.plainTextEdit)

        # self.plainTextEdit.setGeometry(QtCore.QRect(50, 0, screenWidth - 1000, screenHeight - 1000))

        self.editor_container = QtWidgets.QWidget() #container ca file bar sa fie doar deasupra editorului, nu si deasupra sidebar-ului cand e deschis
        self.editor_container.setLayout(self.editor_layout)
        self.editor_container.plainTextEdit = self.plainTextEdit  # Store reference to plainTextEdit
        # self.gridLayout.addWidget(self.plainTextEdit, 2, 0, 1, 2)

        self.splitter, self.tree_view, self.file_model = initialize_sidebar_and_splitter(self.editor_container,self) #functia din folder_open.py care initializeaza sidebar-ul si splitter-ul
        # self.splitter.setSizes([1, 4])
        self.splitter.setSizes([250, 950])
        self.gridLayout.addWidget(self.splitter, 2, 0, 1, 2)  # Add splitter to the grid layout


        #Output pentru run code:

        
        # #Terminal (Zona 5)
        self.terminal = QtWidgets.QPlainTextEdit()
        self.terminal.setReadOnly(False)
        self.terminal.setObjectName("terminal")
        self.terminal.setMinimumHeight(100)

        self.output = QtWidgets.QPlainTextEdit()
        self.output.setReadOnly(True)
        self.output.setObjectName("output")
        self.output.setMinimumHeight(100)

        
        self.input = QtWidgets.QPlainTextEdit()
        self.input.setReadOnly(False)
        self.input.setObjectName("input")
        self.input.setMinimumHeight(100)

        self.tab_widget = QtWidgets.QTabWidget()
        self.tab_widget.setObjectName("tab_widget")
        self.tab_widget.addTab(self.terminal, "Terminal")
        self.tab_widget.addTab(self.input, "Input")
        self.tab_widget.addTab(self.output, "Output")
        self.tab_widget.setTabVisible(2, False)

        self.terminal_splitter = QSplitter(Qt.Vertical) #aici ar trebui sa functioneze splitterul la fel ca in cazul file navigator doar ca pe vertical
        self.terminal_splitter.addWidget(self.splitter) #in orice caz e destul de glitched so idk if im doing it right
        self.terminal_splitter.addWidget(self.tab_widget) #am separat terminal (zona 5) de splitterul anterior (zonele 3+4)
        # self.terminal_splitter.setSizes([1, 4])
        self.terminal_splitter.setSizes([1000, 100])


        self.gridLayout.addWidget(self.terminal_splitter, 2, 0, 1, 2)

        #De aici in jos e shithousery-ul pt functionalitatea terminalului - in mod normal ar trebui mutate undeva separat dar mna
        # QProcess to handle terminal commands
        self.process = QProcess()
        self.process.readyReadStandardOutput.connect(self.display_output)
        self.process.readyReadStandardError.connect(self.display_error)

        # Initialize the terminal prompt
        self.current_directory = QtCore.QDir.currentPath()
        self.update_terminal_prompt()

        # Connect terminal input handling
        self.terminal.installEventFilter(self) #pt functia asta am convertit QtCore.QObject

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def run_code(self):
        """Compile and run the current file."""
        current_index = self.file_tab_bar.currentIndex()
        file_state = self.file_states[current_index]

        # Check if the file is saved - asa ne obliga sa salvam o copie a fisierului inainte de a da run si apoi va functiona
        if not file_state["saved"]:
            self.handle_save_file()  # Save the file before running

        # Get the current file path
        file_path = file_state["file_path"]
        if not file_path:
            self.output.clear()
            self.output.appendPlainText("Error: No file to run.")
            return

        # Compile the file
        file_directory = os.path.dirname(file_path)
        executable_file_name = os.path.basename(file_path).split(".")[0] + ".exe"
        command = ["LLVM/bin/clang++.exe", file_path, "-o", os.path.join(file_directory, executable_file_name)]

        self.tab_widget.setTabVisible(2, True)
        self.tab_widget.setCurrentIndex(2)

        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode != 0:
            self.output.clear()
            self.output.appendPlainText("Compilation Error:\n")
            self.output.appendPlainText(result.stderr)
            return

        # Run the compiled executable
        run_command = os.path.join(file_directory, executable_file_name)
        
        result = subprocess.run(run_command, 
                                input = self.input.toPlainText(),
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True,)

        if result.returncode != 0:
            self.output.clear()
            self.output.appendPlainText("Runtime Error:\n")
            self.output.appendPlainText(result.stderr)
            return

        # Display the output
        self.output.clear()
        self.output.appendPlainText("Execution Output:\n")
        self.output.appendPlainText(result.stdout)
    
    def close_tab(self, index):
        """Handle tab close requests.""" #scoatem din lista si din dictionar datele
        self.file_tab_bar.removeTab(index)
        del self.file_states[index]
        del self.opened_files[index]
        
        # Update the keys in file_states to reflect the new tab indices
        updated_file_states = {}
        for i, key in enumerate(sorted(self.file_states.keys())):
            updated_file_states[i] = self.file_states[key]
        self.file_states = updated_file_states

    #Functiile Handler pt functiile din FileSystem/file_methods.py
    def handle_new_file(self):
        """Handle the New File action."""
        import FileSystem.file_methods as fm

        # Call the new_file function to create a new file
        new_file_name = fm.new_file(self.plainTextEdit.text_edit)

        if new_file_name:
            # Check if the file is already opened
            if new_file_name not in self.opened_files:
                # Add the file to the opened files list
                self.opened_files.append(new_file_name)

                # Add a new tab to the file_tab_bar
                self.file_tab_bar.addTab(new_file_name)

                # Initialize the file state
                self.file_states[len(self.opened_files) - 1] = {
                    "file_path": new_file_name,
                    "saved": False
                }


                # Switch to the new tab
                self.file_tab_bar.setCurrentIndex(len(self.opened_files) - 1)

    def handle_open_file(self):
        """Handle the Open File action."""
        import FileSystem.file_methods as fm

        # Call the open_file function and get the file path
        file_path = fm.open_file(self.plainTextEdit.text_edit)

        if file_path:
            # Check if the file is already opened
            if file_path not in self.opened_files:
                # Add the file to the opened files list
                self.opened_files.append(file_path)

                # Add a new tab to the file_tab_bar
                self.file_tab_bar.addTab(os.path.basename(file_path))

                # Initialize the file state
                self.file_states[len(self.opened_files) - 1] = {
                    "file_path": file_path,
                    "saved": True
                }

                # Switch to the newly opened tab
                self.file_tab_bar.setCurrentIndex(len(self.opened_files) - 1)
            else:
                # If the file is already opened, switch to its tab
                index = self.opened_files.index(file_path)
                self.file_tab_bar.setCurrentIndex(index)

    def handle_save_file(self):
        """Handle the Save File action."""
        import FileSystem.file_methods as fm

        current_index = self.file_tab_bar.currentIndex()
        file_state = self.file_states[current_index]

        # Call the save_file function
        file_path, saved = fm.save_file(
            self.plainTextEdit.text_edit,
            file_state["file_path"],
            file_state["saved"],
            self.plainTextEdit.highlighter
        )

        # Update the file state
        self.file_states[current_index]["file_path"] = file_path
        self.file_states[current_index]["saved"] = saved

    def handle_save_file_as(self):
        """Handle the Save File As action."""
        import FileSystem.file_methods as fm

        current_index = self.file_tab_bar.currentIndex()
        file_state = self.file_states[current_index]

        # Call the save_as_file function
        file_path, saved = fm.save_as_file(
            self.plainTextEdit.text_edit,
            file_state["file_path"]
        )

        # Update the file state
        self.file_states[current_index]["file_path"] = file_path
        self.file_states[current_index]["saved"] = saved

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

    #Fct Terminal
    def update_terminal_prompt(self):
        #print("Update Terminal Prompt")
        """Update the terminal prompt with the current directory."""
        self.terminal.appendPlainText(f"{self.current_directory}> ")

    def execute_command(self, command): #aici e cam shitty pt ca stie doar sa execute anumite comenzi care doar ofera un output (gen dir, git etc)
        #print("Execute Command")       #nu stie sa execute multe lucruri - ar trebui folosita o librarie specializata gen winpty dar mie nu mi a iesit
        #print(f"Executing Command: {command}")  # Debugging line
        """Execute the command entered in the terminal."""
        if command.strip():
            self.terminal.appendPlainText(f"> {command}")  # Display the command
            
             # am tratat in mod special comenzile de clear si cd pt ca sunt printre comenzile uzuale care nu mergeau.
             #asta e doar o solutie temporara pana se prinde cineva cum s ar face legit terminalul
            if command == "clear":
                self.terminal.clear()
                self.update_terminal_prompt()
                return

            # Handle "cd" command
            if command.startswith("cd "):
                new_dir = command[3:].strip()
                if os.path.isdir(new_dir):
                    self.current_directory = os.path.abspath(new_dir)
                    self.update_terminal_prompt()
                else:
                    self.terminal.appendPlainText(f"The system cannot find the path specified: {new_dir}")
                return
            
            self.process.setWorkingDirectory(self.current_directory)

            # Handle shell commands
            if QtCore.QSysInfo.productType() == "windows":
                self.process.start("cmd.exe", ["/c", command])
            else:
                self.process.start("/bin/bash", ["-c", command])


    def display_output(self):
        #print("Display Output")
        """Display the standard output of the command."""
        output = self.process.readAllStandardOutput().data().decode()
        self.terminal.appendPlainText(output)
        self.update_terminal_prompt()

    def display_error(self):
        #print("Display Error")
        """Display the error output of the command."""
        error = self.process.readAllStandardError().data().decode()
        self.terminal.appendPlainText(error)
        self.update_terminal_prompt()
    
    def eventFilter(self, obj, event):
        #print("Event Filter")
        """Handle user input in the terminal."""
        if obj == self.terminal and event.type() == QtCore.QEvent.KeyPress:
            if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:
                cursor = self.terminal.textCursor()
                cursor.movePosition(QTextCursor.StartOfBlock, QTextCursor.KeepAnchor)
                command = cursor.selectedText().strip()
                if command.startswith(f"{self.current_directory}> "):
                    command = command[len(f"{self.current_directory}> "):]
                print(command)  # Debugging line to see the command
                self.execute_command(command)
                return True
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
