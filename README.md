# pyqt-realtime-log-widget
Display log in real time with PyQt widget

## Requirements
* PyQt5

## Install
`python -m pip install git+https://github.com/yjg30737/pyqt-realtime-log-widget.git --upgrade`

If you want to test or modify this (obviously) clone it.

It has test code already so you can just run the logWidget.py.

## Method Overview
* `setProcess(proc: str)` - set the command that you want to see the log in real time.

## Feature
* You can pause/resume/stop the command
* Vertical scroll bar always at the bottom while log is displaying
* Show the warning dialog when you try to close the widget. Process is suspended while warning dialog is showing. If you press Yes, process will be terminated and widget will be closed. If you press no, process will be keep running until it is finished.   

## Example
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
    proc = 'python example.py'
    window.setProcess(proc)
    window.show()
    sys.exit(app.exec())
```

Run it.

Result

https://user-images.githubusercontent.com/55078043/197136837-97503e15-dc7b-4fa7-b892-e7c8c41d5a61.mp4

