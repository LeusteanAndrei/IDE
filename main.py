from window import *
import sys
from Highlighter.highlighter import cPlusPlusHighlighter


if __name__ == "__main__":

    f = open("testingCode.cpp", "r")
    testText = f.readlines()
    test = "".join(testText)

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    editor = ui.plainTextEdit
    editor.setPlainText(test)

    editor.setStyleSheet("background-color: lightgray;")
    font = editor.font()
    font.setPointSize(20)
    editor.setFont(font)    
    highlighter = cPlusPlusHighlighter(editor.document())
    editor.show()
    sys.exit(app.exec_())
