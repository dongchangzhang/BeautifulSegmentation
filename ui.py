import sys
import multiprocessing
from PyQt4 import QtCore, QtGui
from model.train import start_train
from tools.check import check_model
from split.split import split_file
from split.split import split_sentence




class MainWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):

        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("中文分词")
        self.resize(800, 500)
        # widget input...
        self.win_widget = WinWidget(self)
        widget = QtGui.QWidget()
        layout = QtGui.QVBoxLayout(widget)
        layout.addWidget(self.win_widget)

        self.setCentralWidget(widget)
        # status bar
        self.statusBar().showMessage('Ready')
        # toolbar
        self.toolbar = self.addToolBar('Exit')
        # menu bar
        menu_bar = self.menuBar()
        self.file = menu_bar.addMenu('&File')
        open = self.file.addAction('Open')
        self.connect(open, QtCore.SIGNAL('triggered()'), self.on_open)

        save = self.file.addAction('Save')
        self.connect(save, QtCore.SIGNAL('triggered()'), self.on_save)
        self.file.addSeparator()
        close = self.file.addAction("Close")
        self.connect(close, QtCore.SIGNAL('triggered()'), self.on_close)

        # check = self.win_widget.text_input.addAction('Check')
        # self.connect(check, QtCore.SIGNAL('triggered()'), self.OnClose)
        # check = self.win_widget.text_input.addAction("Check")
        # self.connect(check, QtCore.SIGNAL('triggered()'), self.hah)

        # self.connect( self.win_widget.text_input, QtCore.SIGNAL('valueChanged'), QtCore.SLOT('self.hah()'))
        # self.win_widget.text_input.textChanged()

        # self.toolbar = self.addToolBar('Exit')
        # self.toolbar.addAction(exitAction)
        # self.key = self.keyboardGrabber()
        # self.key.customEvent()

        self.connect(self.win_widget.text_input, QtCore.SIGNAL('textChanged(QString)'),
                     self.onChanged)

        self.setWindowIcon (QtGui.QIcon('logo.png'))
        self.show()

    def on_open(self):
        file = QtGui.QFileDialog.getOpenFileName(self, 'Open')
        try:
            with open(file, "r") as f:
                result = ""
                self.setWindowTitle(file)
                self.statusBar().showMessage("Working!")
                for line in f:
                    result += split_sentence(line) + "\n"
                self.win_widget.text_show.setText(result)
                self.statusBar().showMessage("Finished!")

        except:
            self.statusBar().showMessage("can not open!")

    def on_save(self):
        self.show_result()
        # self.label.setText("save")

    def on_close(self):
        self.close()

    def contextMenuEvent(self, event):
        self.file.exec_(event.globalPos())

    def show_result(self):
        result = split_sentence(self.win_widget.text_input.toPlainText())
        self.win_widget.text_show.setText(result)
        self.statusBar().showMessage(self.win_widget.text_input.toPlainText())

    def onChanged(self, text):
        if text == "":
            self.win_widget.text_show.setText("")
            self.statusBar().showMessage("NONE")
        else:
            result = split_sentence(text)
            self.win_widget.text_show.setText(result)
            self.statusBar().showMessage(text)


class WinWidget (QtGui.QWidget) :

    def __init__(self, parent):
        super(WinWidget, self).__init__(parent)
        grid_layout = QtGui.QGridLayout()
        self.text_show = QtGui.QTextEdit()
        self.text_show.setText("show")

        grid_layout.addWidget(self.text_show)
        self.text_input = QtGui.QLineEdit(self)
        grid_layout.addWidget(self.text_input)

        self.setLayout(grid_layout)


def main():

    app = QtGui.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
