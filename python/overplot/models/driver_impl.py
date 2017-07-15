#
# Copyright (c) 2017-2018, Helge Mathee. All rights reserved.
#

import os
import sys
from PySide import QtCore, QtGui

class driver(QtCore.QObject):

  __plotter = None
  __commands = None

  def __init__(self, parent, plotter):
    super(driver, self).__init__(parent)

    self.__plotter = plotter
    self.__commands = []

    self.__plotter.commandSent.connect(self.__onPlotterCommand)

  @property
  def plotter(self):
    return self.__plotter

  @property
  def commands(self):
    return [] + self.__commands

  def clearCommands(self):
    self.__commands = []

  @QtCore.Slot(str)
  def __onPlotterCommand(self, command):
    self.onPlotterCommand(command)

  def onPlotterCommand(self, command):
    self.__commands.append(command)
