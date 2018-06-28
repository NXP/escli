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


class Model(object):
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
            self.kargs["url_path"] = "/models"

    def _get_token(self):
        """return token or None
        Get the user's token
        """
        return user.get_token()

    def print_details(self, data):
        x=[[]]
        if 'models' in data:
            dic_list = data['models']
        else:
            dic_list=[]
            dic_list.append(data)
        for dic in dic_list:
            if "id" not in dic:
                raise Exception("wrong model response format")
            x.append([dic["id"], "%s-%s-%s-%s" %(dic["model"], dic["platform"], dic["type"], dic["vendor"]),\
                     dic["is_public"]])

        tab = tt.Texttable()
        tab.set_deco(tab.HEADER|tab.BORDER|tab.VLINES)
        tab.add_rows(x)
        tab.header(["id", "name (model-platform-type-vendor)", "is_public"])

        print(tab.draw())

    def get_models(self):
        """Get all of the model list
        """
        token = self._get_token()
        __kargs = self.kargs.copy()
        return process_result(Request(__kargs,token).get())

    def get_models_list_sort(self):
        """Get all of the model list
        """
        token = self._get_token()
        __kargs = self.kargs.copy()
        resp = process_result(Request(__kargs,token).get())
        x={}
        if 'models' in resp:
            dic_list = data['models']
        else:
            dic_list = resp
        for dic in dic_list:
            x[dic["id"]] = "%s-%s-%s-%s" %(dic["model"], dic["platform"], dic["type"], dic["vendor"])
        return x

    def create(self, name, is_public=False):
        """Create a new model name
        """
        token = self._get_token()
        ml = name.split("-")
        if len(ml) != 4:
            raise  Exception('Formt of mode should be "model1-platform2-type3-vendor4"')
        __kargs = self.kargs.copy()
        __kargs["request_body"] = {
            "model": ml[0],
            "platform":  ml[1],
            "type":  ml[2],
            "vendor":  ml[3],
            "permission": is_public
        }
        return process_result(Request(__kargs,token).post())

    def update(self, id, name):
        """Update model name
        """
        token = self._get_token()
        ml = name.split("-")
        if len(ml) != 4:
            raise  Exception('Formt of mode should be "model1-type2-platform2-vendor3"')
        __kargs = self.kargs.copy()
        __kargs["request_body"] = {
            "model": ml[0],
            "type":  ml[1],
            "platform":  ml[2],
            "vendor":  ml[3]
        }
        __kargs["url_path"] += "/%s" %id
        return process_result(Request(__kargs,token).put())

    def getname_byid(self, id):
        """Update model name
        """
        token = self._get_token()
        __kargs = self.kargs.copy()
        __kargs["request_body"] = {
            "model": ml[0],
            "type":  ml[1],
            "platform":  ml[2],
            "vendor":  ml[3]
        }
        __kargs["url_path"] += "/%s" %id
        d = process_result(Request(__kargs,token).put())
        if "model" in d:
            return "%s-%s-%s-%s" %(d["model"],d["platform"],d["type"],d["vendor"])

    def delete_model_by_id(self, model_id):
        """Delete vendor
        """
        token = self._get_token()
        __kargs = self.kargs.copy()
        __kargs["request_body"] = {
            "model_id": model_id
        }
        return process_result(Request(__kargs,token).delete())

