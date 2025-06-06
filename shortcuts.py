from PyQt5.QtWidgets import QShortcut, QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QListWidget, QListWidgetItem, QMessageBox
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt
import json
import os

# Calea pentru salvarea scurtăturilor personalizate
SHORTCUTS_FILE = "user_shortcuts.json"

class KeyCaptureDialog(QDialog):
    """Dialog pentru capturarea scurtăturilor de tastatură"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Apasă combinația de taste")
        self.setFixedSize(300, 100)
        
        # Configurare aspect
        layout = QVBoxLayout()
        self.label = QLabel("Apasă combinația de taste dorită")
        layout.addWidget(self.label)
        
        self.key_sequence = None
        self.setLayout(layout)

    def keyPressEvent(self, event):
        """Capturează secvența de taste"""
        # Obține modificatorii
        modifiers = event.modifiers()
        key = event.key()
        
        # Ignoră tastele modificatoare individuale
        if key in (Qt.Key_Control, Qt.Key_Shift, Qt.Key_Alt, Qt.Key_Meta):
            return
            
        # Verifică dacă este o combinație validă
        is_function_key = Qt.Key_F1 <= key <= Qt.Key_F35
        has_modifier = bool(modifiers & (Qt.ControlModifier | Qt.ShiftModifier | Qt.AltModifier | Qt.MetaModifier))
        
        # Respinge taste simple (litere, cifre, simboluri) fără modificatori
        if not has_modifier and not is_function_key:
            self.label.setText("Trebuie să incluzi Ctrl, Shift sau Alt sau o tastă funcțională")
            return
            
        # Creează secvența de taste
        self.key_sequence = QKeySequence(modifiers | key).toString()
        self.label.setText(f"Capturat: {self.key_sequence}")
        
        # Acceptă dialogul după 1 secundă
        from PyQt5.QtCore import QTimer
        QTimer.singleShot(1000, self.accept)

class ShortcutConfigDialog(QDialog):
    """Dialog pentru configurarea scurtăturilor"""
    def __init__(self, shortcut_manager, parent=None):
        super().__init__(parent)
        self.shortcut_manager = shortcut_manager
        self.setWindowTitle("Scurtături tastatură")
        self.setMinimumSize(500, 400)
        
        # Layout principal
        layout = QVBoxLayout()
        
        # Lista de scurtături
        self.list_widget = QListWidget()
        self.populate_shortcut_list()
        layout.addWidget(self.list_widget)
        
        # Layout pentru butoane
        button_layout = QHBoxLayout()
        
        # Buton modificare scurtătură
        self.change_btn = QPushButton("Modifică scurtătura")
        self.change_btn.clicked.connect(self.change_shortcut)
        button_layout.addWidget(self.change_btn)
        
        # Buton resetare la implicit
        self.reset_btn = QPushButton("Resetează")
        self.reset_btn.clicked.connect(self.reset_shortcut)
        button_layout.addWidget(self.reset_btn)
        
        # Buton resetare toate
        self.reset_all_btn = QPushButton("Resetează toate")
        self.reset_all_btn.clicked.connect(self.reset_all_shortcuts)
        button_layout.addWidget(self.reset_all_btn)
        
        # Buton închidere
        self.close_btn = QPushButton("Închide")
        self.close_btn.clicked.connect(self.close)
        button_layout.addWidget(self.close_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
        self.setStyleSheet("""
            QDialog {
                background-color: #344955 ;
                color: #f8f8f2;
                font-size: 14px;
            }
            QListWidget {
                background: #282c34;
                color: #f8f8f2;
                border: 1px solid #44475a;
            }
            QPushButton {
                background-color: #282c34;
                color: #f8f8f2;
                border-radius: 5px;
                padding: 6px 12px;
                margin: 4px;
            }
            QPushButton:hover {
                background-color: #6272a4;
            }
            QLabel {
                color: #f8f8f2;
            }
        """)
        
    def populate_shortcut_list(self):
        """Populează lista cu scurtăturile curente"""
        self.list_widget.clear()
        
        for name, info in self.shortcut_manager.shortcut_info.items():
            key_seq = info['current_sequence']
            item = QListWidgetItem(f"{name}: {key_seq}")
            item.setData(Qt.UserRole, name)  # Stochează numele scurtăturii
            self.list_widget.addItem(item)
    
    def change_shortcut(self):
        """Modifică secvența de taste a scurtăturii selectate"""
        current_item = self.list_widget.currentItem()
        if not current_item:
            QMessageBox.information(self, "Selectare scurtătură", "Te rog selectează o scurtătură")
            return
        
        shortcut_name = current_item.data(Qt.UserRole)
        
        # Deschide dialogul de captură taste
        key_dialog = KeyCaptureDialog(self)
        if key_dialog.exec_():
            new_sequence = key_dialog.key_sequence
            if new_sequence:
                # Verifică duplicatele
                for name, info in self.shortcut_manager.shortcut_info.items():
                    if info['current_sequence'] == new_sequence and name != shortcut_name:
                        QMessageBox.warning(
                            self, 
                            "Scurtătură duplicat", 
                            f"Această combinație este deja folosită pentru '{name}'")
                        return
                
                # Actualizează scurtătura
                self.shortcut_manager.update_shortcut(shortcut_name, new_sequence)
                self.populate_shortcut_list()
                
    def reset_shortcut(self):
        """Resetează scurtătura la secvența implicită"""
        current_item = self.list_widget.currentItem()
        if not current_item:
            QMessageBox.information(self, "Selectare scurtătură", "Te rog selectează o scurtătură")
            return
        
        shortcut_name = current_item.data(Qt.UserRole)
        self.shortcut_manager.reset_shortcut(shortcut_name)
        self.populate_shortcut_list()
    
    def reset_all_shortcuts(self):
        """Resetează toate scurtăturile la valorile implicite"""
        reply = QMessageBox.question(self, 
                                     "Confirmare resetare", 
                                     "Sigur dorești să resetezi toate scurtăturile la valorile implicite?",
                                     QMessageBox.Yes | QMessageBox.No, 
                                     QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.shortcut_manager.reset_all_shortcuts()
            self.populate_shortcut_list()
            QMessageBox.information(self, "Resetare completă", "Toate scurtăturile au fost resetate la valorile implicite")

class ShortcutManager:
    """Manager pentru scurtăturile de tastatură"""

    def __init__(self, main_window):
        """Inițializează managerul de scurtături"""
        self.main_window = main_window
        self.shortcuts = {}  # Mapează numele la obiectul QShortcut
        self.shortcut_info = {}  # Stochează info despre scurtături
        
        # Încarcă scurtăturile salvate
        self.load_shortcuts()
    
    def add_shortcut(self, name, default_sequence, callback):
        """Adaugă o nouă scurtătură"""
        # Verifică dacă scurtătura există deja
        if name in self.shortcut_info:
            key_sequence = self.shortcut_info[name].get('current_sequence', default_sequence)
            # Actualizează callback-ul
            self.shortcut_info[name]['callback'] = callback
            self.shortcut_info[name]['default_sequence'] = default_sequence
        else:
            # Folosește valorile implicite
            key_sequence = default_sequence
            self.shortcut_info[name] = {
                'default_sequence': default_sequence,
                'current_sequence': default_sequence,
                'callback': callback
            }
        
        # Creează scurtătura
        if name in self.shortcuts:
            # Elimină scurtătura veche
            self.shortcuts[name].setEnabled(False)
            
        # Creează scurtătură nouă
        shortcut = QShortcut(QKeySequence(key_sequence), self.main_window)
        shortcut.activated.connect(callback)
        self.shortcuts[name] = shortcut
        
        # Salvează scurtăturile
        self.save_shortcuts()
        
    def update_shortcut(self, name, new_sequence):
        """Actualizează secvența de taste a scurtăturii"""
        if name in self.shortcut_info:
            # Verifică existența callback-ului
            if 'callback' not in self.shortcut_info[name]:
                print(f"Atenție: Lipsă callback pentru '{name}'")
                return
                
            # Șterge scurtătura veche
            if name in self.shortcuts:
                self.shortcuts[name].setEnabled(False)
            
            # Creează scurtătura nouă
            shortcut = QShortcut(QKeySequence(new_sequence), self.main_window)
            shortcut.activated.connect(self.shortcut_info[name]['callback'])
            
            # Actualizează datele
            self.shortcuts[name] = shortcut
            self.shortcut_info[name]['current_sequence'] = new_sequence
            
            # Salvează modificările
            self.save_shortcuts()
            
    def reset_shortcut(self, name):
        """Resetează scurtătura la valorile implicite"""
        if name in self.shortcut_info and 'default_sequence' in self.shortcut_info[name]:
            default_seq = self.shortcut_info[name]['default_sequence']
            self.update_shortcut(name, default_seq)
    
    def reset_all_shortcuts(self):
        """Resetează toate scurtăturile la valorile implicite"""
        for name in self.shortcut_info:
            if 'default_sequence' in self.shortcut_info[name]:
                default_seq = self.shortcut_info[name]['default_sequence']
                self.update_shortcut(name, default_seq)
    
    def clear_shortcuts(self):
        """Elimină toate scurtăturile"""
        for shortcut in self.shortcuts.values():
            shortcut.setEnabled(False)
        self.shortcuts.clear()
    
    def save_shortcuts(self):
        """Salvează scurtăturile personalizate"""
        save_data = {}
        for name, info in self.shortcut_info.items():
            save_data[name] = {
                'current_sequence': info['current_sequence']
            }
        
        try:
            with open(SHORTCUTS_FILE, 'w') as f:
                json.dump(save_data, f)
        except Exception as e:
            print(f"Eroare la salvare: {e}")
            
    def load_shortcuts(self):
        """Încarcă scurtăturile salvate"""
        if not os.path.exists(SHORTCUTS_FILE):
            return
            
        try:
            with open(SHORTCUTS_FILE, 'r') as f:
                save_data = json.load(f)
                
            # Stochează datele încărcate
            for name, data in save_data.items():
                if name not in self.shortcut_info:
                    self.shortcut_info[name] = {}
                # Actualizează doar secvența curentă
                if 'current_sequence' in data:
                    self.shortcut_info[name]['current_sequence'] = data['current_sequence']
                    
        except Exception as e:
            print(f"Eroare la încărcare: {e}")
    
    def show_config_dialog(self):
        """Afișează dialogul de configurare"""
        dialog = ShortcutConfigDialog(self, self.main_window)
        dialog.exec_()