from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QCheckBox)
from PyQt5.QtCore import Qt, pyqtSignal
from Styles import style

class FindDialog(QDialog):
    findNext = pyqtSignal(str, bool, bool)  # search text, whole words, case sensitive
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Find")
        self.setFixedSize(400, 180)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Search text input
        search_layout = QHBoxLayout()
        search_label = QLabel("Find:")
        search_label.setStyleSheet("color: #78A083; font-size: 16px;")
        self.search_input = QLineEdit()
        self.search_input.setStyleSheet("""
            QLineEdit {
                background-color: #181b1f;
                color: #e0e0e0;
                border: 2px solid #78A083;
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
            }
        """)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)
        
        # Options
        options_layout = QHBoxLayout()
        self.case_sensitive = QCheckBox("Match case")
        self.whole_word = QCheckBox("Whole words")
        for checkbox in [self.case_sensitive, self.whole_word]:
            checkbox.setStyleSheet("""
                QCheckBox {
                    color: #78A083;
                    font-size: 14px;
                    spacing: 8px;
                }
                QCheckBox::indicator {
                    width: 18px;
                    height: 18px;
                    background-color: #181b1f;
                    border: 2px solid #78A083;
                    border-radius: 4px;
                }
                QCheckBox::indicator:checked {
                    background-color: #78A083;
                }
            """)
        options_layout.addWidget(self.case_sensitive)
        options_layout.addWidget(self.whole_word)
        layout.addLayout(options_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.find_btn = QPushButton("Find Next")
        self.cancel_btn = QPushButton("Cancel")
        
        for button in [self.find_btn, self.cancel_btn]:
            button.setStyleSheet("""
                QPushButton {
                    background-color: #344955;
                    color: #78A083;
                    border: 2px solid #78A083;
                    border-radius: 8px;
                    padding: 8px 16px;
                    font-size: 14px;
                    min-width: 100px;
                }
                QPushButton:hover {
                    background-color: #78A083;
                    color: #344955;
                }
            """)
        
        button_layout.addStretch()
        button_layout.addWidget(self.find_btn)
        button_layout.addWidget(self.cancel_btn)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        self.setStyleSheet("background-color: #23272b;")
        
        # Connect signals
        self.find_btn.clicked.connect(self.find_clicked)
        self.cancel_btn.clicked.connect(self.reject)
        self.search_input.returnPressed.connect(self.find_clicked)
        
    def find_clicked(self):
        text = self.search_input.text()
        if text:
            self.findNext.emit(text, self.whole_word.isChecked(), self.case_sensitive.isChecked())

class ReplaceDialog(QDialog):
    findNext = pyqtSignal(str, bool, bool)
    replace = pyqtSignal(str)
    replaceAll = pyqtSignal(str, str, bool, bool)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Find and Replace")
        self.setFixedSize(600, 250)  # Made dialog wider to accommodate buttons
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Find text input
        find_layout = QHBoxLayout()
        find_label = QLabel("Find:")
        find_label.setStyleSheet("color: #78A083; font-size: 16px;")
        self.find_input = QLineEdit()
        self.find_input.setStyleSheet("""
            QLineEdit {
                background-color: #181b1f;
                color: #e0e0e0;
                border: 2px solid #78A083;
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
            }
        """)
        find_layout.addWidget(find_label)
        find_layout.addWidget(self.find_input)
        layout.addLayout(find_layout)
        
        # Replace text input
        replace_layout = QHBoxLayout()
        replace_label = QLabel("Replace with:")
        replace_label.setStyleSheet("color: #78A083; font-size: 16px;")
        self.replace_input = QLineEdit()
        self.replace_input.setStyleSheet("""
            QLineEdit {
                background-color: #181b1f;
                color: #e0e0e0;
                border: 2px solid #78A083;
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
            }
        """)
        replace_layout.addWidget(replace_label)
        replace_layout.addWidget(self.replace_input)
        layout.addLayout(replace_layout)
        
        # Options
        options_layout = QHBoxLayout()
        self.case_sensitive = QCheckBox("Match case")
        self.whole_word = QCheckBox("Whole words")
        for checkbox in [self.case_sensitive, self.whole_word]:
            checkbox.setStyleSheet("""
                QCheckBox {
                    color: #78A083;
                    font-size: 14px;
                    spacing: 8px;
                }
                QCheckBox::indicator {
                    width: 18px;
                    height: 18px;
                    background-color: #181b1f;
                    border: 2px solid #78A083;
                    border-radius: 4px;
                }
                QCheckBox::indicator:checked {
                    background-color: #78A083;
                }
            """)
        options_layout.addWidget(self.case_sensitive)
        options_layout.addWidget(self.whole_word)
        layout.addLayout(options_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.find_btn = QPushButton("Find Next")
        self.replace_btn = QPushButton("Replace")
        self.replace_all_btn = QPushButton("Replace All")
        self.cancel_btn = QPushButton("Cancel")
        
        for button in [self.find_btn, self.replace_btn, self.replace_all_btn, self.cancel_btn]:
            button.setStyleSheet("""
                QPushButton {
                    background-color: #344955;
                    color: #78A083;
                    border: 2px solid #78A083;
                    border-radius: 8px;
                    padding: 8px 16px;
                    font-size: 14px;
                    min-width: 100px;
                }
                QPushButton:hover {
                    background-color: #78A083;
                    color: #344955;
                }
            """)
          # Add buttons with proper spacing
        button_layout.addStretch()
        button_layout.addWidget(self.find_btn)
        button_layout.addSpacing(10)  # Add 10 pixels of space between buttons
        button_layout.addWidget(self.replace_btn)
        button_layout.addSpacing(10)
        button_layout.addWidget(self.replace_all_btn)
        button_layout.addSpacing(10)
        button_layout.addWidget(self.cancel_btn)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        self.setStyleSheet("background-color: #23272b;")
        
        # Connect signals
        self.find_btn.clicked.connect(self.find_clicked)
        self.replace_btn.clicked.connect(self.replace_clicked)
        self.replace_all_btn.clicked.connect(self.replace_all_clicked)
        self.cancel_btn.clicked.connect(self.reject)
        self.find_input.returnPressed.connect(self.find_clicked)
        
    def find_clicked(self):
        text = self.find_input.text()
        if text:
            self.findNext.emit(text, self.whole_word.isChecked(), self.case_sensitive.isChecked())
            
    def replace_clicked(self):
        replace_text = self.replace_input.text()
        self.replace.emit(replace_text)
        
    def replace_all_clicked(self):
        find_text = self.find_input.text()
        replace_text = self.replace_input.text()
        if find_text:
            self.replaceAll.emit(find_text, replace_text, self.whole_word.isChecked(), self.case_sensitive.isChecked())
