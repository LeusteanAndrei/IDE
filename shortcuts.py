from PyQt5.QtWidgets import QShortcut
from PyQt5.QtGui import QKeySequence

class ShortcutManager:
    """
    A class to manage keyboard shortcuts for the application.
    """

    def __init__(self, main_window):
        """
        Initialize the ShortcutManager.
        main_window: The main window of the application.
        """
        self.main_window = main_window
        self.shortcuts = []

    def add_shortcut(self, key_sequence, callback):
        """
        Adds a new shortcut.
        Args:
            key_sequence: The key sequence for the shortcut (e.g., "Ctrl+S").
            callback: The function to call when the shortcut is activated.
        """
        shortcut = QShortcut(QKeySequence(key_sequence), self.main_window)
        shortcut.activated.connect(callback)
        self.shortcuts.append(shortcut)

    def clear_shortcuts(self):
        """
        We might actually add something like shortcut_replace in order to dinamically change the bindings
        da mai e pana atunci lmao mi s a luat sa pun comentarii in engleza +100 aura pt cine vede mesaju asta.
        """
        self.shortcuts.clear()