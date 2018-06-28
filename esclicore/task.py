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
from .solution import Solution as Sol
from .utils import Request, process_result, print_dict_member


class Task(object):
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
            self.kargs["url_path"] = "/tasks"

    def _get_token(self):
        """return token or None
        Get the user's token
        """
        return user.get_token()

    def print_list(self, data):
        x=[[]]
        if 'items' in data:
            dic_list = data['items']
        else:
            dic_list = data

        # Gen application
        for dic in dic_list:
            if "id" not in dic:
                continue
            if isinstance(dic["payload"], list) and "application_id" in dic["payload"][0]:
                d = dic["payload"][0]
                x.append([dic["id"], dic["type"], dic["status"], "app_id:%s;version:%s"\
                    %(d["application_id"],d["version"])])

        # Gen solution
        for dic in dic_list:
            if "id" not in dic:
                continue
            if "solution_id" in dic["payload"]:
                d = dic["payload"]
                x.append([dic["id"], dic["type"], dic["status"], "%s-%s;model_id:%d"\
                    %(d["solution"],d["version"], d["model_id"])])

        tab = tt.Texttable()
        tab.set_deco(tab.HEADER|tab.BORDER|tab.VLINES)
        tab.add_rows(x)
        tab.header(["id", "type", "status", "metadata"])

        print(tab.draw())

    def print_show(self, dic):
        if "id" not in dic:
            return
        a ={}
        print("----------------------------------------------------------------------")
        if isinstance(dic, dict):
            a["message"] = json.dumps(dic["status_payload"][0]["payloads"], sort_keys=False)[0:80]
            try:
                a["status"] = dic["status_payload"][0]["payloads"][0]["status"][0:20]
            except:
                a["status"] = dic["status"]
            print_dict_member(dic, "id")
            print_dict_member(dic, "type")
            print_dict_member(dic, "create_time")
            print_dict_member(a, "status")
            print_dict_member(dic["status_payload"][0], "device_name")
            print_dict_member(dic["status_payload"][0], "device_id")
            print_dict_member(dic["payload"], "solution")
            if isinstance(dic["payload"], list) and "application_id" in dic["payload"][0]:
                print_dict_member(dic["payload"][0], "application_id")
            print_dict_member(dic["payload"], "version")
            print_dict_member(dic["payload"], "url")
            print_dict_member(a, "message")
        print("")

    def create_app_task(self, device_list, version, app_id):
        """
        Create a new model name
        @device_list: string, split space Eg: "12 23 43 33"
        @version: type string, application version
        @app_id:  type int, application ID
        """
        token = self._get_token()
        __kargs = self.kargs.copy()
        ids_int = [int(i) for i in device_list.replace(';', ' ').split()]
        __kargs["request_body"] = {
            "task": {
                "device_ids": ids_int,
                "type":  "deploy_app",
                "payload":  [{"version": version, "application_id": app_id}],
            }
        }
        return process_result(Request(__kargs,token).post())

    def create_solution_task(self, device_list, sid):
        """
        Create a new model name
        @device_list: string, split space Eg: "12 23 43 33"
        @sid:  type int, solution id
        """
        token = self._get_token()
        __kargs = self.kargs.copy()

        self.kargs["url_path"] = "/solutions"
        resp = Sol(self.kargs).show(sid)

        _model_id = resp["model_id"]
        _name = resp["solution"]
        _id = int(sid)
        _version = resp["version"]
        _url = resp["link"]
        _payload = {"model_id": _model_id, "solution": _name, "solution_id": _id, \
                    "version":_version, "url": _url}

        __kargs["request_body"] = {
            "task": {
                "device_ids": [int(i) for i in device_list.replace(';', ' ').split()],
                "type":  "deploy_solution",
                "payload":  _payload
            }
        }
        return process_result(Request(__kargs,token).post())


    def list(self):
        """show task list
        """
        token = self._get_token()
        __kargs = self.kargs.copy()
        return process_result(Request(__kargs,token).get())

    def delete_task_by_id(self, task_id):
        """Delete task
        """
        token = self._get_token()
        __kargs = self.kargs.copy()
        __kargs["params"] = {
            "task_ids": task_id
        }
        return process_result(Request(__kargs,token).delete())

    def show(self, task_id):
        """show specific task info
        """
        token = self._get_token()
        __kargs = self.kargs.copy()
        __kargs["url_path"] += "/%s"%(str(task_id))
        return process_result(Request(__kargs,token).get())

