#####################################
#
# Copyright 2018 NXP
#
#####################################

#!/usr/bin/env python

import json
import os
import sys
import errno
import texttable as tt
from . import user
from .utils import Request, process_result


class Vendor(object):
    """cli device query and management class"""

    def __init__(self, kargs):
        """
        kargs: dictionary
            host: string
            api_version: string
            url_path:    string
            headers:     dictionary
            params:      dictionary
            request_body: string request datapayload
        """
        self.kargs = kargs
        if "url_path" not in self.kargs:
            self.kargs["url_path"] = "/vendors"

    def _get_token(self):
        """return token or None
        Get the user's token
        """
        return user.get_token()

    def print_details(self, data):
        x=[[]]
        if 'vendors' in data:
            dic_list = data['vendors']
        else:
            dic_list = data
        for dic in dic_list:
            if "id" not in dic:
                return

            x.append([dic["id"], dic["name"]])

        tab = tt.Texttable()
        tab.set_deco(tab.HEADER|tab.BORDER|tab.VLINES)
        tab.add_rows(x)
        tab.header(["id", "name"])

        print(tab.draw())

    def get_vendors(self):
        """Get all of the vendor list
        """
        token = self._get_token()
        __kargs = self.kargs.copy()
        return process_result(Request(__kargs,token).get())

    def create(self, name):
        """Create a new vendor
        """
        token = self._get_token()
        __kargs = self.kargs.copy()
        __kargs["request_body"] = {
            "name": name
        }
        return process_result(Request(__kargs,token).post())

    def delete_vendor_by_id(self, vendor_id):
        """Delete vendor
        """
        token = self._get_token()
        __kargs = self.kargs.copy()
        __kargs["params"] = {
            "id": vendor_id
        }
        return process_result(Request(__kargs,token).post())

