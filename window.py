from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):

        screenSize = QtWidgets.QDesktopWidget().screenGeometry()
        screenWidth = screenSize.width()
        screenHeight = screenSize.height()

        MainWindow.showMaximized()

        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        # MainWindow.resize(screenWidth, screenHeight)
        # MainWindow.resize(1105, 632)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setGeometry(QtCore.QRect(50, 0, screenWidth - 100, screenHeight - 100))
        # self.plainTextEdit.setGeometry(QtCore.QRect(50, 0, 1051, 571))
        self.plainTextEdit.setObjectName("plainTextEdit")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1105, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))


# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     MainWindow = QtWidgets.QMainWindow()
#     ui = Ui_MainWindow()
#     ui.setupUi(MainWindow)
#     MainWindow.show()
#     editor = ui.plainTextEdit

#     from Highlighter.highlighter import cPlusPlusHighlighter


#     # editor.setPlainText(" ".join(cPlusPlusHighlighter.operators) + "\n" +
#     #                     " ".join(cPlusPlusHighlighter.braces) + "\n" +
#     #                     " ".join(cPlusPlusHighlighter.keywords) + "\n"
#     #                     +"this" + "\n" +
#     #                     "class nume_clasa" + "\n" 
#     #                     +"0x123456789ABCDEF" + "\n" +
#     #                     "0b1010101010101" + "\n" +
#     #                     "167.386516358618" + "\n" +
#     #                     "167.386516358618e+12" + "\n" +
#     #                     "167.386516358618e-12" + "\n" +
#     #                     "+123123132434525"+ "\n" +
#     #                     "-123123132434525"+ "\n" 
#     #                     +"\\\\ifwa7f9a7f bfq i34fi1bq346fg 91374tiawdjawwgyfgq" + "\n" +
#     #                     "\"string\""+ "\n" +
#     #                     "'char'" + "\n"     
#     #                     )
#     editor.setStyleSheet("background-color: lightgray;")
#     font = editor.font()
#     font.setPointSize(20)  # Set the desired font size
#     editor.setFont(font)    
#     highlighter = cPlusPlusHighlighter(editor.document())
#     editor.show()
#     sys.exit(app.exec_())
