import os
import tempfile
import pytest

#that monkeypatch stuff is used to simulate user interactions - pretty cool ngl

def test_save_as_file_writes_content(monkeypatch):
    print()
    from FileSystem import file_methods

    class DummyEditor:
        def toPlainText(self):
            return "test content"

    # Patch QFileDialog.getSaveFileName to return a temp file path
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    print("   ----Created temporary file for testing save_as_file----")
    temp_file.close()
    monkeypatch.setattr(
        file_methods.QFileDialog, "getSaveFileName",
        lambda *a, **k: (temp_file.name, "txt")
    )
    print("   ----Patched QFileDialog to return temporary file path----")
    # Patch QMessageBox to do nothing
    monkeypatch.setattr(file_methods.QMessageBox, "critical", lambda *a, **k: None)
    print("   ----Patched QMessageBox to avoid user interaction----")

    _ , saved = file_methods.save_as_file(DummyEditor(), "")
    print("   ----Called save_as_file with DummyEditor----")
    assert saved is True
    print("   ----File saved successfully----")
    with open(temp_file.name) as f:
        assert f.read() == "test content"
        print("   ----Verified file content matches expected----")
    os.remove(temp_file.name)
    print("   ----Removed temporary file----")

def test_save_file_existing(monkeypatch):
    print()
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
    print("   ----Created temporary file for testing save_file_existing----")

    highlighter = DummyHighlighter()
    monkeypatch.setattr(file_methods.QMessageBox, "critical", lambda *a, **k: None)
    print("   ----Patched QMessageBox to avoid user interaction----")

    path, saved = file_methods.save_file(DummyEditor(), temp_file.name, False, highlighter)
    print("   ----Called save_file with DummyEditor and existing file----")
    assert saved is True
    print("   ----File saved successfully----")
    with open(temp_file.name) as f:
        assert f.read() == "abc123"
        print("   ----Verified file content matches expected----")
    os.remove(temp_file.name)
    print("   ----Removed temporary file----")

def test_new_file_valid_name(monkeypatch):
    print()
    from FileSystem import file_methods

    # Patch QInputDialog.getText to simulate user entering a valid name
    monkeypatch.setattr(
        file_methods.QInputDialog, "getText",
        lambda *a, **k: ("myfile.txt", True)
    )
    print("   ----Patched QInputDialog to simulate valid file name input----")
    monkeypatch.setattr(file_methods.QMessageBox, "warning", lambda *a, **k: None)
    print("   ----Patched QMessageBox to avoid user interaction----")
    result = file_methods.new_file(None)
    print("   ----Called new_file with simulated valid name----")
    assert result == "myfile.txt"
    print("   ----New file created with name 'myfile.txt'----")

def test_new_file_cancel(monkeypatch):
    print()
    from FileSystem import file_methods

    # Patch QInputDialog.getText to simulate user pressing cancel
    monkeypatch.setattr(
        file_methods.QInputDialog, "getText",
        lambda *a, **k: ("", False)
    )
    print("   ----Patched QInputDialog to simulate cancel action----")
    result = file_methods.new_file(None)
    print("   ----Called new_file with simulated cancel action----")
    assert result is None
    print("   ----New file creation cancelled----")