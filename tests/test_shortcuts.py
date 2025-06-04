def test_add_and_update_shortcut(tmp_path, qtbot):
    from shortcuts import ShortcutManager
    from PyQt5.QtWidgets import QMainWindow

    # Use a temp file for shortcuts
    shortcuts_file = tmp_path / "user_shortcuts.json"
    import shortcuts as sh
    sh.SHORTCUTS_FILE = str(shortcuts_file)

    main_window = QMainWindow()
    manager = ShortcutManager(main_window)
    called = {}

    def cb():
        called['test'] = True

    manager.add_shortcut("Test Shortcut", "Ctrl+T", cb)
    assert "Test Shortcut" in manager.shortcut_info
    assert manager.shortcut_info["Test Shortcut"]["current_sequence"] == "Ctrl+T"

    # Update shortcut
    manager.update_shortcut("Test Shortcut", "Ctrl+Shift+T")
    assert manager.shortcut_info["Test Shortcut"]["current_sequence"] == "Ctrl+Shift+T"

def test_save_and_load_shortcuts(tmp_path, qtbot):
    from shortcuts import ShortcutManager
    from PyQt5.QtWidgets import QMainWindow

    shortcuts_file = tmp_path / "user_shortcuts.json"
    import shortcuts as shortcuts_mod
    shortcuts_mod.SHORTCUTS_FILE = str(shortcuts_file)

    main_window = QMainWindow()
    manager = ShortcutManager(main_window)
    manager.add_shortcut("Test", "Ctrl+1", lambda: None)
    manager.update_shortcut("Test", "Ctrl+2")
    manager.save_shortcuts()

    # Create a new manager and load
    manager2 = ShortcutManager(main_window)
    manager2.load_shortcuts()
    assert manager2.shortcut_info["Test"]["current_sequence"] == "Ctrl+2"

def test_reset_shortcut(tmp_path, qtbot):
    from shortcuts import ShortcutManager
    from PyQt5.QtWidgets import QMainWindow

    shortcuts_file = tmp_path / "user_shortcuts.json"
    import shortcuts as shortcuts_mod
    shortcuts_mod.SHORTCUTS_FILE = str(shortcuts_file)

    main_window = QMainWindow()
    manager = ShortcutManager(main_window)
    manager.add_shortcut("ResetTest", "Ctrl+R", lambda: None)
    manager.update_shortcut("ResetTest", "Ctrl+Shift+R")
    manager.reset_shortcut("ResetTest")
    assert manager.shortcut_info["ResetTest"]["current_sequence"] == "Ctrl+R"

def test_clear_shortcuts(qtbot):
    from shortcuts import ShortcutManager
    from PyQt5.QtWidgets import QMainWindow

    main_window = QMainWindow()
    manager = ShortcutManager(main_window)
    manager.add_shortcut("A", "Ctrl+A", lambda: None)
    manager.add_shortcut("B", "Ctrl+B", lambda: None)
    manager.clear_shortcuts()
    assert manager.shortcuts == {}