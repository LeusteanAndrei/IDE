from PyQt5.QtWidgets import QFileDialog, QInputDialog, QMessageBox

current_file_path = None #with this one we verify what the current file path is)


def save_as_file(editor):
    """Save the current of the editor into a new file"""
    global current_file_path
    options = QFileDialog.Options()
    file_path, _ = QFileDialog.getSaveFileName(
                    None, "Save File", "",  "All Files (*);;Text Files (*.txt);;C++ Files (*.cpp)", 
                    options=options)
    if file_path:
        with open(file_path, 'w') as file:
            file.write(editor.toPlainText())
        current_file_path = file_path # Update the current file path
        print(f"File saved as: {file_path}")

def save_file(editor, highlighter):
    """Save current content of the editor into the existing file"""
    global current_file_path
    if current_file_path:
        with open(current_file_path, 'w') as file:
            file.write(editor.toPlainText())
        print(f"File saved: {current_file_path}")
    else:
        save_as_file(editor) # If no file path is set for now -> we must us save as method
    highlighter.rehighlight() # Reapply syntax highlighting after saving

def new_file(editor):
    """Create a new file in the editor"""
    global current_file_path
    while True:
        #prompt the user to provide a file name
        file_name, ok = QInputDialog.getText(None, "New File", "Enter file name:")
        if not ok: #user pressed cancel button
            break
        if file_name.strip():
            current_file_path = file_name.strip()
            editor.clear() # Clear the editor content
            break
        else:
            # Show an error message to the user
            QMessageBox.warning(None, "Invalid File Name", "Please enter a valid file name.")
    print("New file created")

def open_file(editor):
    """Open an existing file in the editor"""
    global current_file_path
    options = QFileDialog.Options()
    file_path, _ = QFileDialog.getOpenFileName(
        None, "Open File", "", "All Files (*);;Text Files (*.txt);;C++ Files (*.cpp)", options=options
    )


    if file_path:
        with open(file_path, 'r') as file:
            content=file.read()
        editor.setPlainText(content)
        current_file_path = file_path
        print(f"File opened: {file_path}")
