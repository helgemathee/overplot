#
# Copyright (c) 2017-2018, Helge Mathee. All rights reserved.
#

from PySide import QtCore, QtGui

class LogWidget(QtGui.QWidget):

  __log = None

  def __init__(self, parent):

    super(LogWidget, self).__init__(parent)

    layout = QtGui.QVBoxLayout()
    self.setLayout(layout)

    self.setContentsMargins(5, 5, 5, 5)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setAlignment(QtCore.Qt.AlignTop)

    self.__log = QtGui.QPlainTextEdit(self)
    self.__log.setReadOnly(True)
    palette = self.palette()
    logPalette = self.__log.palette()
    logPalette.setBrush(QtGui.QPalette.Window, palette.brush(QtGui.QPalette.WindowText))
    logPalette.setBrush(QtGui.QPalette.WindowText, palette.brush(QtGui.QPalette.Window))
    logPalette.setBrush(QtGui.QPalette.Base, palette.brush(QtGui.QPalette.Text))
    logPalette.setBrush(QtGui.QPalette.Text, palette.brush(QtGui.QPalette.Base))
    self.__log.setPalette(logPalette)
    layout.addWidget(self.__log)

  @QtCore.Slot(str)
  def onLogEntryReceived(self, entry):
    self.__log.appendPlainText(entry)
