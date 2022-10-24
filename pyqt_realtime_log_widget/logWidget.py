import subprocess

import psutil
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtWidgets import QMessageBox, QTextBrowser, QVBoxLayout, QLabel, QWidget, QHBoxLayout, \
    QPushButton, QSpacerItem, QSizePolicy, QApplication, QDialog, QGridLayout


class LogThread(QThread):
    updated = pyqtSignal(str)
    stopped = pyqtSignal()

    def __init__(self, command, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__command = command
        self.__process = ''
        self.__stopped = False

    def pause(self):
        self.__process.suspend()

    def resume(self):
        self.__process.resume()

    def stop(self):
        self.__process.terminate()
        self.__stopped = True

    def run(self):
        process = subprocess.Popen(
            self.__command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        self.__process = psutil.Process(process.pid)

        while True:
            if self.__stopped:
                self.__stopped = False
                self.stopped.emit()
                return
            realtime_output = process.stdout.readline()
            if realtime_output == '' and process.poll() is not None:
                break
            if realtime_output:
                self.updated.emit(realtime_output.strip())

class LogWidget(QWidget):
    started = pyqtSignal()
    updated = pyqtSignal(str)
    stopped = pyqtSignal()
    finished = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__parent = parent
        if self.__parent:
            self.__parent.closeEvent = self.closeEvent

        self.__initVal()
        self.__initUi()

    def __initVal(self):
        self.__t = ''
        self.__tDeleted = False

        # each text below are appended when process is started and finished (by default)
        # you can change the text with setStartText(start_text: str) and setFinishText(finish_text: str)
        self.__startText = 'Started!'
        self.__finishText = 'Finished!'
        self.__stopText = 'Stopped!'

    def __initUi(self):
        self.setWindowTitle('Log')

        self.__logBrowser = QTextBrowser()

        self.__pauseResumeBtn = QPushButton('Pause')
        self.__pauseResumeBtn.clicked.connect(self.__pauseResumeToggled)

        self.__stopBtn = QPushButton('Stop')
        self.__stopBtn.clicked.connect(self.__stop)

        lay = QHBoxLayout()
        lay.addWidget(self.__pauseResumeBtn)
        lay.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.MinimumExpanding))
        lay.addWidget(self.__stopBtn)
        lay.setContentsMargins(0, 0, 0, 0)

        bottomWidget = QWidget()
        bottomWidget.setLayout(lay)

        lay = QVBoxLayout()
        lay.addWidget(QLabel('Log'))
        lay.addWidget(self.__logBrowser)
        lay.addWidget(bottomWidget)

        self.setLayout(lay)

    def setCommand(self, command: str):
        self.__t = LogThread(command)
        self.__t.finished.connect(self.__t.deleteLater)
        self.__t.finished.connect(self.__handleButton)
        self.__t.started.connect(self.started)
        self.__t.started.connect(self.__appendStartText)
        self.__t.started.connect(self.__handleButton)
        self.__t.updated.connect(self.__logAppend)
        self.__t.updated.connect(self.updated)
        self.__t.stopped.connect(self.stopped)
        self.__t.stopped.connect(self.__appendStopText)
        self.__t.finished.connect(self.finished)
        self.__t.finished.connect(self.__appendFinishText)
        self.__t.start()

    def __stop(self):
        self.__pauseResumeBtn.setText('Pause')
        self.__t.stop()

    # append the text when process is started (one time)
    def __appendStartText(self):
        self.__logBrowser.append(self.__startText)

    # append in general
    def __logAppend(self, text):
        self.__logBrowser.append(text)
        vBar = self.__logBrowser.verticalScrollBar()
        vBar.setValue(vBar.maximum())

    # append the text when process is finished (one time)
    def __appendFinishText(self):
        self.__logBrowser.append(self.__finishText)

    def __appendStopText(self):
        self.__logBrowser.append(self.__stopText)

    def setStartText(self, start_text: str):
        self.__startText = start_text

    def setFinishText(self, finish_text: str):
        self.__finishText = finish_text

    def setStopText(self, stop_text: str):
        self.__stopText = stop_text

    def getStartText(self):
        return self.__startText

    def getFinishText(self):
        return self.__finishText

    def getStopText(self):
        return self.__stopText

    def __handleButton(self):
        self.__tDeleted = self.__t.isFinished()
        self.__pauseResumeBtn.setDisabled(self.__tDeleted)
        self.__stopBtn.setDisabled(self.__tDeleted)

    def __pauseResumeToggled(self):
        if self.__pauseResumeBtn.text() == 'Pause':
            self.__t.pause()
            self.__pauseResumeBtn.setText('Resume')
        elif self.__pauseResumeBtn.text() == 'Resume':
            self.__t.resume()
            self.__pauseResumeBtn.setText('Pause')

    def closeEvent(self, e):
        if isinstance(self.__t, QThread):
            if self.__tDeleted:
                e.accept()
            else:
                self.__t.pause()
                msgBox = QMessageBox()
                msgBox.setWindowTitle('Warning')
                msgBox.setText('Do you want to stop the process?')
                msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                reply = msgBox.exec()
                if reply == QMessageBox.Yes:
                    self.__t.stop()
                    # give the time to stop the process
                    e.accept()
                elif reply == QMessageBox.No:
                    self.__t.resume()
                    e.ignore()
        else:
            e.accept()

class LogDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.__initUi()

    def __initUi(self):
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
        self.__logWidget = LogWidget(self)
        lay = QGridLayout()
        lay.addWidget(self.__logWidget)
        self.setLayout(lay)

    def getLogWidget(self):
        return self.__logWidget


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = LogWidget()
    proc = 'python example.py'
    window.setCommand(proc)
    window.show()
    sys.exit(app.exec())

# Log dialog example
# if __name__ == '__main__':
#     import sys
#
#     app = QApplication(sys.argv)
#     dialog = LogDialog()
#     proc = 'python example.py'
#     dialog.setWindowTitle('Logging...')
#     logWidget = dialog.getLogWidget()
#     logWidget.setCommand(proc)
#     dialog.show()
#     sys.exit(app.exec())