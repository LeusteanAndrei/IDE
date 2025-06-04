import os
import tempfile
import pytest

#that monkeypatch stuff is used to simulate user interactions - pretty cool ngl

def test_save_as_file_writes_content(monkeypatch):
    from FileSystem import file_methods

    class DummyEditor:
        def toPlainText(self):
            return "test content"

    # Patch QFileDialog.getSaveFileName to return a temp file path
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.close()
    monkeypatch.setattr(
        file_methods.QFileDialog, "getSaveFileName",
        lambda *a, **k: (temp_file.name, "txt")
    )
    # Patch QMessageBox to do nothing
    monkeypatch.setattr(file_methods.QMessageBox, "critical", lambda *a, **k: None)

    _ , saved = file_methods.save_as_file(DummyEditor(), "")
    assert saved is True
    with open(temp_file.name) as f:
        assert f.read() == "test content"
    os.remove(temp_file.name)

def test_save_file_existing(monkeypatch):
    from FileSystem import file_methods

    class DummyEditor:
        def toPlainText(self):
            return "abc123"

    class DummyHighlighter:
        def rehighlight(self):
            self.called = True

    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.write(b"old")
    temp_file.close()

    highlighter = DummyHighlighter()
    monkeypatch.setattr(file_methods.QMessageBox, "critical", lambda *a, **k: None)

    path, saved = file_methods.save_file(DummyEditor(), temp_file.name, False, highlighter)
    assert saved is True
    with open(temp_file.name) as f:
        assert f.read() == "abc123"
    os.remove(temp_file.name)

def test_new_file_valid_name(monkeypatch):
    from FileSystem import file_methods

    # Patch QInputDialog.getText to simulate user entering a valid name
    monkeypatch.setattr(
        file_methods.QInputDialog, "getText",
        lambda *a, **k: ("myfile.txt", True)
    )
    monkeypatch.setattr(file_methods.QMessageBox, "warning", lambda *a, **k: None)
    result = file_methods.new_file(None)
    assert result == "myfile.txt"

def test_new_file_cancel(monkeypatch):
    from FileSystem import file_methods

    # Patch QInputDialog.getText to simulate user pressing cancel
    monkeypatch.setattr(
        file_methods.QInputDialog, "getText",
        lambda *a, **k: ("", False)
    )
    result = file_methods.new_file(None)
    assert result is None