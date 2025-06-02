from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QHBoxLayout, QLabel
from PyQt5.QtCore import QProcess
from PyQt5.QtCore import QThread, pyqtSignal
import google.generativeai as genai


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
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)



    def read_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def ask_question(self, user_text, file_content = None):
        message =  f"{user_text}\n\nThe current opened_file has: {file_content}" if file_content else f"{user_text}\n\n"

        received = self.model.generate_content(message)
        return received.text



class ChatWidget(QWidget):
    def __init__(self, ui):
        super().__init__()

        self.ai_model = AiModel(api_key=local_api_key)
        self.setWindowTitle("AI Chat Widget")
        # self.resize(600, 500)

        self.ui = ui

        # Chat display
        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        self.chat_area.setStyleSheet("color:white;")
        

        # Input box + Send button
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Type your message here...")
        self.input_box.setStyleSheet("color:white;")
        self.input_box.returnPressed.connect(self.send_message)


        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_box)
        input_layout.addWidget(self.send_button)

        # Overall layout
        layout = QVBoxLayout()
        layout.addWidget(QLabel("AI Chat"))
        layout.addWidget(self.chat_area)
        layout.addLayout(input_layout)

        self.setLayout(layout)

        # Store messages for context
        self.messages = [{"role": "system", "content": "You are a helpful AI assistant."}]

        self.aiThread = None


    def send_message(self):


        user_text = self.input_box.text().strip()
        if not user_text:
            return
        
        file_content = self.ui.plainTextEdit.text_edit.toPlainText() 

        self.chat_area.append(f"You: {user_text}")
        self.chat_area.append("Thinking...")

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

        self.chat_area.append(f"AI: {response}")

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


