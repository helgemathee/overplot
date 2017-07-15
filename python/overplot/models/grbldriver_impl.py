#
# Copyright (c) 2017-2018, Helge Mathee. All rights reserved.
#

import os
import sys
import time
import serial
from PySide import QtCore, QtGui

from driver_impl import driver
from grbl_impl import grbl

class GrblDriver(driver):

  __grbl = None

  def __init__(self, parent, plotter, port, baud=115200):
    super(GrblDriver, self).__init__(parent, plotter)
    self.__grbl = grbl(port, baud)

  def connect(self):
    self.__grbl.connect()

  def disconnect(self):
    self.__grbl.disconnect()

  def onPlotterCommand(self, command):
    super(GrblDriver, self).onPlotterCommand(command)
    self.__grbl.sendCommand(command)
