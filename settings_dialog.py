from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QSpinBox, QPushButton, QColorDialog, QHBoxLayout
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QFontComboBox
from themes import THEMES
from Styles.style import SETTINGS_STYLE, FONT_DROPDOWN_STYLE
from Highlighter.theme import HighlighterThemeFactory

# class SettingsDialog(QDialog):
#     def __init__(self, parent=None, editor=None):
#         super().__init__(parent)

#         # self.setStyleSheet(SETTINGS_DIALOG_STYLE)

class SettingsDialog(QDialog):
    def __init__(self, parent=None, editor=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.editor = editor

        layout = QVBoxLayout()

        # Theme selection
        theme_layout = QHBoxLayout()
        theme_layout.addWidget(QLabel("Theme:"))
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(HighlighterThemeFactory.get_available_themes())
        self.theme_combo.setStyleSheet(FONT_DROPDOWN_STYLE)
        theme_layout.addWidget(self.theme_combo)
        layout.addLayout(theme_layout)

        # Font size setting
        font_layout = QHBoxLayout()
        font_layout.addWidget(QLabel("Font size:"))
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(8, 48)
        if editor:
            self.font_size_spin.setValue(editor.text_edit.font().pointSize())
        font_layout.addWidget(self.font_size_spin)
        layout.addLayout(font_layout)
        

        # Font color setting
        font_color_btn = QPushButton("Choose Font Color")
        font_color_btn.clicked.connect(self.choose_font_color)
        layout.addWidget(font_color_btn)

        # Font family selection
        font_family_layout = QHBoxLayout()
        font_family_layout.addWidget(QLabel("Font family:"))
        self.font_combo = QFontComboBox()
        self.font_combo.setStyleSheet(FONT_DROPDOWN_STYLE)
        if editor:
            # current_font = editor.text_edit.font().family()
            self.font_combo.setCurrentFont(editor.text_edit.font())
        font_family_layout.addWidget(self.font_combo)
        layout.addLayout(font_family_layout)
        
        # Theme color setting (background)
        theme_btn = QPushButton("Choose Editor Background Color")
        theme_btn.clicked.connect(self.choose_bg_color)
        layout.addWidget(theme_btn)




        # Save button
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.apply_settings)
        layout.addWidget(save_btn)

        self.setLayout(layout)
        self.setStyleSheet(SETTINGS_STYLE)

        self.bgcolour = editor.text_edit.background_color
        self.font_colour = None  

    def choose_bg_color(self):
        color = QColorDialog.getColor()
        if color.isValid() and self.editor:
            # self.editor.text_edit.setStyleSheet(f"background-color: {color.name()};")
            self.bgcolour = color.name()

    def choose_font_color(self):
        color = QColorDialog.getColor()
        if color.isValid() and self.editor:
            self.font_colour = color.name()
            
    def apply_settings(self):
        if self.editor:
            # font = self.editor.text_edit.font()
            # font.setPointSize(self.font_size_spin.value())
            # font.setFamily(self.font_combo.currentFont().family())
            # self.editor.text_edit.setFont(font)
            # # Apply background color if chosen
            # if hasattr(self, '_chosen_bg_color'):
            #     self.editor.text_edit.setStyleSheet(f"background-color: {self._chosen_bg_color};")
            self.editor.text_edit.font_size = self.font_size_spin.value()
            self.editor.text_edit.font_family = self.font_combo.currentFont().family()
            self.editor.text_edit.background_color = self.bgcolour
            self.editor.text_edit.font_color = self.font_colour 

            # Apply the selected theme
            from Highlighter.theme import ThemeManager
            theme_manager = ThemeManager(self.editor.highlighter)
            theme_manager.set_theme(self.theme_combo.currentText())

            self.editor.highlighter.rehighlight()
            self.editor.text_edit.apply_style()
            self.editor.text_edit.update()  # Refresh the editor to apply changes      
        self.accept()
        
    # #NU MERGE INCA --- e mai complicat sa dai import la teme deja facute :(
    # def choose_theme(self):
    #     # Theme selection dropdown
    #     self.theme_combo = QComboBox()
    #     self.theme_combo.addItems(THEMES.keys())
    #     layout.addWidget(QLabel("Theme:"))
    #     layout.addWidget(self.theme_combo)

