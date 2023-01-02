import sys, json
import time
from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QShortcut
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QKeySequence

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(self.__class__, self).__init__()

        self.cuts = []
        self.start_time = None

        shortcut_start = QShortcut(QKeySequence('S'), self) 
        button1 = QPushButton(self)
        button1.setText("Start")
        button1.move(64,32)
        button1.clicked.connect(self.button1_clicked)
        shortcut_start.activated.connect(self.button1_clicked)

        shortcut_end = QShortcut(QKeySequence('E'), self) 
        button2 = QPushButton(self)
        button2.setText("End")
        button2.move(64,64)
        button2.clicked.connect(self.button2_clicked)
        shortcut_end.activated.connect(self.button2_clicked)

        shortcut_quit = QShortcut(QKeySequence('Q'), self) 
        shortcut_quit.activated.connect(self.finish)

        self.setGeometry(50,50,320,200)
        self.setWindowTitle("PyQt5 Button Click Example")
        self.show()

    def finish(self):
        print("quit")
        with open("cuts.json", "w") as fh:
            fh.write(json.dumps(self.cuts, indent=4))
        app.quit()

    def button1_clicked(self):
        if self.start_time is None:
            self.start_time = time.time()
        cut = {'type': 'start', 'timestamp': "{:.2f}".format(time.time() - self.start_time)}
        print(cut)
        self.cuts.append(cut)
        
    def button2_clicked(self):
        if self.start_time is None:
            return
        cut = {'type': 'end', 'timestamp': "{:.2f}".format(time.time() - self.start_time)}
        print(cut)
        self.cuts.append(cut)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
