#####################################
#
# Copyright 2018 NXP
#
#####################################

import os
import json
import sys
import logging
import esclicore.user as user
import esclicore.device as device


log = logging.getLogger("")
#log.setLevel(logging.DEBUG)

#user.logout()

data = {"username": "b25332", "password": "freescale456"}
#user.login(data=data)

kargs={'host': None, "out_json": False, "api_version": None, "url_path": None} 

device.get_devices(kargs)
