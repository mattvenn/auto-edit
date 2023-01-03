#!/usr/bin/env python3
import sys, json
import time
import glob
from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QShortcut, QLineEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QKeySequence

obs_videos = '/home/matt/Videos/obs/*mkv'
obs_videos = '/media/matt/Seagate Expansion Drive/obs/*mov'

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(self.__class__, self).__init__()

        self.cuts = []
        self.videos = glob.glob(obs_videos) 
        print(f'found {len(self.videos)} videos in {obs_videos}')
        self.start_time = None

        shortcut_start = QShortcut(QKeySequence('S'), self) 
        self.button1 = QPushButton(self)
        self.button1.setText("Start")
        self.button1.move(64,32)
        self.button1.clicked.connect(self.button1_clicked)
        shortcut_start.activated.connect(self.button1_clicked)
        self.button1.setDisabled(True)

        shortcut_end = QShortcut(QKeySequence('E'), self) 
        self.button2 = QPushButton(self)
        self.button2.setText("End")
        self.button2.move(64,64)
        self.button2.clicked.connect(self.button2_clicked)
        shortcut_end.activated.connect(self.button2_clicked)
        self.button2.setDisabled(True)

        self.input_file = QLineEdit(self)
        self.input_file.move(64,96)
        self.input_file.setDisabled(True)
        self.output_file = QLineEdit(self)
        self.output_file.move(64,128)
        self.output_file.setText("output_name")

        shortcut_quit = QShortcut(QKeySequence('Q'), self) 
        shortcut_quit.activated.connect(self.finish)

        # file watcher
        self.file_timer = QtCore.QTimer(self)
        self.file_timer.start(100) 
        self.file_timer.timeout.connect(self.update_files)

        self.setGeometry(50,50,320,200)
        self.setWindowTitle("PyQt5 Button Click Example")
        self.show()

    def update_files(self):
        videos = glob.glob(obs_videos) 
        new_videos = [x for x in videos if x not in self.videos]
        if new_videos:
            print(f"new video detected {new_videos}")
            self.video_file = new_videos[0]
            self.input_file.setText(self.video_file)
            self.start_time = time.time()
            self.button1.setDisabled(False)

        self.videos = videos
   
    def closeEvent(self, event):
        self.finish()

    def finish(self):
        print("quit")
        with open("cuts.json", "w") as fh:
            fh.write(json.dumps(
                {
                    'input_file': self.video_file,
                    'output_file': self.output_file.text(),
                    'cuts': self.cuts,
                }, indent=4))
        app.quit()

    def button1_clicked(self):
        cut = {'type': 'start', 'timestamp': time.time() - self.start_time}
        self.button2.setDisabled(False)
        print(cut)
        self.cuts.append(cut)
        
    def button2_clicked(self):
        cut = {'type': 'end', 'timestamp': time.time() - self.start_time}
        print(cut)
        self.cuts.append(cut)
        self.button2.setDisabled(True)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
