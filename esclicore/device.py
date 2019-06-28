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
import texttable as tt
from . import user
from .utils import Request, print_dict_member
from .utils import update_dic_member, process_result



class Device(object):
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

    def _get_token(self):
        """return token or None
        Get the user's token
        """
        return user.get_token()

    def query_device_by_id(self, id):
        """return dict"""
        self.kargs['url_path'] = self.kargs['url_path'] + "/" + str(id)
        token = self._get_token()
        return process_result(Request(self.kargs,token).get())

    def fuid_to_uid(self, fuid):
        """return dict"""
        self.kargs['url_path'] = self.kargs['url_path'] + "?fuid=" + str(fuid)
        token = self._get_token()
        resp = Request(self.kargs,token).get(to_dict=False)
        process_result(json.loads(resp))
        return eval(resp)

    def delete_device_by_id(self, id):
        """return dict"""
        self.kargs['url_path'] = self.kargs['url_path'] + "/" + str(id)
        token = self._get_token()
        return process_result(Request(self.kargs,token).delete())
    
    def get_devices(self):
        """return dict"""
        token = self._get_token()
        return process_result(Request(self.kargs,token).get())

    def upload_device_db(self, raw_data, keyid):
        """return dict"""
        token = self._get_token()
        __kargs = self.kargs.copy()
        __kargs['request_body'] = {
            "data": raw_data,
            "key_id": keyid
        }
        return process_result(Request(__kargs,token).post())

    def create_device(self):
        """return dict"""
        token = self._get_token()
        return process_result(Request(self.kargs,token).post())
    
    def get_device_cert(self, device_name):
        """return body"""
        self.kargs['params'] = {
           "device_name": device_name
        }

        token = self._get_token()
        resp = Request(self.kargs,token).get(to_dict=False)
        process_result(json.loads(resp))
        return resp

def print_header():
    print("%-4s %-64s %-8s %-30s %-15s" %('ID', 'device_name', 'status', 'create_time','local_ip'))
    print("-------------------------------------------------------------------------------------------------------------------------")

def print_device(data, max_width=150):
    """
    :param item: dict type
    """
    x=[[]]
    if 'results' in data:
        dic_list = data['results']
    else:
        dic_list = data
    for dic in dic_list:
        if "id" not in dic:
            return

        x.append([dic["id"], dic["name"]+"\n", dic['status'], dic['created_at'], dic['local_ip']])

    tab = tt.Texttable(max_width=max_width)
    tab.set_deco(tab.HEADER|tab.BORDER|tab.VLINES)
    tab.add_rows(x)
    #tab.set_cols_width([5, 50, 8, 20, 25])
    tab.header(["id", "Device name", "Status", "Create time", "IP addr"])

    print(tab.draw())


def print_device_json(item):
    print(json.dumps(item, sort_keys=True, indent=4))

def print_device_details(data):
    """data: type dictionary"""
    if 'device_info' in data:
        dic = data['device_info']
    else:
        dic = data
    print("----------------------------------------------------------------------")
    if isinstance(dic, dict):
        print_dict_member(dic, "id")
        #print_dict_member(dic, "device_id")
        print_dict_member(dic, "name")
        print_dict_member(dic, "created_at")
        print_dict_member(dic, "last_report")
        print_dict_member(dic, "mode")
        print_dict_member(dic, "certname")
        print_dict_member(dic, "uid")
        print_dict_member(dic, "cpu_usage")
        print_dict_member(dic, "mem_usage")
        print_dict_member(dic, "es_version")
        print_dict_member(dic, "app_num")
        print_dict_member(dic, "mac")
        print_dict_member(data,"tags")
    print("")

