def test_add_and_update_shortcut(tmp_path, qtbot):

    from shortcuts import ShortcutManager
    from PyQt5.QtWidgets import QMainWindow

    # Use a temp file for shortcuts
    shortcuts_file = tmp_path / "user_shortcuts.json"
    import shortcuts as sh
    sh.SHORTCUTS_FILE = str(shortcuts_file)

    print("\n   ----Created temporary shortcut file----")

    from PyQt5.QtWidgets import QApplication


    import sys

    if not QApplication.instance():
        print("   ----Creating application instance----")
        app = QApplication(sys.argv)
    else:
        print("   ----Using existing application instance----")
        app = QApplication.instance()

    print("   ----Got application instance----")

    main_window = QMainWindow()
    manager = ShortcutManager(main_window)
    
    print("   ----Created ShortcutManager instance----")

    called = {}
    def cb():
        called['test'] = True

    manager.add_shortcut("Test Shortcut", "Ctrl+T", cb)
    print("   ----Added Test Shortcut----")
    assert "Test Shortcut" in manager.shortcut_info
    assert manager.shortcut_info["Test Shortcut"]["current_sequence"] == "Ctrl+T"
    print("   ----Test Shortcut added successfully----")
    # Update shortcut
    manager.update_shortcut("Test Shortcut", "Ctrl+Shift+T")
    print("   ----Updated Test Shortcut to Ctrl+Shift+T----")
    assert manager.shortcut_info["Test Shortcut"]["current_sequence"] == "Ctrl+Shift+T"
    print("   ----Test Shortcut updated successfully----")


def test_save_and_load_shortcuts(tmp_path, qtbot):
    from shortcuts import ShortcutManager
    from PyQt5.QtWidgets import QMainWindow

    shortcuts_file = tmp_path / "user_shortcuts.json"
    import shortcuts as shortcuts_mod
    shortcuts_mod.SHORTCUTS_FILE = str(shortcuts_file)
    print("\n   ----Created temporary shortcut file----")

    from PyQt5.QtWidgets import QApplication
    import sys

    if not QApplication.instance():
        print("   ----Creating application instance----")
        app = QApplication(sys.argv)
    else:
        print("   ----Using existing application instance----")
        app = QApplication.instance()
    print("   ----Got application instance----")

    main_window = QMainWindow()
    manager = ShortcutManager(main_window)
    print("   ----Created ShortcutManager instance----")
    manager.add_shortcut("Test", "Ctrl+1", lambda: None)
    manager.update_shortcut("Test", "Ctrl+2")
    manager.save_shortcuts()
    print("   ----Saved shortcuts to file----")

    # Create a new manager and load
    manager2 = ShortcutManager(main_window)
    print("   ----Created new ShortcutManager instance----")
    manager2.load_shortcuts()
    print("   ----Loaded shortcuts from file----")
    assert manager2.shortcut_info["Test"]["current_sequence"] == "Ctrl+2"
    print("   ----Test shortcut loaded successfully----")

def test_reset_shortcut(tmp_path, qtbot):
    from shortcuts import ShortcutManager
    from PyQt5.QtWidgets import QMainWindow

    shortcuts_file = tmp_path / "user_shortcuts.json"
    import shortcuts as shortcuts_mod
    shortcuts_mod.SHORTCUTS_FILE = str(shortcuts_file)
    print("\n   ----Created temporary shortcut file----")

    from PyQt5.QtWidgets import QApplication
    import sys
    if not QApplication.instance():
        print("   ----Creating application instance----")
        app = QApplication(sys.argv)
    else:
        print("   ----Using existing application instance----")
        app = QApplication.instance()
    print("   ----Got application instance----")

    main_window = QMainWindow()
    manager = ShortcutManager(main_window)
    print("   ----Created ShortcutManager instance----")

    manager.add_shortcut("ResetTest", "Ctrl+R", lambda: None)
    manager.update_shortcut("ResetTest", "Ctrl+Shift+R")
    print("   ----Added and updated ResetTest shortcut----")
    manager.reset_shortcut("ResetTest")
    print("   ----Reset ResetTest shortcut----")
    assert manager.shortcut_info["ResetTest"]["current_sequence"] == "Ctrl+R"
    print("   ----Shortcut resetted succesfully----")

def test_clear_shortcuts(qtbot):
    from shortcuts import ShortcutManager
    from PyQt5.QtWidgets import QMainWindow

    from PyQt5.QtWidgets import QApplication
    import sys
    print()
    if not QApplication.instance():
        print("   ----Creating application instance----")
        app = QApplication(sys.argv)
    else:
        print("   ----Using existing application instance----")
        app = QApplication.instance()
    print("   ----Got application instance----")


    main_window = QMainWindow()
    manager = ShortcutManager(main_window)
    print("   ----Created ShortcutManager instance----")

    manager.add_shortcut("A", "Ctrl+A", lambda: None)
    manager.add_shortcut("B", "Ctrl+B", lambda: None)
    print("   ----Added shortcuts A and B----")
    
    manager.clear_shortcuts()
    print("   ----Cleared all shortcuts----")
    assert manager.shortcuts == {}
    print("   ----Shortcuts cleared successfully----")