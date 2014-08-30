#!/usr/bin/python

from interface import *
from threading import Thread
import time
interface = Interface()

thread=Thread(target=interface.start)
thread.start()

time.sleep(3)
interface.grid[27][18]=True
