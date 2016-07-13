#!/usr/bin/python

from func import *
from service import *


if argv(1) == "start" and isNum(argv(2, default=False)):
        run(argv(2))
elif argv(1) == "stop":
        stop()
elif argv(1) == "status":
        status()
elif argv(1) == "log":
        readlog();
else:
        help(argv(0))

quit();
