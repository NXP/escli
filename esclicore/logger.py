#####################################
#
# Copyright 2018 NXP
#
#####################################

#!/usr/bin/env python


import sys
import logging

def add_handler(stream, lvl, formatter):
    logger = logging.getLogger("")
    handler = logging.StreamHandler(stream)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(lvl)
    #return handler

def set_default_log(lvl=logging.INFO):
    formatter = logging.Formatter(fmt="%(levelname)-4s: %(message)s")
    add_handler(sys.stdout, lvl, formatter)


