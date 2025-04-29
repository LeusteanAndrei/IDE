from PyQt5.QtWidgets import QFileSystemModel, QTreeView, QSplitter, QFileDialog, QMessageBox
from PyQt5.QtCore import QDir

#In general am lasat si descrierile pe care mi le-a mai dat copilot la inceputul functiilor in order to better get the idea
#sincer e putin cam messy codul pt ca am incercat sa pun cat mai mult din el in functii ca dupa sa fie mai usor de adaptat
#o sa fie o durere imensa sa refacem designul F
def initialize_sidebar_and_splitter(editor):
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
    tree_view.doubleClicked.connect(lambda index: open_file_from_sidebar(index, file_model, editor))

    editor.setMinimumSize(1000, 1000)  # setat manual pt ca din nush ce motiv editorul se face foarte mic din cauza functiei .addWidget(editor)
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
    if folder_path:
        #print(f"Selected folder: {folder_path}")
        file_model.setRootPath(folder_path) #set root <=> we will see the rest of the files relative to the selected folder
        tree_view.setRootIndex(file_model.index(folder_path))
        tree_view.show() # Show the sidebar when a folder is opened

def open_file_from_sidebar(index, file_model, editor):
    """
    Open a file from the sidebar when double-clicked.
    Args:
        index: The QModelIndex of the clicked item.
        file_model: The QFileSystemModel for the file system.
        editor: The main editor (QPlainTextEdit).
    """
    file_path = file_model.filePath(index)
    file_extension = file_path.split('.')[-1].lower() #obtain the extension (without .)



    # Supported file types
    supported_extensions = ['txt', 'cpp', 'py', 'md', 'h'] #extensions supported - mai adaugati daca va vin idei, in general am putea deschide orice e de tip text

    if file_extension in supported_extensions:
            # Open text-based files in the editor
        try:
            with open(file_path, 'r') as file:
                content = file.read()
            editor.text_edit.setPlainText(content)
            print(f"Opened file: {file_path}")
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to open file: {e}")
    else:
        QMessageBox.warning(None, "Unsupported File", "File type not supported.")