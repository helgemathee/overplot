#
# Copyright (c) 2017-2018, Helge Mathee. All rights reserved.
#

import os
import sys
import math
from PySide import QtCore

class plotter(QtCore.QObject):

  __homePos = None
  __motorPos = None
  __servoAngle = None
  __simMotorPos = None
  __simServoAngle = None
  __settings = None

  __beltLength = None
  __stepperDistance = None
  __stepperDiameter = None

  __canvasWidth = None
  __canvasHeight = None
  __canvasOffset = None

  changed = QtCore.Signal()

  def __init__(self, parent, settings):
    super(plotter, self).__init__(parent)

    self.__settings = settings

    self.__homePos = (0, 0)
    self.__motorPos = (0, 0)
    self.__simMotorPos = (0, 0)
    self.__servoAngle = 0
    self.__simServoAngle = 0

    self.calibrate()

  def homePos(self, index, simulated=True):
    return self.__homePos[index]

  def motorPos(self, index, simulated=True):
    if simulated:
      return self.__simMotorPos[index]
    return self.__motorPos[index]

  def servoAngle(self, simulated=True):
    if simulated:
      return self.__simServoAngle
    return self.__servoAngle

  def belts(self, simulated=True):
    home = self.homePos(simulated)
    motors = self.motorPos(simulated)
    return (motors[0] - home[0], motors[1] - home[1])

  @QtCore.Slot(str, float)
  def onSettingChanged(self, name, value):
    self.update()

  def _posFromBelts(self, belts):
    (a, c) = belts
    b = float(self.__stepperDistance)
    angle = math.acos((b * b + c * c - a * a) / (2.0 * b * c))
    x = math.cos(angle) * c
    y = math.sin(angle) * c
    return (x, y)

  def _beltsFromPos(self, pos):
    x = float(pos[0])
    y = float(pos[1])
    x1 = self.__stepperDistance - x
    a = math.sqrt(x * x + y * y)
    c = math.sqrt(x1 * x1 + y * y)
    return (a, c)

  def update(self):
    self.__beltLength = float(self.__settings.value('settings.beltlength', 1000))
    self.__stepperDistance = float(self.__settings.value('settings.left2right', 2000))
    self.__stepperDiameter = float(self.__settings.value('settings.stepperDiameter', 12))

    self.__canvasOffset = 250
    self.__canvasWidth = int(self.__stepperDistance) * 2 * self.__canvasOffset
    self.__canvasHeight = int(self.__beltLength * 0.75) + self.__canvasOffset

  def calibrate(self):
    self.update()

    left2gondola= float(self.__settings.value('settings.left2gondola', 150))
    right2gondola= float(self.__settings.value('settings.right2gondola', 150))

    (homeX, homeY) = self._posFromBelts((self.__beltLength, self.__beltLength))
    homeY = homeY * 0.5
    (homeL, homeR) = self._beltsFromPos((homeX, homeY))

    self.__homePos = (left2gondola - homeL, right2gondola - homeR)

    print self.__homePos
    print self._posFromBelts((left2gondola, right2gondola))
    print self._posFromBelts((homeL, homeR))
