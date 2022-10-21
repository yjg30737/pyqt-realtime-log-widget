# pyqt-realtime-log-widget
Display log in real time with PyQt widget

## Requirements
* PyQt5

## Install
`python -m pip install git+https://github.com/yjg30737/pyqt-realtime-log-widget.git --upgrade`

If you want to test or modify this, clone it.

It has test code already so you can just run the logWidget.py.

## Method Overview
* `setCommand(command: str)` - set the command that you want to see the log in real time.
* started - signal emitted after command being started.
* updated(str) - signal emitted after log being updated. updated line as an argument.
* finished - signal emitted after command being finished

## Feature
* You can pause/resume/stop the command
* Vertical scroll bar always at the bottom while log is displaying
* Show the warning dialog when you try to close the widget. Process is suspended while warning dialog is showing. If you press Yes, process will be terminated and widget will be closed. If you press no, process will be keep running until it is finished.
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





