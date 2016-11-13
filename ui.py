import sys
import time
from PyQt4 import QtCore, QtGui
from model.train import start_train
from tools.check import check_model
from split.split import split_file
from split.split import split_sentence


class MainWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):
        # file line numbers
        self.pbar = None
        self.lines = 0
        # init
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
        self.statusBar().showMessage("就绪")
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
        # when text changed do action
        self.connect(self.win_widget.text_input, QtCore.SIGNAL('textChanged(QString)'), self.onChanged)

        self.setWindowIcon(QtGui.QIcon('logo.png'))
        self.show()

    def on_open(self):
        file = QtGui.QFileDialog.getOpenFileName(self, 'Open')
        try:
            # add progress bar
            self.pbar = QtGui.QProgressBar(self)
            self.statusBar().clearMessage()
            self.statusBar().addWidget(self.pbar)
            self.pbar.setMinimum(0)
            self.pbar.setMaximum(100)
            self.lines = self.getlines(file)
            # do thread function
            self.bwThread = Work(file)
            # 连接子进程的信号和槽函数
            self.bwThread.finishSignal.connect(self.BigWorkEnd)
            self.bwThread.status_signal.connect(self.status_bar)
            # 开始执行 run() 函数里的内容
            self.bwThread.start()

        except:
            self.statusBar().showMessage("Error!")

    def BigWorkEnd(self, ls):
        self.win_widget.text_show.setText(ls)
        self.statusBar().removeWidget(self.pbar)
        self.statusBar().showMessage("就绪")
    def status_bar(self, times):

        self.pbar.setValue(100 * float(times) / self.lines)
        # self.statusBar().showMessage(str(100 * float(times) / self.lines) + "%")


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
    def getlines(self, file):
        with open(file, "r") as f:
            l = list(f)
        return len(l)
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


class Work(QtCore.QThread):

    finishSignal = QtCore.pyqtSignal(str)
    status_signal = QtCore.pyqtSignal(str)

    def __init__(self ,file ,parent=None):
        super(Work, self).__init__(parent)
        #储存参数
        self.file = file

    def run(self):
        print("here")
        try:
            with open(self.file, "r") as f:
                result = ""
                i = 0
                for line in f:
                    result += split_sentence(line) + "\n"
                    i += 1
                    self.status_signal.emit(str(i))
            self.finishSignal.emit(result)
        except:
            print("Error")

def main():

    app = QtGui.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
