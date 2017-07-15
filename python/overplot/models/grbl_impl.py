#
# Copyright (c) 2017-2018, Helge Mathee. All rights reserved.
#

import os
import sys
import time
import serial

class grbl(object):

  __port = None
  __baud = None
  __conn = None
  __gcount = None
  __cline = None

  def __init__(self, port, baud=115200):
    super(grbl, self).__init__()

    self.__port = port
    self.__baud = baud

  def connect(self):
    if self.__conn:
      return
    self.__conn = serial.Serial(self.__port, self.__baud)
    self.__gcount = 0
    self.__cline = []

    # Wake up grbl
    self.__conn.write("\r\n\r\n")

    # Wait for grbl to initialize and flush startup text in serial input
    time.sleep(2)
    self.__conn.flushInput()

  def disconnect(self):
    if not self.__conn:
      return
    self.__conn.close()
    self.__conn = None

  def sendCommand(self, command):
    if not self.__conn:
      return

    print command
    self.__conn.write(str(command).strip() + '\n')
    result = []

    # todo: we need to figure out how long to wait for commands

    while True:
      l = self.__conn.readline().strip()
      if not l or l.find('ok') >= 0:
        break
      if l.find('error') >= 0:
        print 'grbl: {0}'.format(l)
        break
      result += [l]
    return result
