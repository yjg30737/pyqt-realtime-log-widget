from setuptools import setup, find_packages

setup(
    name='pyqt-realtime-log-widget',
    version='0.0.1',
    author='Jung Gyu Yoon',
    author_email='yjg30737@gmail.com',
    license='MIT',
    packages=find_packages(),
    description='Display log in real time with PyQt',
    url='https://github.com/yjg30737/pyqt-realtime-log-widget.git',
    install_requires=[
        'PyQt5',
        'psutil'
    ]
)