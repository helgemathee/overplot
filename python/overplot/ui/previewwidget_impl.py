#
# Copyright (c) 2017-20187, Helge Mathee. All rights reserved.
#

from PySide import QtCore, QtGui

class PreviewWidget(QtGui.QWidget):

  def __init__(self, parent):
    super(PreviewWidget, self).__init__(parent)


  def paintEvent(self, event):

    r = event.rect()
    p = QtGui.QPainter()
    p.begin(self)

    p.setBrush(QtGui.QColor(255, 0, 0))
    p.drawRect(r)

    p.end()
