#
# Copyright (c) 2017-2018, Helge Mathee. All rights reserved.
#

from PySide import QtCore, QtGui

from overplot.models.driver_impl import driver

class PreviewDriver(driver):

  __pixmap = None
  __firstPos = None
  __lastPos = None
  __isPenDown = None

  def __init__(self, parent, plotter):
    super(PreviewDriver, self).__init__(parent, plotter)
    self.__firstPos = self.plotter._posFromBelts(self.plotter.belts())
    self.__lastPos = self.__firstPos
    self.__isPenDown = True

  def setPixmap(self, pixmap):
    self.__pixmap = pixmap
    self.__pixmap.fill(QtGui.QColor(60, 60, 60))
    self.__lastPos = self.__firstPos

    commands = self.commands
    self.clearCommands()

    for c in commands:
      self.onPlotterCommand(c)

  def onPlotterCommand(self, command):
    super(PreviewDriver, self).onPlotterCommand(command)

    parts = command.split(' ')
    if parts[0] in ['G0', 'G1']:
      p = self.plotter._posFromBelts((float(parts[1][1:]), float(parts[2][1:])))
      if self.__isPenDown and self.__pixmap:
    
        painter = QtGui.QPainter(self.__pixmap)
        painter.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255), 1.0))

        a = self.plotter.point(x=self.__lastPos[0], y=self.__lastPos[1], w=self.__pixmap.width())
        b = self.plotter.point(x=p[0], y=p[1], w=self.__pixmap.width())
        painter.drawLine(a, b)

        painter.end()

      self.__lastPos = p

    elif parts[0] in ['M5']:
      self.__isPenDown = True

    elif parts[0] in ['M3']:
      self.__isPenDown = float(parts[1][1:]) == 0.0
