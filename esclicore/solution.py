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
from .utils import Request, process_result, print_dict_member


class Solution(object):
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
            self.kargs["url_path"] = "/solutions"
        if "params" not in self.kargs:
            self.kargs["params"] = {}

    def _get_token(self):
        """return token or None
        Get the user's token
        """
        return user.get_token()

    def print_list(self, data, max_width=150):
        x=[[]]
        if 'results' in data:
            dic_list = data['results']
        else:
            dic_list = []
            dic_list.append(data)
        # Gen list
        for d in dic_list:
            if "id" not in d:
                continue
            if isinstance(d['model'], dict):
                m = d['model']
            else:
                m = d
            x.append([d["id"], "%s:%s"%(d["solution"],d["version"]),"%s-%s-%s-%s"\
                     %(m["model"], m["platform"], m["type"], m["vendor"]), \
                     os.path.basename(d["link"])+"\n", d["is_public"]])

        tab = tt.Texttable(max_width=max_width)
        tab.set_deco(tab.HEADER|tab.BORDER|tab.VLINES)
        tab.add_rows(x)
        #tab.set_cols_width([5, 20, 25, 30, 10])
        tab.header(["id", "name:version", "model", "image_name", "is_public"])

        print(tab.draw())

    def create(self, name, version, model_id, image_url, is_public=True, public_key=None):
        """
        Create a solution
        @name: string, solution name
        @version: string, solution version
        @version: type string, application version
        @model_id:  type int, model's ID
        @image_url: image full usr
        """
        import os.path
        token = self._get_token()
        if public_key==None:
            is_signed = False
        else:
            is_signed = True

        __kargs = self.kargs.copy()
        __kargs["request_body"] = {
           "solution": name,
           "model_id":  model_id,
           "version":  version,
           "image":  os.path.basename(image_url),
           "url":  image_url,
           "is_public":  is_public,
           "is_signed":  is_signed,
           "public_key":  public_key
        }
        return process_result(Request(__kargs,token).post())

    def update(self, sid, image_url, is_private=False):
        """Update model name
        """
        token = self._get_token()
        __kargs = self.kargs.copy()
        __kargs["request_body"] = {
            "id": int(sid),
            "url":  image_url,
            "is_public": not is_private
        }
        return process_result(Request(__kargs,token).put())

    def list(self):
        """query solution list
        """
        token = self._get_token()
        __kargs = self.kargs.copy()
        r = process_result(Request(__kargs,token).get())

        __kargs['params'].update({"my_solution": "true"})
        my = process_result(Request(__kargs,token).get())

        r['results']= r.get('results',[])+ my.get('results',[])
        r['total']+=my.get("total", 0)
        return r

    def delete_solution_by_id(self, sid):
        """Delete task
        @sid: string solution id
        """
        token = self._get_token()
        __kargs = self.kargs.copy()
        __kargs["request_body"] = {
            "id": [int(i) for i in sid.replace(';', ' ').split()]
        }
        return process_result(Request(__kargs,token).delete())

    def show(self, solution_id):
        """show specific task info
        """
        token = self._get_token()
        __kargs = self.kargs.copy()
        __kargs["url_path"] += "/%s"%(str(solution_id))
        return process_result(Request(__kargs,token).get())

