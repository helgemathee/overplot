#
# Copyright (c) 2017-20187, Helge Mathee. All rights reserved.
#

import sys
from PySide import QtCore, QtGui
from overplot.ui.mainwindow_impl import MainWindow

app = QtGui.QApplication(sys.argv)
app.setOrganizationName("HelgeMathee")
app.setOrganizationDomain("helgemathee.com")
app.setApplicationName("Overplot Control")

window = MainWindow()
window.show()

app.exec_()
