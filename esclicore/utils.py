#####################################
#
# Copyright 2018 NXP
#
#####################################

#!/usr/bin/env python

import json
from .client import Client

class Request(object):
    """high level class to make http request"""

    def __init__(self, kargs, token=None):

        """ kargs: dictionary
        host: string
        api_version: string
        url_path:    string
        headers:     dictionary
        params:      dictionary
        request_body: string request datapayload

        token:  http request token defualt is None
        """

        self.host = "https://ueys86rk5l.execute-api.us-west-2.amazonaws.com"
        self.api_version = "v1"
        self.url_path = "/devices"
        self.headers = {}
        self.params = {}
        self.request_body = None

        if 'host' in kargs:
            self.host = kargs['host']

        if 'api_version' in kargs:
            self.api_version = kargs['api_version']

        if 'url_path' in kargs:
            self.url_path = kargs['url_path']

        if 'headers' in kargs:
            self.headers = kargs['headers']

        if 'params' in kargs:
            self.params = kargs['params']

        if 'request_body' in kargs:
            self.request_body = kargs['request_body']

        # Update token header
        if token != None:
            _token_header = {
                "dcca_token": token
            }
            #self.headers = dict(self.headers.items() + _token_header.items())
            self.headers = self.headers.copy()
            self.headers.update(_token_header)

        # Make the rest-ful request
        self.client = Client(host=self.host, version=self.api_version, request_headers=self.headers, url_path=self.url_path)

    def get(self, to_dict=True):
        resp = self.client.api_keys.get(query_params=self.params).body
        if to_dict:
            return json.loads(resp)
        return resp

    def post(self, to_dict=True):
        return json.loads(self.client.api_keys.post(query_params=self.params, request_body=self.request_body).body)

    def put(self, to_dict=True):
        return json.loads(self.client.api_keys.put(query_params=self.params, request_body=self.request_body).body)

    def delete(self, to_dict=True):
        return json.loads(self.client.api_keys.delete(query_params=self.params, request_body=self.request_body).body)

def meet_filter(dic, filters):
    """ To compare the dic to filter, if meeting the filter, return True
    param dic:      dict type
    param filters:  dict type

    """
    for k, v in filters.iteritems():
        #print k, v
        if v == None:
            continue
        if k in dic and str(dic[k]) != str(v):
            return False
    return True

def print_dict_member(data, key):
    """
    param data: dict type
    param key:  string
    """
    if isinstance(data, dict):
        #for k, v in data.iteritems():
        if key in data:
            if isinstance(data[key], dict) or isinstance(data[key], list):
                print("  %-20s %-60s" %(key, json.dumps(data[key], sort_keys=False)))
            else:
                print("  %-20s %-60s" %(key + ":", str(data[key])))

def update_dic_member(dic, *args):
    """ check the member and return unkonw if member doesn't exist
    param dic:      dict type
    param args:  list type
    """
    for member in args:
        if member not in dic.keys():
            dic[member] = "unknown"
    return dic


def process_result(dict_data):
    """return dict or None
    dict_data type dict
    """
    if "error" in dict_data:
        #print json.dumps(dict_data['error'], sort_keys=False)
        if "message" in dict_data:
            raise Exception(dict_data['message'])
        raise Exception(dict_data)
    if "status" in dict_data and hasattr(dict_data["status"], 'lower'):
        if dict_data["status"].lower() in ["fail", "failed", "failure"]:
            #print json.dumps(dict_data, sort_keys=False)
            if "message" in dict_data:
                raise Exception(dict_data['message'])
            raise Exception(dict_data)
    if "errorType" in dict_data or "stackTrace" in dict_data:
        raise Exception(dict_data)
    return dict_data

