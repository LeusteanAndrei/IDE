from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QTextEdit, QLineEdit, 
                         QPushButton, QHBoxLayout, QLabel, QFontDialog)
from PyQt5.QtCore import QProcess, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QTextCharFormat, QColor, QTextCursor
import google.generativeai as genai
import re


local_api_key = ""


class AiThread(QThread):
    response_signal  = pyqtSignal(str)
    error_signal = pyqtSignal(str)

    def __init__(self, ai_model, user_text, file_content=None):
        super().__init__()
        self.ai_model = ai_model
        self.user_text = user_text
        self.file_content = file_content

    def run(self):
        try:
            # This runs in a separate thread
            response = self.ai_model.ask_question(
                user_text=self.user_text, 
                file_content=self.file_content
            )
            # Emit the response back to the main thread
            self.response_signal.emit(response)
        except Exception as e:
            # Emit error back to the main thread
            self.error_signal.emit(str(e))

class AiModel:
    def __init__(self, api_key,   model = "gemini-1.5-flash"):
        from huggingface_hub import InferenceClient
        self.api_key = api_key
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)



    def read_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def ask_question(self, user_text, file_content = None):
        message =  f"{user_text}\n\nThe current opened_file has: {file_content}" if file_content else f"{user_text}\n\n"

        received = self.model.generate_content(message)
        return received.text

class ClickableTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        
    def mousePressEvent(self, event):
        cursor = self.cursorForPosition(event.pos())
        format = cursor.charFormat()
        
        # Select the whole button text when clicked
        cursor.movePosition(QTextCursor.StartOfBlock, QTextCursor.MoveAnchor)
        cursor.movePosition(QTextCursor.EndOfBlock, QTextCursor.KeepAnchor)
        text = cursor.selectedText()
        
        # Check if we clicked on a button
        if text.strip().startswith("[Insert Code") and text.strip().endswith("]"):
            try:
                index = int(text.strip().split()[2].rstrip("]")) - 1
                if 0 <= index < len(self.parent.code_blocks):
                    self.parent.insert_code(self.parent.code_blocks[index])
            except (IndexError, ValueError):
                pass
        else:
            super().mousePressEvent(event)

class ChatWidget(QWidget):
    def __init__(self, ui):
        super().__init__()
        global local_api_key

        self.ai_model = AiModel(api_key=local_api_key)
        self.setWindowTitle("AI Chat Widget")
        self.setMinimumWidth(500)

        self.ui = ui

        # Chat display with improved styling
        self.chat_area = ClickableTextEdit(self)  # Use our custom QTextEdit
        self.chat_area.setReadOnly(True)
        self.chat_area.setStyleSheet("""
            QTextEdit {
                color: white;
                background-color: #2b2b2b;
                border: 1px solid #3b3b3b;
                border-radius: 5px;
                padding: 5px;
                font-family: 'Consolas', monospace;
                font-size: 12px;
            }
        """)

        # Buttons layout for permanent buttons
        button_layout = QHBoxLayout()
        
        # New Chat button
        self.new_chat_button = QPushButton("New Chat")
        self.new_chat_button.setStyleSheet("""
            QPushButton {
                background-color: #2d5a27;
                color: white;
                border: none;
                padding: 5px 15px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #3d7a37;
            }
        """)
        self.new_chat_button.clicked.connect(self.new_chat)
        
        button_layout.addWidget(self.new_chat_button)
        button_layout.addStretch()

        # Input box + Send button with improved styling
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Type your message here...")
        self.input_box.setStyleSheet("""
            QLineEdit {
                color: white;
                background-color: #3b3b3b;
                border: 1px solid #4b4b4b;
                border-radius: 3px;
                padding: 5px;
                font-family: 'Consolas', monospace;
            }
        """)
        self.input_box.returnPressed.connect(self.send_message)

        self.send_button = QPushButton("Send")
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #2b5b87;
                color: white;
                border: none;
                padding: 5px 15px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #3b6b97;
            }
        """)
        self.send_button.clicked.connect(self.send_message)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_box)
        input_layout.addWidget(self.send_button)

        # Title with better styling
        title_label = QLabel("AI Chat")
        title_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 5px;
            }
        """)

        # Overall layout
        layout = QVBoxLayout()
        layout.addWidget(title_label)
        layout.addLayout(button_layout)
        layout.addWidget(self.chat_area)
        layout.addLayout(input_layout)

        self.setLayout(layout)

        # Store messages for context
        self.messages = [{"role": "system", "content": "You are a helpful AI assistant."}]
        self.code_blocks = []  # Store all code blocks
        self.aiThread = None

        if local_api_key == "":
            self.chat_area.append("To use the AI model, please set your API key in the code.")
            self.input_box.setPlaceholderText("Please enter the API key: ")
            
    def new_chat(self):
        self.chat_area.clear()
        self.messages = [{"role": "system", "content": "You are a helpful AI assistant."}]
        self.code_blocks = []
        
    def insert_code(self, code):
        if code and self.ui.plainTextEdit.text_edit:
            cursor = self.ui.plainTextEdit.text_edit.textCursor()
            cursor.insertText(code)
            
    def extract_code_blocks(self, text):
        # Extract code blocks between triple backticks
        code_blocks = re.findall(r'```(?:\w+\n)?(.*?)```', text, re.DOTALL)
        self.code_blocks = [block.strip() for block in code_blocks]
        return code_blocks

    def send_message(self):

        global local_api_key
        if local_api_key == "":
            api_key = self.input_box.text().strip()
            if not api_key:
                self.chat_area.append("Please enter a valid API key.")
                return
            self.ai_model = AiModel(api_key=api_key)
            local_api_key = api_key
            self.chat_area.append("API key set successfully. You can now start chatting.")
            return

        user_text = self.input_box.text().strip()
        if not user_text:
            return
        
        file_content = self.ui.plainTextEdit.text_edit.toPlainText() 

        # Format user message with a different style
        format = QTextCharFormat()
        format.setForeground(QColor("#88cc88"))  # Light green for user messages
        self.chat_area.setCurrentCharFormat(format)
        self.chat_area.append("You:")
        
        format = QTextCharFormat()
        format.setForeground(QColor("white"))
        self.chat_area.setCurrentCharFormat(format)
        self.chat_area.append(f"  {user_text}\n")  # Indent the message and add extra newline

        # Show thinking indicator with different style
        format = QTextCharFormat()
        format.setForeground(QColor("#888888"))  # Gray for the thinking indicator
        self.chat_area.setCurrentCharFormat(format)
        self.chat_area.append("AI is thinking...\n")  # Add newline after thinking indicator

        self.send_button.setEnabled(False)
        self.input_box.setEnabled(False)

        self.aiThread = AiThread(
            ai_model=self.ai_model, 
            user_text=user_text, 
            file_content=file_content
        )
        self.aiThread.response_signal.connect(self.display_response)
        self.aiThread.error_signal.connect(self.error_processing)
        self.aiThread.finished.connect(self.finished_processing)
        self.aiThread.start()

    def display_response(self, response):
        cursor = self.chat_area.textCursor()
        cursor.movePosition(cursor.End)
        cursor.select(cursor.BlockUnderCursor)
        cursor.removeSelectedText()
        cursor.deletePreviousChar()
        cursor.deletePreviousChar()  # Remove the extra newline from thinking indicator

        # Add AI prefix with style
        format = QTextCharFormat()
        format.setForeground(QColor("#88aaff"))  # Light blue for AI indicator
        self.chat_area.setCurrentCharFormat(format)
        self.chat_area.append("AI:")
        self.chat_area.insertPlainText("\n")  # Add a line break after the AI prefix

        # Extract code blocks before processing the response
        code_blocks = self.extract_code_blocks(response)
        
        # Split the response into parts (code and non-code)
        parts = re.split(r'(```.*?```)', response, flags=re.DOTALL)
        
        for i, part in enumerate(parts):
            if part.strip().startswith('```') and part.strip().endswith('```'):
                code_index = len([p for p in parts[:i] if p.strip().startswith('```')])
                
                # Create a clickable button-like text
                format = QTextCharFormat()
                format.setBackground(QColor("#2b5b87"))
                format.setForeground(QColor("white"))
                self.chat_area.setCurrentCharFormat(format)
                self.chat_area.insertPlainText(f"[Insert Code {code_index + 1}]")
                
                # Reset format and add newline
                format = QTextCharFormat()
                format.setForeground(QColor("white"))
                self.chat_area.setCurrentCharFormat(format)
                self.chat_area.insertPlainText("\n")
                
                # Format code blocks
                format = QTextCharFormat()
                format.setForeground(QColor("#a8d7fe"))
                format.setBackground(QColor("#1e1e1e"))
                self.chat_area.setCurrentCharFormat(format)
                
                # Remove the triple backticks and language identifier
                code = re.sub(r'```\w*\n?|\n?```', '', part)
                self.chat_area.insertPlainText(code)
                self.chat_area.insertPlainText("\n\n")
            else:
                # Reset format for normal text
                format = QTextCharFormat()
                format.setForeground(QColor("white"))
                self.chat_area.setCurrentCharFormat(format)
                self.chat_area.insertPlainText("  " + part)  # Indent normal text

        self.chat_area.insertPlainText("\n\n")  # Add extra space between messages
        self.chat_area.verticalScrollBar().setValue(self.chat_area.verticalScrollBar().maximum())  # Auto-scroll to bottom
        
    def mousePressEvent(self, event):
        cursor = self.chat_area.cursorForPosition(event.pos())
        cursor.select(QTextCursor.WordUnderCursor)
        text = cursor.selectedText()
        
        # Check if we clicked on an insert button
        if text.startswith("[Insert") and text.endswith("]"):
            try:
                index = int(text.split()[2].rstrip("]")) - 1
                if 0 <= index < len(self.code_blocks):
                    self.insert_code(self.code_blocks[index])
            except (IndexError, ValueError):
                pass

    def error_processing(self, error_message):
        cursor = self.chat_area.textCursor()
        cursor.movePosition(cursor.End)
        cursor.select(cursor.BlockUnderCursor)
        cursor.removeSelectedText()
        cursor.deletePreviousChar()

        self.chat_area.append(f"Error: {error_message}")

    def finished_processing(self):
        self.send_button.setEnabled(True)
        self.input_box.setEnabled(True)
        self.input_box.clear()

        self.aiThread = None

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    widget = ChatWidget()
    widget.show()
    sys.exit(app.exec_())


