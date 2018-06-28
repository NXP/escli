#####################################
#
# Copyright 2018 NXP
#
#####################################

#!/usr/bin/env python

import json
import logging
import os
import sys
import errno
from . import logger as eslog
from .utils import Request, process_result


log = logging.getLogger("u")
eslog.set_default_log()

tokenfile = os.path.expanduser("~/edgescale/") + "token.txt"

def create_token_file(filename):
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise Exception("tokenfile exist")

def get_token():
    if not is_login():
        print("login first")
        raise Exception("login first")

    log.debug("reading token from file: %s", tokenfile)
    try:
        with open(tokenfile, 'r') as f:
            token = f.read().replace('\n', '')
            if len(token) < 2:
                print("error: token length is too short")
                raise Exception("token length short")
    except Exception:
        raise Exception("error: reading token fail")
    return token

def logout():
    try:
        os.remove(tokenfile)
        log.info("Success to logout")
    except Exception:
        log.info("You have logout")


def login(kargs, username='', password=''):
    """ log in the server and save token file
    :kargs dic
    :username: string
    :passwrod: string
    """
    if username == '' or password == '':
        raise Exception("username or passworld is null")

    kargs["request_body"] = {
        "username": username,
        "password": password
    }
    # Generate url path 
    if "url_path" not in kargs:
        kargs["url_path"] = "/users/login"

    resp_dic = process_result(Request(kargs).post())
    if "token" in resp_dic:
        create_token_file(tokenfile)
        with open(tokenfile, "w") as f:
            f.write(resp_dic['token'])
        
    log.debug("token: %s",get_token())

def is_login():
    return os.path.exists(tokenfile)

