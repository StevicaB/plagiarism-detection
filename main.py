'''The first entrypoint in the program.

Made by: Stevica Bozhinoski

'''

#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui

from modules.user_interface import MainWindow

if __name__ == '__main__':
    APPLICATION = QtGui.QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(APPLICATION.exec_())
