from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QProcess
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QSplitter, QDialog, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QPushButton, QSizePolicy, QFileDialog
from FileSystem.folder_open import initialize_sidebar_and_splitter
from FileSystem.file_methods import save_as_file
from Styles import style
import os, subprocess
from PyQt5.QtCore import QTimer
from Code_Runner import Code_Runner, Input, Output

import File_Tab, editor


class Ui_MainWindow(QtCore.QObject):
    # Add these styles at the top of your class
    menu_button_style = """
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

    menu_style = """
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
    """

    number_bar_button_style = '''
    QPushButton#shortcutButton {
        background-color: #344955 !important;
        color: #78A083;
        border: none;
        border-radius: 8px;
        padding: 6px 0px;
        font-size: 16px;
        min-width: 120px;
        min-height: 36px;
        margin: 2px 0px;
    }
    QPushButton#shortcutButton:hover, QPushButton#shortcutButton:checked {
        background-color: #78A083 !important;
        color: #344955;
    }
    '''

    def add_sections(self):
                # Sections (Zona 1)
        self.sectionLayout = QtWidgets.QHBoxLayout()
        self.sectionLayout.setSpacing(24)  # distanțiere mai mare între butoane
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
            button.setStyleSheet(self.menu_button_style)  # Apply style
            button.setCursor(Qt.PointingHandCursor)       # Set cursor
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

        # Apply styles to menus and submenus
        self.fileMenu.setStyleSheet(self.menu_style)
        self.algorithmsMenu.setStyleSheet(self.menu_style)
        self.menuSorting.setStyleSheet(self.menu_style)
        self.menuSearching.setStyleSheet(self.menu_style)
        self.menuDataStructures.setStyleSheet(self.menu_style)
        self.menuGraphAlgorithms.setStyleSheet(self.menu_style)
        self.menuDynamicProgramming.setStyleSheet(self.menu_style)
        self.menuOther.setStyleSheet(self.menu_style)
      
    def connect_buttons(self):
        for button in self.sections:
            if button.objectName() == "File":
                button.setMenu(self.fileMenu)
            elif button.objectName() == "Code":
                button.setMenu(self.algorithmsMenu)

    def setup_buttons(self):
        # Shortcut Buttons (Area 2)
        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.buttonLayout.setSpacing(0)
        self.buttonLayout.setContentsMargins(0, 0, 0, 0)
        self.buttons = []

        def add_group(labels):
            for label in labels:
                b = QtWidgets.QPushButton(label)
                b.setObjectName("FunctionButton")
                b.setStyleSheet(style.BUTTON_STYLE)
                b.setCursor(Qt.PointingHandCursor)
                self.buttonLayout.addWidget(b)
                self.buttons.append(b)
                b.setCheckable(True)

        add_group(["1", "2", "3", "4", "5"])
        self.buttonLayout.addSpacing(120)
        add_group(["6", "7"])
        self.buttonLayout.addSpacing(120)
        add_group(["8", "9", "10", "11", "12", "13"])
        self.buttonLayout.addSpacing(120)
        add_group(["20"])
        self.buttonLayout.addSpacing(60)
        add_group(["14", "15", "16", "17"])
        self.buttonLayout.addSpacing(120)
        add_group(["18", "19"])

        # pune layout-ul în grid
        self.gridLayout.addLayout(self.buttonLayout, 1, 0, 1, 2)

        # și legi semnalele de care ai nevoie
        self.buttons[17].clicked.connect(self.code_runner.abort_run)

    def setupUi(self, MainWindow):
 
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet("background-color: #344955;")
        MainWindow.setStyleSheet("background-color: #344955;")

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


        self.plainTextEdit = editor.Editor()
        self.file_tab_bar = File_Tab.File_Tab_Bar(ui = self)  # Use the custom tab bar class

         #Editor (Zona 4) - legat si de file navigator - Zona 3
        # self.plainTextEdit = editor.Editor() 

        self.editor_layout = QtWidgets.QVBoxLayout()
        self.editor_layout.setContentsMargins(0, 40, 0, 0)  # Adaugă 40px sus pentru a coborî editorul
        self.editor_layout.setSpacing(0)
        self.editor_layout.addWidget(self.file_tab_bar)
        self.editor_layout.addWidget(self.plainTextEdit)


        self.editor_container = QtWidgets.QWidget() #container ca file bar sa fie doar deasupra editorului, nu si deasupra sidebar-ului cand e deschis
        self.editor_container.setLayout(self.editor_layout)
        self.editor_container.plainTextEdit = self.plainTextEdit
        self.editor_container.setStyleSheet("border: none; background: #344955;")

        # Initialize the file system model and tree view
        self.splitter, self.tree_view, self.file_model = initialize_sidebar_and_splitter(self.editor_container, self)
        
        # Create sidebar container with header and icon bar
        self.sidebar_container = QtWidgets.QWidget()
        self.sidebar_layout = QtWidgets.QVBoxLayout(self.sidebar_container)
        self.sidebar_layout.setContentsMargins(0, 0, 0, 0)
        self.sidebar_layout.setSpacing(0)

        # Create header (compact, modern)
        self.sidebar_header = QtWidgets.QWidget()
        self.sidebar_header.setFixedHeight(48)
        self.sidebar_header.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #23272b, stop:1 #263445);
                border-bottom: 2px solid #1e222a;
                padding-top: 8px;
                padding-bottom: 4px;
            }
        """)
        header_layout = QtWidgets.QHBoxLayout(self.sidebar_header)
        header_layout.setContentsMargins(16, 0, 0, 0)
        header_layout.setSpacing(0)
        title_label = QtWidgets.QLabel("EXPLORER")
        title_label.setStyleSheet("""
            QLabel {
                color: #aee9d1;
                font-size: 20px;
                font-weight: bold;
                letter-spacing: 1.5px;
                padding-top: 2px;
                padding-bottom: 2px;
                /* text-shadow: 1px 1px 2px #000; -> nu exista proprietatea text-shadow */
            }
        """)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        # --- Butoane funcționale ---
        self.move_btn = QtWidgets.QPushButton("⇄")
        self.move_btn.setToolTip("Mută Explorer-ul stânga/dreapta")
        self.move_btn.setFixedSize(36, 36)
        self.move_btn.setStyleSheet("""
            QPushButton {
                background: #23272b;
                border: 1.5px solid #78A083;
                color: #78A083;
                font-size: 22px;
                border-radius: 10px;
                /* box-shadow: 0 2px 8px #0004;  -> nu exista culoarea #0004*/
            }
            QPushButton:hover {
                background: #78A083;
                color: #23272b;
                border: 1.5px solid #aee9d1;
            }
        """)
        self.close_btn = QtWidgets.QPushButton("❌")
        self.close_btn.setToolTip("Închide Explorer-ul")
        self.close_btn.setFixedSize(36, 36)
        self.close_btn.setStyleSheet("""
            QPushButton {
                background: #23272b;
                border: 1.5px solid #e57373;
                color: #e57373;
                font-size: 22px;
                border-radius: 10px;
                /* box-shadow: 0 2px 8px #0004; -> nu exista culoarea #0004*/
            }
            QPushButton:hover {
                background: #e57373;
                color: #fff;
                border: 1.5px solid #fff;
            }
        """)
        header_layout.addWidget(self.move_btn)
        header_layout.addWidget(self.close_btn)
        # --- Funcționalitate butoane ---
        def toggle_sidebar():
            if self.sidebar_container.isVisible():
                self.sidebar_container.hide()
            else:
                self.sidebar_container.show()
        self.close_btn.clicked.connect(lambda: self.sidebar_container.hide())
        # Shortcut Ctrl+B pentru a arăta/ascunde Explorer-ul
        QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+B"), MainWindow, toggle_sidebar)
        # Mutare Explorer stânga/dreapta
        def move_sidebar():
            idx = self.splitter.indexOf(self.sidebar_container)
            count = self.splitter.count()
            if idx == 0 and count > 1:
                self.splitter.insertWidget(1, self.sidebar_container)
            else:
                self.splitter.insertWidget(0, self.sidebar_container)
        self.move_btn.clicked.connect(move_sidebar)

        # Create icon bar (modern, compact)
        self.sidebar_icon_bar = QtWidgets.QWidget()
        self.sidebar_icon_bar.setFixedHeight(44)
        self.sidebar_icon_bar.setStyleSheet("""
            QWidget {
                background: #23272b;
                border-bottom: 2px solid #1e222a;
                padding: 6px 0 6px 0;
            }
            QPushButton {
                background: #23272b;
                /* border: 1.2px solid #444a; -> nu exista culoarea #444a */
                min-width: 38px;
                min-height: 38px;
                max-width: 38px;
                max-height: 38px;
                margin: 0 8px;
                border-radius: 8px;
                color: #b0b0b0;
                font-size: 20px;
            }
            QPushButton:hover {
                background: #78A083;
                color: #23272b;
                border: 1.2px solid #aee9d1;
            }
        """)
        icon_layout = QtWidgets.QHBoxLayout(self.sidebar_icon_bar)
        icon_layout.setContentsMargins(8, 0, 0, 0)
        icon_layout.setSpacing(0)
        refresh_btn = QtWidgets.QPushButton("⟳")
        refresh_btn.setToolTip("Refresh")
        new_file_btn = QtWidgets.QPushButton("＋")
        new_file_btn.setToolTip("New File")
        new_folder_btn = QtWidgets.QPushButton("🗀")
        new_folder_btn.setToolTip("New Folder")
        icon_layout.addWidget(refresh_btn)
        icon_layout.addWidget(new_file_btn)
        icon_layout.addWidget(new_folder_btn)
        icon_layout.addStretch()

        # Conectez butoanele la funcții
        refresh_btn.clicked.connect(self.refresh_file_explorer)
        new_file_btn.clicked.connect(self.create_new_file_in_root)
        new_folder_btn.clicked.connect(self.create_new_folder_in_root)

        # Add header and icon bar to sidebar layout
        self.sidebar_layout.addWidget(self.sidebar_header)
        self.sidebar_layout.addWidget(self.sidebar_icon_bar)

        # Creez un container pentru QTreeView și spacer
        self.tree_area = QtWidgets.QWidget()
        self.tree_area_layout = QtWidgets.QVBoxLayout(self.tree_area)
        self.tree_area_layout.setContentsMargins(0, 0, 0, 0)
        self.tree_area_layout.setSpacing(0)
        self.tree_area.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)

        self.tree_view.setParent(None)
        self.tree_view.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        self.sidebar_spacer = QtWidgets.QWidget()
        self.sidebar_spacer.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)

        self.tree_area_layout.addWidget(self.tree_view)
        self.tree_area_layout.addWidget(self.sidebar_spacer)
        self.sidebar_layout.addWidget(self.tree_area)
        self.sidebar_layout.setStretch(0, 0)  # header
        self.sidebar_layout.setStretch(1, 0)  # icon bar
        self.sidebar_layout.setStretch(2, 1)  # tree_area (ocupă tot spațiul)

        # La început, ascund spacer-ul
        self.sidebar_spacer.hide()

        # Funcții pentru a arăta/ascunde QTreeView sau spacer
        def show_tree_view():
            self.tree_view.show()
            self.sidebar_spacer.hide()
        def hide_tree_view():
            self.tree_view.hide()
            self.sidebar_spacer.show()
        self.show_tree_view = show_tree_view
        self.hide_tree_view = hide_tree_view

        # Remove margin from sidebar_container
        self.sidebar_container.setStyleSheet("background: #23272b; border: 2px solid #1e222a; border-radius: 12px;")

        # Remove the first widget (tree_view) from splitter and add sidebar_container
        self.splitter.insertWidget(0, self.sidebar_container)
        self.splitter.setStyleSheet("QSplitter::handle { background: transparent; } border: none; background: #344955;")
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
        self.tab_widget.setStyleSheet("""
                            QTabWidget {
                                border: none;
                                outline: none;
                                background-color: #344955;
                            }
                            QTabWidget::pane {
                                border: none;
                                outline: none;
                                background-color: #344955;
                                margin: 0px;
                                padding: 0px;
                            }
                            QTabWidget::tab-bar {
                                border: none;
                                outline: none;
                                background-color: #344955;
                            }
                            QTabBar {
                                border: none;
                                outline: none;
                                background-color: #344955;
                            }
                            QTabBar::tab {
                                background-color: #344955;
                                color: #78A083;
                                border: none;
                                outline: none;
                                padding: 8px 16px;
                                margin: 0px;
                            }
                            QTabBar::tab:selected {
                                background-color: #78A083;
                                color: #344955;
                                border: none;
                                outline: none;
                            }
                            """)

        self.terminal_splitter = QSplitter(Qt.Vertical)
        self.terminal_splitter.addWidget(self.splitter)
        self.terminal_splitter.addWidget(self.tab_widget)
        self.terminal_splitter.setSizes([1000, 100])
        self.terminal_splitter.setStyleSheet("QSplitter::handle { background: transparent; } border: none; background: #344955;")

        self.gridLayout.addWidget(self.terminal_splitter, 2, 0, 1, 2)

        # Creez un label pentru root folder
        self.root_folder_label = QtWidgets.QLabel()
        self.root_folder_label.setStyleSheet(
            "color: #78A083; font-size: 26px; font-weight: bold; padding: 12px 0 12px 16px;"
        )
        self.root_folder_label.setText("")
        self.sidebar_layout.insertWidget(2, self.root_folder_label)  # Adaugă deasupra tree_area

        # În setupUi, după crearea self.tree_view și self.root_folder_label:
        self.tree_view.setStyleSheet("""
            QTreeView {
                background: #23272b;
                color: #e0e0e0;
                border: 2px solid #1e222a;
                font-size: 16px;
                padding: 8px 0 8px 10px;
                font-family: 'Roboto Mono', 'Roboto', monospace;
                border-radius: 8px;
            }
            QTreeView::item:selected {
                background: #2d323b;
                color: #aee9d1;
            }
            QTreeView::item:hover {
                background: #31363f;
            }
        """)

        self.file_tab_bar.tabClicked.connect(self.on_tab_clicked)

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    
    #Functiile Handler pt functiile din FileSystem/file_methods.py
    def handle_new_file(self):
        from PyQt5.QtWidgets import QFileDialog, QMessageBox
        import os
        # Deschide dialogul Save As
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self.centralwidget,
            "Create New File",
            "",
            "All Files (*);;Text Files (*.txt);;C++ Files (*.cpp)",
            options=options
        )
        if file_path:
            # Extrage numele fișierului fără extensie
            base_name = os.path.basename(file_path)
            name_no_ext, ext = os.path.splitext(base_name)
            parent_dir = os.path.dirname(file_path)
            folder_path = os.path.join(parent_dir, name_no_ext.capitalize())  # Prima literă mare
            # Creează folderul dacă nu există
            try:
                os.makedirs(folder_path, exist_ok=True)
            except Exception as e:
                QMessageBox.critical(self.centralwidget, "Error", f"Could not create folder: {e}")
                return
            # Creează fișierul în folderul nou
            new_file_path = os.path.join(folder_path, base_name)
            if os.path.exists(new_file_path):
                QMessageBox.warning(self.centralwidget, "File Exists", "A file with that name already exists in the folder.")
                return
            try:
                with open(new_file_path, 'w') as f:
                    f.write("")
            except Exception as e:
                QMessageBox.critical(self.centralwidget, "Error", f"Could not create file: {e}")
                return
            # Deschide fișierul nou în editor
            self.handle_open_file_path(new_file_path)
            # Dacă folderul e nou, actualizează Explorer-ul
            self.file_model.setRootPath(folder_path)
            self.tree_view.setRootIndex(self.file_model.index(folder_path))
            self.tree_view.show()
            self.update_root_folder_label()

    def handle_open_file_path(self, file_path):
        # Deschide fișierul dat direct (fără dialog)
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
            if file_path not in self.file_tab_bar.opened_files:
                self.file_tab_bar.add_new_tab(name=os.path.basename(file_path), file_path=file_path, content=content, saved=True)
            else:
                index = self.file_tab_bar.opened_files.index(file_path)
                self.file_tab_bar.tab_switch(index)
            # Evidențiază fișierul în Explorer
            file_index = self.file_model.index(file_path)
            self.tree_view.setCurrentIndex(file_index)
            self.tree_view.scrollTo(file_index)
            self.update_root_folder_label()

    def handle_save_file(self):
        """Handle the Save File action."""
        import FileSystem.file_methods as fm

        current_index = self.file_tab_bar.currentIndex()
        # file_state = self.file_tab_bar.file_states[current_index]


        # Call the save_file function
        file_path, saved = fm.save_file(
            self.plainTextEdit.text_edit,
            self.plainTextEdit.text_edit.file_path,
            self.plainTextEdit.text_edit.saved,
            self.plainTextEdit.highlighter
        )

        # Update the file state
        # self.file_tab_bar.file_states[current_index]["file_path"] = file_path
        # self.file_tab_bar.file_states[current_index]["saved"] = saved
        self.plainTextEdit.text_edit.file_path = file_path
        self.plainTextEdit.text_edit.saved = saved
        self.file_tab_bar.mark_tab_saved(current_index)

    def handle_save_file_as(self):
        """Handle the Save File As action."""
        import FileSystem.file_methods as fm

        current_index = self.file_tab_bar.currentIndex()
        # file_state = self.file_tab_bar.file_states[current_index]

        # Call the save_as_file function
        file_path, saved = fm.save_as_file(
            self.plainTextEdit.text_edit,
            self.plainTextEdit.text_edit.file_path
        )

        if file_path is None:
            return
        # Update the file state
        # self.file_tab_bar.file_states[current_index]["file_path"] = file_path
        # self.file_tab_bar.file_states[current_index]["saved"] = saved
        self.plainTextEdit.text_edit.file_path = file_path
        self.plainTextEdit.text_edit.saved = saved
        self.file_tab_bar.mark_tab_saved(current_index)

        # Update the tab name
        self.file_tab_bar.setTabText(current_index, os.path.basename(file_path))
        self.file_tab_bar.mark_tab_saved(current_index)

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

    def changeEditor(self, new_editor):
        self.plainTextEdit.hide_editor()
        self.plainTextEdit = new_editor
        self.plainTextEdit.show_editor()

    def refresh_file_explorer(self):
        # Reîncarcă folderul curent în QTreeView
        root_path = self.file_model.rootPath()
        self.file_model.setRootPath("")  # Reset temporar
        self.file_model.setRootPath(root_path)
        self.tree_view.setRootIndex(self.file_model.index(root_path))
        self.update_root_folder_label()

    def create_new_file_in_root(self):
        from PyQt5.QtWidgets import QMessageBox
        import os
        root_path = self.file_model.rootPath()
        if not root_path:
            QMessageBox.warning(self.centralwidget, "No Folder", "No folder is currently open.")
            return
        dlg = CustomInputDialog("New File", "Enter file name:", self.centralwidget)
        if dlg.exec_() == QDialog.Accepted:
            file_name = dlg.getText()
            if file_name:
                file_path = os.path.join(root_path, file_name)
                if os.path.exists(file_path):
                    QMessageBox.warning(self.centralwidget, "File Exists", "A file with that name already exists.")
                    return
                try:
                    with open(file_path, 'w') as f:
                        f.write("")
                    self.refresh_file_explorer()
                except Exception as e:
                    QMessageBox.critical(self.centralwidget, "Error", f"Could not create file: {e}")

    def create_new_folder_in_root(self):
        from PyQt5.QtWidgets import QMessageBox
        import os
        root_path = self.file_model.rootPath()
        if not root_path:
            QMessageBox.warning(self.centralwidget, "No Folder", "No folder is currently open.")
            return
        dlg = CustomInputDialog("New Folder", "Enter folder name:", self.centralwidget)
        if dlg.exec_() == QDialog.Accepted:
            folder_name = dlg.getText()
            if folder_name:
                folder_path = os.path.join(root_path, folder_name)
                if os.path.exists(folder_path):
                    QMessageBox.warning(self.centralwidget, "Folder Exists", "A folder with that name already exists.")
                    return
                try:
                    os.makedirs(folder_path)
                    self.refresh_file_explorer()
                except Exception as e:
                    QMessageBox.critical(self.centralwidget, "Error", f"Could not create folder: {e}")

    def handle_open_file(self):
        import FileSystem.file_methods as fm
        file_path, content = fm.open_file(self)
        if file_path:
            self.handle_open_file_path(file_path)

    def update_root_folder_label(self):
        import os
        root_path = self.file_model.rootPath()
        if root_path:
            folder_name = os.path.basename(os.path.normpath(root_path))
            self.root_folder_label.setText(folder_name)
        else:
            self.root_folder_label.setText("")

    def show_find_dialog(self):
        from dialogs import FindDialog
        dialog = FindDialog(self.centralwidget)
        dialog.findNext.connect(self.find_text)
        dialog.exec_()
        
    def show_replace_dialog(self):
        from dialogs import ReplaceDialog
        dialog = ReplaceDialog(self.centralwidget)
        dialog.findNext.connect(self.find_text)
        dialog.replace.connect(self.replace_text)
        dialog.replaceAll.connect(self.replace_all_text)
        dialog.exec_()
        
    def find_text(self, text, whole_words, case_sensitive):
        editor = self.plainTextEdit.text_edit
        cursor = editor.textCursor()
        
        # Start searching from the current position
        doc = editor.document()
        find_flags = QtGui.QTextDocument.FindFlags()
        
        if case_sensitive:
            find_flags |= QtGui.QTextDocument.FindCaseSensitively
        if whole_words:
            find_flags |= QtGui.QTextDocument.FindWholeWords
            
        # If we're at the end of a selection, start from cursor position
        if cursor.hasSelection() and cursor.selectionEnd() == cursor.position():
            cursor.clearSelection()
            editor.setTextCursor(cursor)
            
        # Find the next occurrence
        found_cursor = doc.find(text, cursor, find_flags)
        
        if not found_cursor.isNull():
            editor.setTextCursor(found_cursor)
        else:
            # If not found from cursor, try from start
            cursor.movePosition(QtGui.QTextCursor.Start)
            found_cursor = doc.find(text, cursor, find_flags)
            if not found_cursor.isNull():
                editor.setTextCursor(found_cursor)
                
    def replace_text(self, replace_with):
        editor = self.plainTextEdit.text_edit
        cursor = editor.textCursor()
        if cursor.hasSelection():
            cursor.insertText(replace_with)
            editor.setTextCursor(cursor)
            
    def replace_all_text(self, find_text, replace_with, whole_words, case_sensitive):
        editor = self.plainTextEdit.text_edit
        cursor = editor.textCursor()
        
        # Start from the beginning
        cursor.movePosition(QtGui.QTextCursor.Start)
        editor.setTextCursor(cursor)
        
        # Set find flags
        find_flags = QtGui.QTextDocument.FindFlags()
        if case_sensitive:
            find_flags |= QtGui.QTextDocument.FindCaseSensitively
        if whole_words:
            find_flags |= QtGui.QTextDocument.FindWholeWords
            
        # Start a single undo operation
        cursor.beginEditBlock()
        
        while True:
            found_cursor = editor.document().find(find_text, cursor, find_flags)
            if found_cursor.isNull():
                break
            
            found_cursor.insertText(replace_with)
            cursor = found_cursor
            
        cursor.endEditBlock()
        
    def on_tab_clicked(self, index):
        print(f"[DEBUG] Tab {index} clicked!")
        # Sterg orice workaround care forta saved=True sau update_tab_saved_indicator aici
        # Las doar logica de comparatie de continut sa decida dot-ul

class CustomInputDialog(QDialog):
    def __init__(self, title, label_text, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setFixedSize(520, 270)
        self.setStyleSheet("""
            QDialog {
                background-color: #23272b;
                border-radius: 16px;
                min-height: 220px;
            }
            QLabel#DialogTitle {
                color: #78A083;
                font-size: 22px;
                font-weight: bold;
                margin-bottom: 18px;
                qproperty-alignment: AlignCenter;
            }
            QLabel {
                color: #78A083;
                font-size: 18px;
                font-weight: bold;
                margin-bottom: 10px;
                background: transparent;
                border: none;
                border-radius: 12px;
            }
            QLineEdit#DialogInput {
                background: #181b1f;
                color: #e0e0e0;
                border: 2px solid #78A083;
                border-radius: 12px;
                font-size: 20px;
                padding: 10px 18px;
                margin-bottom: 28px;
            }
            QPushButton {
                background-color: #344955;
                color: #78A083;
                border: none;
                border-radius: 10px;
                font-size: 20px;
                padding: 12px 36px;
                margin: 0 16px;
            }
            QPushButton:hover {
                background-color: #78A083;
                color: #344955;
            }
        """)
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(32, 18, 32, 18)
        title = QLabel(title)
        title.setObjectName("DialogTitle")
        layout.addWidget(title)
        label = QLabel(label_text)
        layout.addWidget(label)
        input_container = QtWidgets.QWidget()
        input_container.setFixedWidth(480)
        input_hbox = QHBoxLayout(input_container)
        input_hbox.setContentsMargins(0, 16, 0, 16)
        input_hbox.setSpacing(0)
        self.input = QLineEdit()
        self.input.setObjectName("DialogInput")
        self.input.setPlaceholderText("Type name here...")
        self.input.setFixedHeight(75)
        self.input.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.input.setFixedWidth(460)
        input_hbox.addWidget(self.input, 1)
        layout.addWidget(input_container)
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(20)
        self.ok_btn = QPushButton("OK")
        self.cancel_btn = QPushButton("Cancel")
        btn_layout.addStretch()
        btn_layout.addWidget(self.ok_btn)
        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        self.ok_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)
   
    def getText(self):
        return self.input.text()

class fileHandler():
    def __init__ (self, ui):
        self.ui = ui

    def handle_new_file(self):
            # get_file_path()
            # create_text_edit()
            # create_tab()
            # link_tab_to_text_edit()
            # switch_text_edit()
        import FileSystem.file_methods as fm
        new_file_name = fm.new_file(self.ui.plainTextEdit.text_edit)
        if new_file_name:
            self.ui.file_tab_bar.add_new_tab(new_file_name, new_file_name)

        # Ascund header-ul QTreeView (Name)
        self.ui.tree_view.header().hide()
        self.ui.tree_view.header().setVisible(False)
        self.ui.tree_view.setHeaderHidden(True)
        # Măresc fontul pentru item-urile din QTreeView
        self.ui.tree_view.setStyleSheet("QTreeView { background: #23272b; color: #e0e0e0; border: none; font-size: 17px; } QTreeView::item:selected { background: #31363b; color: #78A083; }")