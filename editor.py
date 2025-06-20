from PyQt5.QtWidgets import QMainWindow, QApplication, QPlainTextEdit, QWidget, QVBoxLayout, QListWidget, QToolTip
from PyQt5.QtCore import QProcess, Qt, QTimer, pyqtSignal, QEvent
from PyQt5.QtGui import QTextCursor
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut



import tempfile, os, sys, json
from lsp import requests, logger
from Highlighter.highlighter import cPlusPlusHighlighter
from Styles import style
import subprocess


Log = logger.Logger("lsp.log")

class TextEditor(QPlainTextEdit):
    
    textChangedWithIndex = pyqtSignal(int)
    
    def __init__(self, file_path = None, tab_index=None):
        super().__init__()
        self.file_path = file_path
        self.saved = True  # Start as saved
        self.up_to_date = True
        self.tab_index = tab_index
        self.ignore_text_changed = False
        self.textChanged.connect(self.handle_text_changed)  # Connect to textChanged signal


        self.font_size = style.EDITOR_FONT_SIZE
        self.background_color = "#23272b"
        self.font_family = self.font().family()  # Get the default font family
        self.apply_style()

    def handle_text_changed(self):
        if self.ignore_text_changed:
            return
        self.saved = False  # Mark as unsaved when text changes
        if self.tab_index is not None:
            self.textChangedWithIndex.emit(self.tab_index)

    def readContent(self):
        if self.file_path and os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                content = file.read()
                return content
        return "Nope, nothing here"
    
    def insert_multiple_line_comment(self):
        cursor = self.textCursor()
        comment_block = "\n/*\n\n*/\n"
        cursor.insertText(comment_block)
        # Move cursor between the newlines for convenience
        cursor.movePosition(QTextCursor.PreviousBlock)
        self.setTextCursor(cursor)
        
    def keyPressEvent(self, e):
        super().keyPressEvent(e)
        # We don't need to emit textChangedWithIndex here anymore since we're using textChanged signal
        if e.key() != Qt.Key.Key_Down and e.key() != Qt.Key.Key_Up and e.key() != Qt.Key.Key_Right and e.key() != Qt.Key.Key_Left:
            self.up_to_date = False

    def apply_style(self):
        if self.font_size is not None:
            font = self.font()
            font.setPointSize(self.font_size)
            self.setFont(font)

        # if self.background_color is not None:
        #     self.setStyleSheet(style.EDITOR_STYLE+ f"background-color: {self.background_color};")
        bg = getattr(self, "background_color", "#23272b")
        fg = getattr(self, "font_color", "#ffffff")
        self.setStyleSheet(style.EDITOR_STYLE + f"background-color: {bg}; color: {fg};")
        if self.font_family is not None:
            font = self.font()
            font.setFamily(self.font_family)
            self.setFont(font)

    def show(self):
        super().show()

        self.apply_style()
        self.update()  # Refresh the editor to apply changes
        

class LspProcess():

    def __init__(self, editor):
        self.editor = editor
        self.text_edit = editor.text_edit
        self.lsp_process = None
        self.version = 0
        self.temp_file_path = None
        self.temp_file_uri = None
        self.lsp_path = "./LLVM/bin/clangd.exe"

    def initialize_lsp(self):
        self.create_temporary_file()

        self.lsp_process = QProcess()
        self.lsp_process.setProcessChannelMode(QProcess.MergedChannels)
        # ii spune ca stdOutput si StdError sunt pe acelasi canal
       
        self.lsp_process.start(self.lsp_path)

        if not self.lsp_process.waitForStarted(5000):
            # daca nu a inceput dupa 5 sec eroare
            Log.logger.error("Failed to start LSP process.")
            raise Exception("Failed to start LSP process.")
        Log.logger.info("LSP process started successfully.")

        self.lsp_process.readyReadStandardOutput.connect(self.handle_response)

        self.initialize_request()
    
    def initialize_request(self):
        req = requests.Requests().getInitializeRequest(self.lsp_process.processId())
        self.send_request(req)

    def send_request(self, message): 
        method = message['method']
        message = json.dumps(message)
        message_in_bytes = f"Content-Length: {len(message)}\r\n\r\n{message}".encode("utf-8")
        # formatul de sus e formatul standard pt requesturi LSP
        self.lsp_process.write(message_in_bytes)
        Log.logger.info(f"Request sent with method {method}")        

    def handle_hover(self, message):
        if  message['result']:
            contents = message['result']['contents']
            if isinstance(contents, dict) and 'value' in contents:
                hover_text = contents['value']
                self.editor.showHover(hover_text)
                Log.logger.info(f"Hover text: {hover_text}")
            else:
                Log.logger.warning("Hover response does not contain expected format.")
        else:
            Log.logger.warning("Hover response does not contain 'contents'.")

    def handle_response(self):
        # if not self.lsp_process or not hasattr(self.lsp_process, 'canReadLine'):
        #     return
        # if self.lsp_process.state() != QProcess.Running:
        #     return
        while self.lsp_process.canReadLine():
            line = self.lsp_process.readLine()
            # intoarce un QByteArray si trb convertit in str
            line_string = line.data().decode("utf-8").strip()

            if line_string.startswith("Content-Length:"):
                Log.logger.info("Handling response from LSP")

                '''
                    mesajul e de forma
                    content-length: 1234

                    si un json de lungime 1234 cu inf necesare, pe noi ne intereseaza json-ul
                '''
                length = int(line_string.split(":")[1].strip())
                self.lsp_process.readLine() #citim o linie goala pt ca asa e format-ul :)) sunt detalii pe site-ul lsp

                json_in_bytes = self.lsp_process.read(length)

                try:
                    json_in_string = json_in_bytes.decode("utf-8")

                    #urm 3 linii sunt doar pt logging, pt a avea usor mesajul de citit la debugging
                    aux = json.loads(json_in_string)
                    formatted_json = json.dumps(aux, indent=4)
                    Log.logger.info(f"Received response: {formatted_json}")


                    self.handle_message(json.loads(json_in_string))
                except UnicodeDecodeError as e:
                    Log.logger.error(f"Failed to decode response: {e}")
                    # raise e
                except json.JSONDecodeError as e:
                    Log.logger.error(f"Failed to parse JSON response: {e}")
                    # raise e

    def handle_message(self, message):
        if 'method' in message:
            match message['method']:
                case 'textDocument/publishDiagnostics':
                    Log.logger.info("Diagnostics received from LSP.")
                    self.handle_diagnostics(message)
        elif 'result' in message:
            match message['id']:
                case 0:
                    # in acest caz e raspunsul la request ul de initializare
                    # pt id-uri in reqests.py e id-ul fiecaruai pus de mine, tre doar sa fie unic
                    # momentan 0 - initializare, 1 - completion
                    Log.logger.info("LSP initialized successfully.")
                    # tre acum sa ii spunem sa deschidem documentul
                    self.open_document()
                case 1:
                    Log.logger.info("Received a completion response from LSP.")
                    self.handle_completion(message)
                    self.editor.completion_popup.show_completions()
                case 2:
                    Log.logger.info("Received hover response.")
                    self.handle_hover(message)

    def handle_diagnostics(self, message):  
        # return
        diagnostics = message['params']['diagnostics']
        errors = []
        if diagnostics:
            for diagnostic in diagnostics: 
                if diagnostic['severity'] == 1: # 1 = error, 2 = warning            
                    error_line = diagnostic['range']['start']['line'] 
                    error_line_end = diagnostic['range']['end']['line']
                    error_start =  diagnostic['range']['start']['character']
                    error_end = diagnostic['range']['end']['character']
                    if error_line == error_line_end:
                        errors.append(Error(error_line, error_start, error_end, diagnostic['message']))
                        # errors  = errors + [[error_line, [error_start, error_end]]]
        self.editor.highlighter.errors = errors
        self.editor.highlighter.rehighlight()
        Log.logger.info(f"Errors received: {self.editor.highlighter.errors}")
   
    def open_document(self):
        text = self.text_edit.toPlainText()
        notification = requests.Requests().getOpenDocument(self.temp_file_uri, text, self.version)
        self.send_request(notification)

    def handle_completion(self, message):
        result = message['result']['items']
        completions = []
        for item in result:
            text = item['insertText']
            completions.append(text)
        self.editor.completion_popup.completion_words.clear()
        self.editor.completion_popup.completion_words = completions
        Log.logger.info(f"Completions received: {self.editor.completion_words}")
    
    def create_temporary_file(self):
        # avem nevoie de un fisier temporar pt a putea lucra cu modificarile curente, fara a fi nevoie sa salvam totimpul
        if hasattr(self, 'temp_file'):
            self.temp_file.close()
        
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".cpp", mode = "w+")
        self.temp_file_path = self.temp_file.name
        self.temp_file_uri = "file://" + self.temp_file_path.replace("\\", "/")
        Log.logger.info(f"Temporary file created: {self.temp_file_path}")

    def rewrite_temp_file(self):
        if not hasattr(self, 'temp_file') or self.temp_file.closed:
            self.create_temporary_file()
            
        text = self.text_edit.toPlainText()
        self.temp_file.seek(0)  
        self.temp_file.truncate() # stergem ce era in el  
        self.temp_file.write(text)
        self.temp_file.flush()  # ne asiguram ca s-a bagat tot
        Log.logger.info(f"Updated temporary file {self.temp_file_path}")
    
    def sync_document(self):
        text = self.text_edit.toPlainText()
        self.version += 1
        change_notification = requests.Requests().changeNotification(text, self.temp_file_uri, self.version)
        self.send_request(change_notification)
    
    def get_completion(self):
        cursor = self.text_edit.textCursor()
        line = cursor.blockNumber()
        column = cursor.columnNumber()

        request = requests.Requests().getCompletionRequest(self.temp_file_uri, line, column)
        self.send_request(request)

    def text_change(self):
        self.rewrite_temp_file()
        self.sync_document()

    def shutdown(self):
        if self.lsp_process is not None:
            # self.lsp_process.kill()
            # self.lsp_process.close()
            # self.lsp_process = None
            # Log.logger.info("LSP process shut down successfully.")
            try:
                # self.lsp_process.readAllStandardOutput.disconnect()

                if self.lsp_process.state() == QProcess.Running:
                    shutdown_request = requests.Requests().getShutdownRequest()
                    self.send_request(shutdown_request)

                    exit_request = requests.Requests().getExitRequest()
                    self.send_request(exit_request)

                    if not self.lsp_process.waitForFinished(3000):
                        Log.logger.warning("LSP process didn't shut down gracefully, forcing termination...")
                        self.lsp_process.kill()
                        self.lsp_process.waitForFinished(1000)  

                self.lsp_process.close()
                self.lsp_process.deleteLater()
                self.lsp_process = None
                Log.logger.info("LSP process shut down successfully.")

            except Exception as e:
                Log.logger.error(f"Error disconnecting from LSP process: {e}")

                if self.lsp_process:
                    try:
                        self.lsp_process.kill()
                        self.lsp_process.waitForFinished(1000)

                        self.lsp_process.close()
                        self.lsp_process.deleteLater()
                    except:
                        pass
                    self.lsp_process = None

    def restart(self):
        if self.lsp_process is not None:
            self.shutdown()
            self.initialize_lsp()
            Log.logger.info("LSP process restarted successfully.")
        else:
            Log.logger.error("LSP process is not running, cannot restart.")

class Editor(QWidget):

    def __init__(self, text_edit = None):
        super().__init__()
        self.setObjectName("plainTextEdit")
        self.setStyleSheet("border: none; background: #344955;")

        self.current_file_name = None
        self.current_file_path = None
        self.text_edit = text_edit if text_edit else TextEditor()

        self.text_edit.setCursorWidth(0)  # Elimină linia de cursor

        self.setup_layout()
        self.text_edit.keyPressEvent = self.keyPressEvent
        self.setup_lsp()
        self.setup_completions()
        self.setup_hover()
        self.set_highlighter()

    def setup_hover(self):

        self.text_edit.setAttribute(Qt.WA_Hover, True)
        self.text_edit.viewport().setAttribute(Qt.WA_Hover, True)

        
        self.text_edit.setMouseTracking(True)
        self.text_edit.viewport().installEventFilter(self)

        self.hover_timer = QTimer(self)
        self.hover_timer.setSingleShot(True)
        self.hover_timer.timeout.connect(self.show_hover)

        self.last_hover = None
        QToolTip.setFont(self.text_edit.font())

    def setup_completions(self):

        self.completion_words = []
        self.completion_popup = Completion_Popup(self)
        self.completion_popup.hide()
        self.layout.addWidget(self.completion_popup)

    def setup_lsp(self):
        self.Lsp = LspProcess(self)
        self.Lsp.initialize_lsp()

    def setup_layout(self):

        self.container = QWidget()
        self.layout = QVBoxLayout(self.container)
        self.layout.addWidget(self.text_edit)
        self.container.setLayout(self.layout)
        self.setLayout(self.layout)

    def show_hover(self):
       

        cursor = self.text_edit.cursorForPosition(self.last_hover)
        cursor.select(QTextCursor.WordUnderCursor)
        word = cursor.selectedText().strip()
        print(word)
        for error in self.highlighter.errors:
            if error.line == cursor.blockNumber() and error.column_start <= cursor.columnNumber() <= error.column_end:
                QToolTip.showText(self.text_edit.mapToGlobal(self.last_hover), error.message, self.text_edit)
                return

        if len(word) != 0:
            hover_request = requests.Requests().getHoverRequest(self.Lsp.temp_file_uri, cursor.blockNumber(), cursor.columnNumber())
            self.Lsp.send_request(hover_request)

    def set_highlighter(self):
        self.highlighter = cPlusPlusHighlighter(self, self.text_edit.document())

    def eventFilter(self, source, event):
        if source == self.text_edit.viewport() :
            if event.type() == QEvent.HoverMove:
                if not self.isActiveWindow():
                    QToolTip.hideText()
                    self.hover_timer.stop()
                    return True

                current_position = event.pos()
                if self.last_hover != current_position:
                    QToolTip.hideText()
                    self.hover_timer.stop()
                    self.last_hover = current_position
                    self.hover_timer.start(1000)

                return True
            
            elif event.type() == event.HoverLeave:
                QToolTip.hideText()
                self.hover_timer.stop()
                return True
        elif event.type() == event.WindowDeactivate:
            QToolTip.hideText()
            self.hover_timer.stop()
        elif event.type() == event.WindowActivate:
            self.hover_timer.start(1000)
        return super().eventFilter(source, event)

    def showHover(self, hover_text):
        QToolTip.showText(self.text_edit.mapToGlobal(self.last_hover), hover_text, self.text_edit)

    def keyPressEvent(self, event):

        if event.key() != Qt.Key.Key_Down and event.key() != Qt.Key.Key_Up and event.key() != Qt.Key.Key_Right and event.key() != Qt.Key.Key_Left:
            self.Lsp.text_change()

        if self.completion_popup.isVisible():
            if event.key() == Qt.Key_Tab or event.key() == Qt.Key_Return:
                if self.completion_popup.currentItem():
                    self.completion_popup.insert_completion(self.completion_popup.currentItem())
                return
            elif event.key() == Qt.Key_Escape:
                self.completion_popup.hide()
                return
            elif event.key() == Qt.Key_Down:
                if self.completion_popup.currentRow() < self.completion_popup.count() - 1:
                    self.completion_popup.setCurrentRow(self.completion_popup.currentRow() + 1)
                return
            elif event.key() == Qt.Key_Up:
                if self.completion_popup.currentRow() > 0:
                    self.completion_popup.setCurrentRow(self.completion_popup.currentRow() - 1)
                return
            elif event.key() == Qt.Key_Space:
                self.completion_popup.hide()
        else:
            if event.key() == Qt.Key_Tab:
                cursor = self.text_edit.textCursor()
                start_selection = cursor.selectionStart()
                end_selection = cursor.selectionEnd()

                start_cursor = QTextCursor(self.text_edit.document())
                start_cursor.setPosition(start_selection)
                end_cursor = QTextCursor(self.text_edit.document())
                end_cursor.setPosition(end_selection)

                if start_cursor.blockNumber() != end_cursor.blockNumber():
                    cursor.beginEditBlock()
                    for number in range(start_cursor.blockNumber(), end_cursor.blockNumber()+1):
                        line = self.text_edit.document().findBlockByNumber(number).text()
                        new_line = "\n\t" + line
                        block_cursor = QTextCursor(self.text_edit.document().findBlockByNumber(number))
                        block_cursor.select(QTextCursor.BlockUnderCursor)
                        # print(block_cursor.selectedText())
                        block_cursor.removeSelectedText()
                        block_cursor.insertText(new_line)
                    cursor.endEditBlock()
                else:   
                    cursor.insertText("   ")
                return



        super().keyPressEvent(event)
        super(TextEditor, self.text_edit).keyPressEvent(event)


        triggered_char = ['.', '>', '-', '<']
        triggered_keys = [Qt.Key_Backspace]
        if event.text().isalnum() or event.text() in triggered_char or event.key() in triggered_keys:
            self.Lsp.get_completion()
        
        self.Lsp.sync_document()

    def hide_editor(self):
        self.text_edit.hide()
        self.hide()

    def show_editor(self):
        self.text_edit.show()
        self.show()

    def switch_text_edit(self, textedit):
        if textedit is None:
            return
        
        if self.text_edit is not None:
            self.layout.removeWidget(self.text_edit)
            self.text_edit.hide()

        textedit.ignore_text_changed = True
        self.text_edit = textedit
        self.layout.addWidget(self.text_edit)
        self.text_edit.show()
        self.set_highlighter()
        self.Lsp.rewrite_temp_file()
        self.text_edit.keyPressEvent = self.keyPressEvent
        self.text_edit.setMouseTracking(True)
        self.text_edit.viewport().installEventFilter(self)
        self.setup_hover()

        self.Lsp.shutdown()
        self.setup_lsp()

        # self.text_edit.setStyleSheet(style.EDITOR_STYLE)
        # font = self.text_edit.font()
        # font.setPointSize(style.EDITOR_FONT_SIZE)
        # self.text_edit.setFont(font)

        self.text_edit.ignore_text_changed = False
    
        self.text_edit.apply_style()

    def format_code(self):
        code = self.text_edit.toPlainText()
        clang_format_path = "./LLVM/bin/clang-format.exe"
        try:
            # Run clang-format as a subprocess
            proc = subprocess.run(
                [clang_format_path],
                input=code.encode("utf-8"),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True
            )
            formatted_code = proc.stdout.decode("utf-8")
            self.text_edit.setPlainText(formatted_code)
        except Exception as e:
            print("Formatting failed:", e)       
           
    def insert_multiple_line_comment(self):
        cursor = self.text_edit.textCursor()
        doc = self.text_edit.document()

        # If no selection, select the current line
        if not cursor.hasSelection():
            cursor.select(QTextCursor.LineUnderCursor)

        start = cursor.selectionStart()
        end = cursor.selectionEnd()

        # Expand selection to full lines
        start_block = doc.findBlock(start)
        end_block = doc.findBlock(end)
        if end_block.position() == end:
            end_block = end_block.previous()

        # Collect all lines in the selection
        blocks = []
        block = start_block
        while True:
            blocks.append(block)
            if block == end_block:
                break
            block = block.next()

        lines = [block.text() for block in blocks]
        comment_block = "\n".join(lines)

        # Prepare the block comment with extra newlines before and after
        # This will insert 2 empty lines before and after the block comment
        new_text = "\n\n/*\n\n*/\n\n" + comment_block

        # Replace the selected lines with the block comment and push the text down
        cursor.beginEditBlock()
        cursor.setPosition(start_block.position())
        cursor.setPosition(end_block.position() + end_block.length() - 1, QTextCursor.KeepAnchor)
        cursor.removeSelectedText()
        cursor.insertText(new_text)
        cursor.endEditBlock()
        self.text_edit.setTextCursor(cursor)
        
    def comment_line_or_selection(self):
        """Toggle comment on the current line or all selected lines."""
        cursor = self.text_edit.textCursor()
        doc = self.text_edit.document()

        # If no selection, select the current line
        if not cursor.hasSelection():
            cursor.select(QTextCursor.LineUnderCursor)

        start = cursor.selectionStart()
        end = cursor.selectionEnd()

        # Expand selection to full lines
        start_block = doc.findBlock(start)
        end_block = doc.findBlock(end)
        # If selection ends at the start of a block, don't include that block
        if end_block.position() == end:
            end_block = end_block.previous()

        # Collect all lines in the selection
        blocks = []
        block = start_block
        while True:
            blocks.append(block)
            if block == end_block:
                break
            block = block.next()

        lines = [block.text() for block in blocks]
        comment_block= "\n".join(lines)

        # Decide to comment or uncomment
        if all(line.strip().startswith("//") for line in lines if line.strip()):
            # Uncomment
            new_lines = [line.replace("//", "", 1) if line.strip().startswith("//") else line for line in lines]
        elif comment_block.strip().startswith("/*") and comment_block.strip().endswith("*/"):
            new_lines = [line.replace("/*", "", 1).replace("*/", "", 1) for line in lines]
        else:
            # Comment
            new_lines = ["//" + line if line.strip() else line for line in lines]

        # Replace the selected lines with new_lines
        cursor.beginEditBlock()
        # Select from start of first block to end of last block
        cursor.setPosition(start_block.position())
        cursor.setPosition(end_block.position() + end_block.length() - 1, QTextCursor.KeepAnchor)
        cursor.removeSelectedText()
        cursor.insertText('\n'.join(new_lines))
        cursor.endEditBlock()
        self.text_edit.setTextCursor(cursor)
      
class Completion_Popup(QListWidget):
    def __init__(self, parent=None):


        super().__init__(parent)
        self.parent = parent
        self.setWindowFlag(Qt.ToolTip)
        self.setFocusPolicy(Qt.NoFocus)
        self.setMaximumHeight(100)
        self.setMaximumWidth(300)
        self.hide()

        self.itemClicked.connect(self.insert_completion)

        self.completion_words = []
        
        self.setCss()

    def setCss(self):
        self.setStyleSheet(style.COMPLETION_POPUP_STYLE)

    def insert_completion(self, item):
        completion = item.text()

        cursor = self.parent.text_edit.textCursor()
        cursor.select(QTextCursor.WordUnderCursor)
        cursor.removeSelectedText()
        cursor.insertText(completion)

        self.hide()

    
    def show_completions(self):

        cursor = self.parent.text_edit.cursorRect()
        cursor_global_coordinates = self.parent.text_edit.mapToGlobal(cursor.bottomLeft())
        cursor_local_coordinates = self.parent.container.mapFromGlobal(cursor_global_coordinates)
        self.move(cursor_local_coordinates.x(), cursor_local_coordinates.y() + 5)

        cursor = self.parent.text_edit.textCursor()
        cursor.select(QTextCursor.WordUnderCursor)
        word = cursor.selectedText().strip()

        if len(word) == 0:
            self.hide()
            return
    
        good_completions = [
            comp for comp in self.completion_words if comp.startswith(word)
        ]

        if good_completions:
            self.clear()
            self.addItems(good_completions)
            self.show()
            self.setCurrentRow(0)
        else:
            self.hide()

class Error:
    def __init__(self, line, column_start, column_end, message):
        self.line = line
        self.column_start = column_start
        self.column_end = column_end
        self.message = message

    def __repr__(self):
        return f"Error(line={self.line}, column={self.column_start}, column_end = {self.column_end}, message={self.message})"

class Utility_Functions:

    def undo(editor):
        editor.text_edit.undo()
    
    def redo(editor):
        editor.text_edit.redo()

    def cut(editor):
        editor.text_edit.cut()  

    def copy(editor):
        editor.text_edit.copy()

    def paste(editor):
        editor.text_edit.paste()

    def zoom_in(editor):
        editor.text_edit.zoomIn(1)

    def zoom_out(editor):
        editor.text_edit.zoomOut(1)

    def select_all(editor):
        editor.text_edit.selectAll()

    
if __name__ == "__main__":



    app = QApplication(sys.argv)

    texteditor1 = TextEditor()
    texteditor2 = TextEditor()

    editor = Editor(text_edit=texteditor1)
    editor.text_edit = texteditor1

    editor.showMaximized()
    editor.show()


    shortcut = QShortcut(QKeySequence("Ctrl+Tab"), editor)
    shortcut.activated.connect(lambda: editor.switch_text_edit(texteditor2))
    shortcut2 = QShortcut(QKeySequence("Ctrl+Shift+Tab"), editor)
    shortcut2.activated.connect(lambda: editor.switch_text_edit(texteditor1))



    sys.exit(app.exec_())
