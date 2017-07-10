#
# Copyright (c) 2017-2018, Helge Mathee. All rights reserved.
#

from PySide import QtCore, QtGui

class PreviewWidget(QtGui.QWidget):

  __plotter = None

  def __init__(self, parent, plotter):
    super(PreviewWidget, self).__init__(parent)

    self.__plotter = plotter
    self.__plotter.changed.connect(self.onChanged)

  def resizeEvent(self, event):
    w = event.size().width()
    h = event.size().height()
    self.__pixmap = QtGui.QPixmap(w, h)
    self.clearPixmap()

  def clearPixmap(self):
    self.__pixmap.fill(QtGui.QColor(60, 60, 60))
    # todo: replot!

  @QtCore.Slot()
  def onChanged(self):
    self.update()

  def paintEvent(self, event):

    w = self.geometry().width()
    h = self.geometry().height()

    r = event.rect()
    p = QtGui.QPainter()
    p.begin(self)

    p.drawPixmap(0, 0, self.__pixmap)

    p.setPen(QtGui.QPen(QtGui.QColor(255, 0, 0), 1.0))

    home = self.__plotter.homePoint(w=w)
    p.drawLine(home.x() - 10, home.y(), home.x() + 10, home.y())
    p.drawLine(home.x(), home.y() - 10, home.x(), home.y() + 10)

    p.setPen(QtGui.QPen(QtGui.QColor(255, 255, 0), 1.0))
    p.drawLine(self.__plotter.point(0, 0, w=w), self.__plotter.point(self.__plotter.stepperDistance, 0, w=w))
    p.drawLine(self.__plotter.point(0, 0, w=w), self.__plotter.point(w=w))
    p.drawLine(self.__plotter.point(self.__plotter.stepperDistance, 0, w=w), self.__plotter.point(w=w))


    p.end()
