from PyQt5.QtWidgets import QTabBar, QPlainTextEdit, QStackedWidget
from PyQt5.QtGui import QTextCursor
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QProcess, QDir, QSysInfo, QEvent, pyqtSignal
from Styles import style
import os
from editor import Editor
from editor import TextEditor  
import uuid
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
    tabClicked = pyqtSignal(int)

    def __init__(self, parent=None, ui = None):
        
        super(File_Tab_Bar, self).__init__(parent)
        
        self.ui = ui
        self.setObjectName("file_tab_bar")
        self.setTabsClosable(False)  # Dezactivez butonul de close nativ
        self.setMovable(True)
        self.setFixedHeight(48)
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)  # Fix the size
        self.setLayoutDirection(Qt.LeftToRight)
        self.setStyleSheet("QTabBar { background: transparent; } QTabBar::tab { background: transparent; }")

        self.default_file_name = "Untitled"
        # self.addTab(self.default_file_name)
        # self.setCurrentIndex(0)

        self.tabCloseRequested.connect(self.close_tab)
        self.currentChanged.connect(self.tab_switch)
        self.tabMoved.connect(self.tab_moved)

        self.opened_files = []  # Aici ar trebui sa fie adaugate dinamic fisierele deschise
        # self.file_states={} #pt a retine care au fost salvate si path-ul lor
        self.editors = {}
        self.tab_labels = {}
        self.saved_content = {}  # <--- cheie: editor

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

    def reconnect_close_buttons(self):
        for i in range(self.count()):
            tab_widget = self.tabButton(i, QTabBar.LeftSide)
            if tab_widget:
                for j in range(tab_widget.layout().count()):
                    item = tab_widget.layout().itemAt(j)
                    widget = item.widget()
                    if isinstance(widget, QtWidgets.QPushButton):
                        try:
                            widget.clicked.disconnect()
                        except Exception:
                            pass
                        widget.clicked.connect(lambda _, idx=i: self.close_tab(idx))

    def add_new_tab(self, name , file_path, saved=False, content = None):
        index = self.count()
        # Creez widget custom pentru tab
        tab_widget = QtWidgets.QWidget()
        tab_layout = QtWidgets.QHBoxLayout(tab_widget)
        tab_layout.setContentsMargins(16, 0, 16, 0)  # padding vertical redus pentru a ridica tabul
        tab_layout.setSpacing(14)
        label = QtWidgets.QLabel(name)
        label.setStyleSheet("color: #aee9d1; font-size: 22px; font-weight: 600; padding: 4px 0;")  # font mai mare, fără text-shadow
        close_btn = QtWidgets.QPushButton("✕")
        close_btn.setFixedSize(32, 32)
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.setStyleSheet("""
            QPushButton {
                background: #263445;
                border: 2px solid #aee9d1;
                color: #aee9d1;
                font-size: 20px;
                border-radius: 16px;
                padding: 0;
            }
            QPushButton:hover {
                background: #e57373;
                color: #fff;
                border: 2px solid #fff;
            }
        """)
        close_btn.clicked.connect(lambda _, i=index: self.close_tab(i))
        tab_layout.addWidget(label)
        tab_layout.addWidget(close_btn)
        tab_layout.addStretch(0)
        tab_widget.setStyleSheet("background: #31395a; border-radius: 16px; border: 3px solid #aee9d1;")
        self.addTab("")
        self.setTabButton(index, QTabBar.LeftSide, tab_widget)
        self.opened_files.append(file_path)
        self.editors[index] = TextEditor(tab_index=index)
        self.editors[index].file_path = file_path
        self.editors[index].tab_index = index
        # Cheie unica: file_path sau uuid pentru taburi noi
        if file_path:
            tab_key = file_path
        else:
            tab_key = f"{name}_{uuid.uuid4()}"
        self.editors[index].tab_key = tab_key
        self.editors[index].textChangedWithIndex.connect(self.mark_tab_unsaved)
        if content is not None:
            self.editors[index].ignore_text_changed = True
            self.editors[index].setPlainText(content)
            self.editors[index].saved = True
            self.editors[index].ignore_text_changed = False
        else:
            self.editors[index].saved = saved
        self.saved_content[tab_key] = content if content is not None else ""
        if file_path and content is not None:
            self.mark_tab_saved(index)
        self.ui.plainTextEdit.switch_text_edit(self.editors[index])  # Switch to the new editor
        self.setCurrentIndex(index)  # Switch to the new tab
        # Salvez referința la label pentru indicator
        self.tab_labels[index] = label
        self.update_tab_saved_indicator(index)
        self.reconnect_close_buttons()

    def update_tab_saved_indicator(self, index):
        # print(f"[DEBUG] update_tab_saved_indicator for tab {index}")
        if not hasattr(self, 'tab_labels') or index not in self.tab_labels:
            return
        try:
            label = self.tab_labels[index]
            if not label:  # Skip if label is None
                return
            name = label.text().lstrip("• ")  # Remove any existing dot
            if not self.editors[index].saved:
                if not name.startswith("• "):
                    label.setText("• " + name)
            else:
                label.setText(name)
        except RuntimeError:
            # If the label was deleted, remove it from our dictionary
            if index in self.tab_labels:
                del self.tab_labels[index]

    def mark_tab_unsaved(self, index):
        if index in self.editors:
            editor = self.editors[index]
            tab_key = editor.tab_key
            current_content = editor.toPlainText()
            print(f"[DEBUG] mark_tab_unsaved: tab_key={tab_key}, current={current_content[:10]}, saved={self.saved_content.get(tab_key, '')[:10]}")
            if current_content != self.saved_content.get(tab_key, ""):
                editor.saved = False
            else:
                editor.saved = True
            self.update_tab_saved_indicator(index)

    def mark_tab_saved(self, index):
        if index in self.editors:
            editor = self.editors[index]
            tab_key = editor.tab_key
            self.saved_content[tab_key] = editor.toPlainText()
            editor.saved = True
            self.update_tab_saved_indicator(index)

    def close_tab(self, index):
        if index in self.editors:
            editor = self.editors[index]
            tab_key = editor.tab_key
            if tab_key in self.saved_content:
                del self.saved_content[tab_key]
            del self.editors[index]
        if index in self.tab_labels:
            del self.tab_labels[index]
        if index < len(self.opened_files):
            del self.opened_files[index]
        self.removeTab(index)
        # Reindex auxiliary mappings (editors, tab_labels, opened_files) so that keys greater than index are shifted down by one.
        new_editors = {}
        new_tab_labels = {}
        for old_idx in sorted(self.editors.keys()):
            if old_idx < index:
                new_editors[old_idx] = self.editors[old_idx]
            elif old_idx > index:
                 new_editors[old_idx - 1] = self.editors[old_idx]
        self.editors = new_editors
        for idx, editor in self.editors.items():
            editor.tab_index = idx
        for old_idx in sorted(self.tab_labels.keys()):
            if old_idx < index:
                 new_tab_labels[old_idx] = self.tab_labels[old_idx]
            elif old_idx > index:
                 new_tab_labels[old_idx - 1] = self.tab_labels[old_idx]
        self.tab_labels = new_tab_labels
        # Reindex opened_files (a list) by shifting elements (if any) after index down by one.
        if index < len(self.opened_files):
             self.opened_files.pop(index)
        print(f"[DEBUG] after close_tab, saved_content keys: {list(self.saved_content.keys())}")
        self.reconnect_close_buttons()

        current_index = self.currentIndex()
        if current_index in self.editors:
             self.ui.plainTextEdit.switch_text_edit(self.editors[current_index])
             # Force re-connect of textChangedWithIndex (for the current editor) so that (even if only one tab remains) the unsaved indicator is updated.
             self.editors[current_index].textChangedWithIndex.disconnect(self.mark_tab_unsaved)
             self.editors[current_index].textChangedWithIndex.connect(self.mark_tab_unsaved)
        elif len(self.editors) > 0:
             first_valid = next(iter(self.editors.values()))
             self.ui.plainTextEdit.switch_text_edit(first_valid)
             first_valid.textChangedWithIndex.disconnect(self.mark_tab_unsaved)
             first_valid.textChangedWithIndex.connect(self.mark_tab_unsaved)
        else:
             self.ui.plainTextEdit.hide_editor()

    def tab_moved(self, from_index, to_index): 
        # Update opened files (only if indices are in bounds)
        if (from_index < len(self.opened_files) and to_index < len(self.opened_files)):
             aux = self.opened_files[from_index]
             self.opened_files[from_index] = self.opened_files[to_index]
             self.opened_files[to_index] = aux

        # Update editors (only if indices are in bounds)
        if (from_index in self.editors and to_index in self.editors):
             aux_editor = self.editors[from_index]
             self.editors[from_index] = self.editors[to_index]
             self.editors[to_index] = aux_editor

        # Update tab labels (only if indices are in bounds)
        if (hasattr(self, 'tab_labels') and from_index in self.tab_labels and to_index in self.tab_labels):
             aux_label = self.tab_labels[from_index]
             self.tab_labels[from_index] = self.tab_labels[to_index]
             self.tab_labels[to_index] = aux_label

        # Update tab_index for all editors
        for idx, editor in self.editors.items():
            editor.tab_index = idx

        self.reconnect_close_buttons()

    def tab_switch(self, index):
        if index not in self.editors.keys():
            return
        self.ui.plainTextEdit.switch_text_edit(self.editors[index])  # Switch to the editor of the selected tab
        self.setCurrentIndex(index)  # Ensure the tab bar reflects the current index
        self.editors[index].tab_index = index

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        index = self.tabAt(event.pos())
        if index != -1:
            self.tabClicked.emit(index)


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
