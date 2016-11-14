import sys
import time
import threading
from PyQt4 import QtCore, QtGui
from model.train import start_train
from tools.check import check_model
from split.split import get_status
from split.split import split_file
from split.split import split_sentence


class MainWindow(QtGui.QMainWindow):
    """main window"""
    def __init__(self, parent=None):

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
        self.connect(self.win_widget.text_input, QtCore.SIGNAL('textChanged(QString)'), self.on_changed)

        self.setWindowIcon(QtGui.QIcon('res/icon.svg'))
        self.show()

    def on_open(self):
        file = QtGui.QFileDialog.getOpenFileName(self, 'Open')
        try:
            self.statusBar().showMessage("准备中...")
            # do thread function
            self.bwThread = DealFile(file)
            self.bwThread.finishSignal.connect(self.action_end)
            self.bwThread.statusSignal.connect(self.show_status)
            self.bwThread.start()

        except:
            self.statusBar().showMessage("Error!")

    def action_end(self, ls):
        self.win_widget.text_show.setText(ls)
        self.statusBar().showMessage("就绪")

    def show_status(self, s):
        self.statusBar().showMessage(s)

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

    def on_changed(self, text):
        if text == "":
            self.win_widget.text_show.setText("")
            self.statusBar().showMessage("就绪")
        else:
            result = split_sentence(text)
            self.statusBar().showMessage("正在分词...")
            self.win_widget.text_show.setText(result)
            self.statusBar().showMessage("完成")


class WinWidget (QtGui.QWidget) :
    """text area"""
    def __init__(self, parent):
        super(WinWidget, self).__init__(parent)
        grid_layout = QtGui.QGridLayout()
        self.text_show = QtGui.QTextEdit()
        self.text_show.setText("")

        grid_layout.addWidget(self.text_show)
        self.text_input = QtGui.QLineEdit(self)
        grid_layout.addWidget(self.text_input)

        self.setLayout(grid_layout)


class DealFile(QtCore.QThread):
    """ threading action """
    finishSignal = QtCore.pyqtSignal(str)
    statusSignal = QtCore.pyqtSignal(str)

    def __init__(self ,file ,parent=None):
        super(DealFile, self).__init__(parent)
        self.file = file
    def deal_file(self):
        try:
            split_file(self.file)
            with open("split/tmp/tmp.txt", "r") as f:
                result = f.readlines()
            self.finishSignal.emit("".join(result))
        except:
            print("Error")

    def deal_status(self):
        last_status = -1
        status = 0
        while last_status != status:
            time.sleep(0.1)
            last_status = status
            status = get_status()
            self.statusSignal.emit("已经处理" + str(status) + "行")
        print("finish")

    def run(self):
        t1 = threading.Thread(target=self.deal_file, args=())
        t2 = threading.Thread(target=self.deal_status, args=())
        t1.start()
        t2.start()


def main():

    app = QtGui.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
