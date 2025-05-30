from PyQt5.QtWidgets import QTabBar, QPlainTextEdit, QStackedWidget
from PyQt5.QtGui import QTextCursor
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QProcess, QDir, QSysInfo, QEvent
from Styles import style
import os
from editor import Editor
from editor import TextEditor  
# class File_Tab_Bar(QTabBar):

#     def __init__(self, parent=None, ui = None):
        
#         super(File_Tab_Bar, self).__init__(parent)
        
#         self.ui = ui
#         self.setObjectName("file_tab_bar")
#         self.setTabsClosable(True)
#         self.setMovable(True)
#         self.setFixedHeight(25)
#         self.setStyleSheet(style.FILE_TAB_STYLE)
#         self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)  # Fix the size
#         self.setLayoutDirection(Qt.LeftToRight) 

#         self.default_file_name = "Untitled"
#         self.addTab(self.default_file_name)
#         self.setCurrentIndex(0)

#         self.tabCloseRequested.connect(self.close_tab)
#         self.currentChanged.connect(self.tab_switch)
#         self.tabMoved.connect(self.tab_moved)

#         self.opened_files = []  # Aici ar trebui sa fie adaugate dinamic fisierele deschise
#         self.file_states={} #pt a retine care au fost salvate si path-ul lor

#          # Cand deschidem editorul, adaugam un tab default numit Untitled
#          # ca sa fie rulat codul din el intai ne va obliga sa il salvam
#         self.opened_files.append(self.default_file_name)
#         self.file_states[0] = {
#             "file_path": None,  # No file path yet
#             "saved": False      # File is not saved
#         }


#     def close_tab(self, index):

#         """Handle tab close requests.""" #scoatem din lista si din dictionar datele
#         current_index = self.currentIndex()
#         self.removeTab(index)
#         del self.file_states[index]
#         del self.opened_files[index]
        
#         # Update the keys in file_states to reflect the new tab indices
#         updated_file_states = {}
#         for i, key in enumerate(sorted(self.file_states.keys())):
#             updated_file_states[i] = self.file_states[key]
#         self.file_states = updated_file_states
#         # previous_path = self.file_states.get(index, {}).get("file_path")

#         if index == current_index:
#             current_index = self.currentIndex()
#             if current_index == -1:  # No more tabs open
#                 self.ui.plainTextEdit.hide()
#                 self.ui.plainTextEdit.text_edit.hide()

#             try:
#                 if self.file_states[current_index]["file_path"] is not None:
#                     with open(self.file_states[current_index]["file_path"], 'r') as file:
#                         content = file.read()
#                     self.ui.plainTextEdit.text_edit.setPlainText(content)
#             except Exception as e:
#                 pass
            
#     def tab_moved(self, from_index, to_index): 

#         aux = self.file_states[from_index]
#         self.file_states[from_index] = self.file_states[to_index]
#         self.file_states[to_index] = aux

#         aux = self.opened_files[from_index]
#         self.opened_files[from_index] = self.opened_files[to_index]
#         self.opened_files[to_index] = aux

#     def tab_switch(self, index):
#         file_state = self.file_states.get(index)
#         if file_state and file_state["file_path"] is not None:
#             with open(file_state["file_path"], 'r') as file:
#                 content = file.read()
#             self.ui.plainTextEdit.text_edit.setPlainText(content)


class File_Tab_Bar(QTabBar):

    def __init__(self, parent=None, ui = None):
        
        super(File_Tab_Bar, self).__init__(parent)
        
        self.ui = ui
        self.setObjectName("file_tab_bar")
        self.setTabsClosable(True)
        self.setMovable(True)
        self.setFixedHeight(48)
        self.setStyleSheet(style.FILE_TAB_STYLE)
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)  # Fix the size
        self.setLayoutDirection(Qt.LeftToRight) 

        self.default_file_name = "Untitled"
        # self.addTab(self.default_file_name)
        # self.setCurrentIndex(0)

        self.tabCloseRequested.connect(self.close_tab)
        self.currentChanged.connect(self.tab_switch)
        self.tabMoved.connect(self.tab_moved)

        self.opened_files = []  # Aici ar trebui sa fie adaugate dinamic fisierele deschise
        # self.file_states={} #pt a retine care au fost salvate si path-ul lor
        self.editors = {}

        #  # Cand deschidem editorul, adaugam un tab default numit Untitled
        #  # ca sa fie rulat codul din el intai ne va obliga sa il salvam
        # self.opened_files.append(self.default_file_name)
        # self.file_states[0] = {
        #     "file_path": None,  # No file path yet
        #     "saved": False      # File is not saved
        # }
        # self.editors[0] = Editor()  # Associate the default editor with the first tab
        # self.ui.plainTextEdit = self.editors[0]  # Set the default editor in the UI

        self.add_new_tab(self.default_file_name, None)  # Initialize with a default tab

    def add_new_tab(self, name , file_path, saved=False, content = None):
        index = self.count()
        self.addTab(name)
        self.opened_files.append(file_path)
        # self.file_states[index] = {
        #     "file_path": file_path,  # Path of the file
        #     "saved": saved           # File is not saved
        # }

        self.editors[index] = TextEditor()
        self.editors[index].file_path = file_path
        self.editors[index].saved = saved
        if content is not None:
            self.editors[index].setPlainText(content)
        self.ui.plainTextEdit.switch_text_edit(self.editors[index])  # Switch to the new editor
        self.setCurrentIndex(index)  # Switch to the new tab

        if not self.isVisible():
            self.show()


    def close_tab(self, index):
        current_index = self.currentIndex()
        # del self.file_states[index]
        del self.opened_files[index]
        del self.editors[index]
        # self.editors.pop(index)
        self.removeTab(index)


        # updated_file_states = {}
        # for i, key in enumerate(sorted(self.file_states.keys())):
        #     updated_file_states[i] = self.file_states[key]
        # self.file_states = updated_file_states

        updated_editors = {}
        
        for i, editor in enumerate(sorted(self.editors.keys())):
            updated_editors[i] = self.editors[editor]
        self.editors = updated_editors

        if index == current_index:
            current_index = self.currentIndex()
            if current_index == -1:  # No more tabs open
                self.hide()
                self.ui.plainTextEdit.hide_editor()
            else:
                self.ui.plainTextEdit.switch_text_edit(self.editors[current_index])  # Switch to the current editor  
   
        self.refresh()

    def tab_moved(self, from_index, to_index): 

        # aux = self.file_states[from_index]
        # self.file_states[from_index] = self.file_states[to_index]
        # self.file_states[to_index] = aux

        aux = self.opened_files[from_index]
        self.opened_files[from_index] = self.opened_files[to_index]
        self.opened_files[to_index] = aux

        aux_editor = self.editors[from_index]
        self.editors[from_index] = self.editors[to_index]
        self.editors[to_index] = aux_editor

    def tab_switch(self, index):
        if index not in self.editors.keys():
            return
        self.ui.plainTextEdit.switch_text_edit(self.editors[index])  # Switch to the editor of the selected tab
        self.setCurrentIndex(index)  # Ensure the tab bar reflects the current index

    def refresh(self):
        self.update()


class Terminal(QPlainTextEdit):
    def __init__(self, parent=None, ui = None):
        super(Terminal, self).__init__(parent)
        self.ui = ui
        self.setReadOnly(False)
        self.setObjectName("terminal")
        self.setMinimumHeight(100)      

        self.process = QProcess()
        self.process.readyReadStandardOutput.connect(self.display_output)
        self.process.readyReadStandardError.connect(self.display_error)
        self.current_directory = QDir.currentPath()
        self.update_terminal_prompt()

    def update_terminal_prompt(self):
        #print("Update Terminal Prompt")
        """Update the terminal prompt with the current directory."""
        self.appendPlainText(f"{self.current_directory}> ")

    def execute_command(self, command): #aici e cam shitty pt ca stie doar sa execute anumite comenzi care doar ofera un output (gen dir, git etc)
        #print("Execute Command")       #nu stie sa execute multe lucruri - ar trebui folosita o librarie specializata gen winpty dar mie nu mi a iesit
        #print(f"Executing Command: {command}")  # Debugging line
        """Execute the command entered in the terminal."""
        if command.strip():
            self.appendPlainText(f"> {command}")  # Display the command
            
             # am tratat in mod special comenzile de clear si cd pt ca sunt printre comenzile uzuale care nu mergeau.
             #asta e doar o solutie temporara pana se prinde cineva cum s ar face legit terminalul
            if command == "clear":
                self.clear()
                self.update_terminal_prompt()
                return

            # Handle "cd" command
            if command.startswith("cd "):
                new_dir = command[3:].strip()
                if os.path.isdir(new_dir):
                    self.current_directory = os.path.abspath(new_dir)
                    self.update_terminal_prompt()
                else:
                    self.appendPlainText(f"The system cannot find the path specified: {new_dir}")
                return
            
            self.process.setWorkingDirectory(self.current_directory)

            # Handle shell commands
            if QSysInfo.productType() == "windows":
                self.process.start("cmd.exe", ["/c", command])
            else:
                self.process.start("/bin/bash", ["-c", command])

    def display_output(self):
        #print("Display Output")
        """Display the standard output of the command."""
        output = self.process.readAllStandardOutput().data().decode()
        self.appendPlainText(output)
        self.update_terminal_prompt()

    def display_error(self):
        #print("Display Error")
        """Display the error output of the command."""
        error = self.process.readAllStandardError().data().decode()
        self.appendPlainText(error)
        self.update_terminal_prompt()
    
    def handle_event(self, event):
        if event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
                cursor = self.textCursor()
                cursor.movePosition(QTextCursor.StartOfBlock, QTextCursor.KeepAnchor)
                command = cursor.selectedText().strip()
                if command.startswith(f"{self.current_directory}> "):
                    command = command[len(f"{self.current_directory}> "):]
                print(command)  # Debugging line to see the command
                self.execute_command(command)
                return True    
