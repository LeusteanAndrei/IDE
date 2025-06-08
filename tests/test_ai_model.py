def test_ai_model_read_file(tmp_path):
    from ai_model import AiModel
    # Create a temporary file
    file_path = tmp_path / "test.txt"
    print("\n   ----Created temporary file for testing AiModel.read_file----")
    file_path.write_text("hello world")
    ai = AiModel(api_key="dummy")
    print("   ----Created AiModel instance----")
    content = ai.read_file(str(file_path))
    print("   ----Called AiModel.read_file----")
    assert content == "hello world"
    print("   ----Verified file content matches expected----")

def test_extract_code_blocks():
    assert True  # Placeholder for actual test logic

def test_add_text_appends_to_chat_area(qtbot):
    from ai_model import ChatWidget
    class DummyUI:
        class DummyPlainTextEdit:
            text_edit = None
        plainTextEdit = DummyPlainTextEdit()

    print()
    from PyQt5.QtWidgets import QApplication
    if not QApplication.instance():
        print("   ----Creating application instance----")
        app = QApplication([])
    else:
        print("   ----Using existing application instance----")
        app = QApplication.instance()
    print("   ----Got application instance----")

    widget = ChatWidget(DummyUI())
    widget.chat_area.clear()
    widget.add_text("Hello AI")
    print("\n   ----Created ChatWidget instance for testing add_text----")

    assert "Hello AI" in widget.chat_area.toPlainText()
    print("   ----Verified text was added to chat area----")

def test_insert_code_inserts_text(qtbot):
    from ai_model import ChatWidget
    from PyQt5.QtWidgets import QTextEdit
    class DummyTextEdit(QTextEdit):
        def __init__(self):
            super().__init__()
    class DummyUI:
        class DummyPlainTextEdit:
            def __init__(self):
                self.text_edit = DummyTextEdit()
        def __init__(self):
            self.plainTextEdit = self.DummyPlainTextEdit()
    from PyQt5.QtWidgets import QApplication
    print()
    if not QApplication.instance():
        print("   ----Creating application instance----")
        app = QApplication([])
    else:
        print("   ----Using existing application instance----")
        app = QApplication.instance()
    print("   ----Got application instance----")

    ui = DummyUI()
    widget = ChatWidget(ui)
    widget.insert_code("int x = 42;")
    print("   ----Created ChatWidget instance for testing insert_code----")

    assert "int x = 42;" in ui.plainTextEdit.text_edit.toPlainText()
    print("   ----Verified code was inserted into text edit----")