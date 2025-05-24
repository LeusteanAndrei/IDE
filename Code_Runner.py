from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5 import QtCore
from PyQt5.QtCore import QProcess, QTimer
import os
import subprocess

class Code_Runner:
    def __init__(self, ui):
        self.ui = ui
        self.run_process = None
        self.output_code = None
        self.start_time = None
        self.end_time = None

        self.output = Output()
        self.input = Input()

        self.run_button = self.ui.sections[self.ui.section_names.index("Run")]
        self.run_button.clicked.connect(self.run_code)

    def abort_run(self):
        print("Abort Run")
        if self.run_process:
            self.end_time = QtCore.QDateTime.currentMSecsSinceEpoch() / 1000.0
            self.run_process.kill()
            self.run_process.waitForFinished()
            self.run_process = None
            self.output.clear()
            if len(self.output_code) > 100000:
                self.output_code = self.output_code[-100000:] + "......."
            self.output.appendPlainText("Run aborted.\nOutput:\n")
            self.output.appendPlainText(self.output_code)
            self.output.appendPlainText(f"Execution time: {self.end_time - self.start_time:.2f} seconds")
            self.dot_timer.stop()
            self.run_button.setEnabled(True)  # Re-enable the button after execution

    def run_code(self):
        # if self.run_process:
        #     return

        self.run_button.setEnabled(False)  # Disable the button to prevent multiple clicks

        """Compile and run the current file."""
        current_index = self.ui.file_tab_bar.currentIndex()
        file_state = self.ui.file_tab_bar.file_states[current_index]

        # Check if the file is saved - asa ne obliga sa salvam o copie a fisierului inainte de a da run si apoi va functiona
        if not file_state["saved"]:
            self.ui.handle_save_file()  # Save the file before running

        # Get the current file path
        file_path = file_state["file_path"]
        if not file_path:
            self.output.clear()
            self.output.appendPlainText("Error: No file to run.")
            self.run_button.setEnabled(True)
            return

        # Compile the file
        file_directory = os.path.dirname(file_path)
        executable_file_name = os.path.basename(file_path).split(".")[0] + ".exe"

            
        command = ["LLVM/bin/clang++.exe", file_path, "-o", os.path.join(file_directory, executable_file_name)]

        self.ui.tab_widget.setTabVisible(2, True)
        self.ui.tab_widget.setCurrentIndex(2)


        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode != 0:
            self.output.clear()
            self.output.appendPlainText("Compilation Error:\n")
            self.output.appendPlainText(result.stderr)
            self.run_button.setEnabled(True)
            return


        self.run_process = QProcess()

        run_command = os.path.join(file_directory, executable_file_name)

        self.start_time = QtCore.QDateTime.currentMSecsSinceEpoch() / 1000.0
        self.output_code = ""



        self.run_process.start(run_command)
        self.run_process.readyReadStandardOutput.connect(self.display_run_output)
        
        input_text = self.input.toPlainText()
        if input_text:
            self.run_process.write(input_text.encode())
        self.run_process.closeWriteChannel()


        self.run_process.finished.connect(self.run_finished)


        self.print_running_output()
    
    def display_run_output(self):
        output = self.run_process.readAllStandardOutput().data().decode()
        self.output_code += output
        if len(self.output_code) > 100000:
            self.output_code = self.output_code[-100000:] 
    
    def run_finished(self):
        self.output.clear()
        self.output.appendPlainText("Execution Output:\n")
        self.output.appendPlainText(self.output_code)
        self.run_process.close()
        self.run_process = None
        self.dot_timer.stop()
        self.end_time = QtCore.QDateTime.currentMSecsSinceEpoch() / 1000.0
        self.output.appendPlainText(f"\nExecution time: {self.end_time - self.start_time:.2f} seconds")
        self.run_button.setEnabled(True)  # Re-enable the button after execution is finished

    def print_running_output(self):
        self.output.clear()
        self.output.appendPlainText("Running")
        self.dots = ""
        self.dot_timer = QTimer(self.output)
        self.dot_timer.setInterval(1000)
        def update_dots():
            if len(self.dots) < 3:
                self.dots += "."
            else:
                self.dots = "."
            self.output.clear()
            self.output.appendPlainText("Running" + self.dots)
        self.dot_timer.timeout.connect(update_dots)
        self.dot_timer.start()

class Output(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
        self.setObjectName("output")
        self.setMinimumHeight(100)

class Input(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.setReadOnly(False)
        self.setObjectName("input")
        self.setMinimumHeight(100)