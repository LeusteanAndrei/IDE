from PyQt5.QtWidgets import QFileDialog, QInputDialog, QMessageBox
from editor import TextEditor


#Nu mai folosim variabilele globale de current_path si saved pt ca erau folosite cum trebuie doar prima data
#in schimb acum fiecare file va avea un path si saved state propriu - le retinem intr-un dictionar in window.py
#probabil asa va trebui sa procedam si cu editorul - fiecare file are propriul editor

#in functii acum vom return path si saved state pt a le adauga in dictionar si manevra in functiile handler din window.py
def save_as_file(editor, file_path):
    """Save the current of the editor into a new file"""
    options = QFileDialog.Options()
    new_file_path, _ = QFileDialog.getSaveFileName(
                    None, "Save File", file_path,  "All Files (*);;Text Files (*.txt);;C++ Files (*.cpp)", 
                    options=options)
    if new_file_path:
        # with open(new_file_path, 'w') as file:
        #     file.write(editor.toPlainText())
        # print(f"File saved as: {file_path}")
        return new_file_path, True #return the new file path and set saved to True
    return None, False
    # return file_path, False #if the user cancels the save dialog, return the original file path and set saved to False

def save_file(editor, file_path, saved, highlighter):
    """Save current content of the editor into the existing file"""
    if file_path and saved:
        with open(file_path, 'w') as file:
            file.write(editor.toPlainText())
        print(f"File saved: {file_path}")
    else:
        file_path, saved = save_as_file(editor, file_path) # If no file path is set for now -> we must us save as method
    highlighter.rehighlight() # Reapply syntax highlighting after saving
    return file_path, saved

def new_file(editor): #default face terminatia .txt pana cand salvam noi altfel
    """Create a new file in the editor"""
    while True:
        #prompt the user to provide a file name
        file_name, ok = QInputDialog.getText(None, "New File", "Enter file name:")
        if not ok: #user pressed cancel button
            return None #return None to indicate no file was created
        if file_name.strip():
            current_file_path = file_name.strip()
            # editor.clear() # Clear the editor content
            break
        else:
            # Show an error message to the user
            QMessageBox.warning(None, "Invalid File Name", "Please enter a valid file name.")
    print("New file created")
    return current_file_path

def open_file(ui):
    """Open an existing file in the editor"""

    options = QFileDialog.Options()
    file_path, _ = QFileDialog.getOpenFileName(
        None, "Open File", "", "All Files (*);;Text Files (*.txt);;C++ Files (*.cpp)", options=options
    )

    # print(f"Selected file: {file_path}")
    if file_path:
        with open(file_path, 'r') as file:
            content=file.read()
        # new_text_edit = TextEditor()
        # new_text_edit.setPlainText(content)
        
        # ui.plainTextEdit.switch_text_edit(new_text_edit)
        print(f"File opened: {file_path}")
        # if not editor.isVisible():
        #     editor.parentWidget().show()  # Show the parent/container
        #     editor.show()
        return file_path, content
    
    return None, None  # If no file was opened, return None



# def open_file(editor):
#     """Open an existing file in the editor"""

#     options = QFileDialog.Options()
#     file_path, _ = QFileDialog.getOpenFileName(
#         None, "Open File", "", "All Files (*);;Text Files (*.txt);;C++ Files (*.cpp)", options=options
#     )

#     # print(f"Selected file: {file_path}")
#     if file_path:
#         with open(file_path, 'r') as file:
#             content=file.read()
#         editor.setPlainText(content)
#         print(f"File opened: {file_path}")
#         if not editor.isVisible():
#             editor.parentWidget().show()  # Show the parent/container
#             editor.show()
#         return file_path

