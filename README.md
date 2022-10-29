# pyqt-realtime-log-widget
Display command log in real time with PyQt widget.

This is using subprocess and psutil to execute/manuever the process, using QThread and a variety of signals defined by me to demonstrate process' log.

## Requirements
* PyQt5
* psutil

## Install
`python -m pip install pyqt-realtime-log-widget --upgrade`

If you want to test or modify this, clone it.

It has test code already so you can just run the logWidget.py.

## Class/Method Overview
* `LogWidget(parent=None)`
    * `setCommand(command: str)` - set the command that you want to see the log in real time.
    * `started` - signal emitted after command being started.
    * `updated(str)` - signal emitted after log being updated. updated line as an argument.
    * `stopped` - signal emitted after log being stopped.
    * `finished` - signal emitted after command being finished
    * `setStartText(start_text: str)` - set the text you want to add when process begins to execute
    * `setStopText(stop_text: str)` - set the text you want to add when process being stopped
    * `setFinishText(finish_text: str)` - text when process being finished
    * `getStartText`, `getStopText`, `getFinishText` are also provided.
* `LogDialog()` - Simply put, dialog version of LogWidget. Currently under development, just use `LogWidget`.
    * `getLogWidget()` - I believe this is self-explanatory.
## Feature
* You can pause/resume/stop the command
* Vertical scroll bar always at the bottom while log is displaying
* Show the warning dialog when you try to close the widget, if you give the parent widget to the constructor such as `LogWidget(self)`. Process is suspended while warning dialog is showing. If you press Yes, process will be terminated and widget will be closed. If you press no, process will be keep running until it is finished.
* You can use the signal like `started`, `updated`, `finished` as i mentioned before.

## Example
### Example 1
You need an example.py file. make it, write the code like below.

```python
for i in range(1000):
    for j in range(1000000):
        pass
    print(f'Log {i}')
```

After doing it, make main.py file or something like that and write the code below. 

```python
from PyQt5.QtWidgets import QApplication
from pyqt_realtime_log_widget import LogWidget

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = LogWidget()
    comm = 'python example.py'
    window.setCommand(comm)
    window.show()
    sys.exit(app.exec())
```

Run it.

### Result 1

https://user-images.githubusercontent.com/55078043/197136837-97503e15-dc7b-4fa7-b892-e7c8c41d5a61.mp4

### Example 2
Make example.py file.
```python
for i in range(100):
    for j in range(1000000):
        pass
    print(f'Log {i}')
```

Make the Python script and write the code below
```python
from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget
from pyqt_realtime_log_widget import LogWidget


class Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.__initUi()

    def __initUi(self):
        self.__btn = QPushButton('Start')
        self.__btn.clicked.connect(self.__start)
        self.__logWidget = LogWidget(self)
        self.__logWidget.layout().setContentsMargins(0, 0, 0, 0)
        self.__logWidget.finished.connect(self.__finished)
        lay = QVBoxLayout()
        lay.addWidget(self.__btn)
        lay.addWidget(self.__logWidget)
        self.setLayout(lay)

    def __start(self):
        self.__btn.setEnabled(False)
        comm = 'python example.py'
        self.__logWidget.setCommand(comm)

    def __finished(self):
        self.__btn.setEnabled(True)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    sys.exit(app.exec())
```

Run.

### Result 2

https://user-images.githubusercontent.com/55078043/197147702-c1c86945-819d-40e6-ae4a-084146344eb9.mp4

### Example 3 (LogDialog)
```python
from PyQt5.QtWidgets import QApplication
from pyqt_realtime_log_widget import LogDialog
//...

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    dialog = LogDialog()
    proc = 'python example.py'
    dialog.setWindowTitle('Logging...')
    logWidget = dialog.getLogWidget()
    logWidget.setCommand(proc)
    dialog.show()
    sys.exit(app.exec())
```

Result? It's just a dialog version of LogWidget, so it is pointless to upload the image.

## Note
Currently stop and finish signal is not well-distinguished. When process being stopped, finished event will be emitted as well, so it will be very confusing. I will fix it or how about you fix it for me?
