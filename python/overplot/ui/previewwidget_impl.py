#
# Copyright (c) 2017-2018, Helge Mathee. All rights reserved.
#

from PySide import QtCore, QtGui

class PreviewWidget(QtGui.QWidget):

  __plotter = None

  def __init__(self, parent, plotter):
    super(PreviewWidget, self).__init__(parent)

    self.__plotter = plotter


  def paintEvent(self, event):

    r = event.rect()
    p = QtGui.QPainter()
    p.begin(self)

    p.setBrush(QtGui.QColor(60, 60, 60))
    p.drawRect(r)

    p.end()
