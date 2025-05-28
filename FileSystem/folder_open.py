from PyQt5.QtWidgets import QFileSystemModel, QTreeView, QSplitter, QFileDialog, QMessageBox
from PyQt5.QtCore import QDir
import os

#In general am lasat si descrierile pe care mi le-a mai dat copilot la inceputul functiilor in order to better get the idea
#sincer e putin cam messy codul pt ca am incercat sa pun cat mai mult din el in functii ca dupa sa fie mai usor de adaptat
#o sa fie o durere imensa sa refacem designul F
def initialize_sidebar_and_splitter(editor, main_window):
    """
    Initialize the sidebar (file tree) and splitter layout.
    Args:
        MainWindow: The main application window.
        editor: The main editor (QPlainTextEdit).
    Returns:
        splitter: The QSplitter containing the sidebar and editor.
        tree_view: The QTreeView for the file tree.
        file_model: The QFileSystemModel for the file system.
    
    """
    
    # Initialize the file system model
    file_model = QFileSystemModel()
    file_model.setFilter(QDir.AllDirs | QDir.NoDotAndDotDot | QDir.Files) #filtring in order to only show directories -
                                                                          #it would be dumb to show files even though we specifically want to open a folder lmao                                          
    # Initialize the tree view
    tree_view = QTreeView()
    tree_view.setModel(file_model)
    tree_view.setMinimumWidth(200)  # Set a minimum width for the sidebar
    tree_view.hide()  # Hide it by default - it will be shown when we open a folder

    # Show only the name column - without it we would have also seen some irrelevant bs
    for column in range(1, file_model.columnCount()):
        tree_view.hideColumn(column)

    # Connect the "doubleClick" function in order to be able to open the files from the sidebar
    tree_view.doubleClicked.connect(lambda index: open_file_from_sidebar(index, file_model, main_window))

    # editor.setMinimumSize(1000, 1000)  # setat manual pt ca din nush ce motiv editorul se face foarte mic din cauza functiei .addWidget(editor)
    # Initialize the splitter
    splitter = QSplitter()
    splitter.addWidget(tree_view)  # Add the sidebar
    splitter.addWidget(editor)  # Add the editor

    return splitter, tree_view, file_model

def open_folder(file_model, tree_view):
    """
    Open a folder and update the sidebar with its contents.
    Args:
        file_model: The QFileSystemModel for the file system.
        tree_view: The QTreeView for the file tree.
    """
    folder_path = QFileDialog.getExistingDirectory(None, "Select Folder")
  # Hide the sidebar if no folder is selected
    if folder_path:
        #print(f"Selected folder: {folder_path}")
        file_model.setRootPath(folder_path) #set root <=> we will see the rest of the files relative to the selected folder
        tree_view.setRootIndex(file_model.index(folder_path))
        tree_view.show() # Show the sidebar when a folder is opened
        return
    # tree_view.hide()  # Hide the sidebar if no folder is selected

def open_file_from_sidebar(index, file_model, main_window):
    """
    Open a file from the sidebar when double-clicked and add it to the file bar.
    Args:
        index: The QModelIndex of the clicked item.
        file_model: The QFileSystemModel for the file system.
        main_window: The main window instance (Ui_MainWindow).
    """
    editor = main_window.plainTextEdit.text_edit

    file_path = file_model.filePath(index)
    file_extension = file_path.split('.')[-1].lower()  # Obtain the extension (without .)

    # Supported file types
    supported_extensions = ['txt', 'cpp', 'py', 'md', 'h']  # Add more extensions if needed

    opened_files = main_window.file_tab_bar.opened_files
    # file_states = main_window.file_tab_bar.file_states

    if file_extension in supported_extensions:
        # Acelasi principiu ca in window.py - verificam daca fisierul e deja deschis in navbar
        if file_path not in opened_files:
            try:
                # Open the file and read its content
                with open(file_path, 'r') as file:
                    content = file.read()
               
                # main_window.plainTextEdit.text_edit.setPlainText(content)

                # # Add the file to the file bar
                file_name = os.path.basename(file_path)
                # main_window.file_tab_bar.addTab(file_name)
                # opened_files.append(file_path)

                # # Initialize the file state
                # file_states[len(opened_files) - 1] = {
                #     "file_path": file_path,
                #     "saved": True  # Avand in vedere ca il deschidem dintr-un folder evident e deja salvat
                # }
                main_window.file_tab_bar.add_new_tab(file_name, file_path = file_path, content=content, saved = True)

                # # Switch to the newly opened tab
                # main_window.file_tab_bar.setCurrentIndex(len(opened_files) - 1)
                if not editor.isVisible():
                    editor.parentWidget().show()  # Show the parent/container
                    editor.show()
                print(f"Opened file: {file_path}")
            except Exception as e:
                QMessageBox.critical(None, "Error", f"Failed to open file: {e}")
        else:
            # If the file is already opened, switch to its tab
            index =opened_files.index(file_path)
            # main_window.file_tab_bar.setCurrentIndex(index)
            main_window.file_tab_bar.tab_switch(index)
    else:
        QMessageBox.warning(None, "Unsupported File", "File type not supported.")