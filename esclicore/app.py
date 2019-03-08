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
from . import user
import texttable as tt
from .utils import Request, process_result


class App(object):
    """cli application  management class"""

    def __init__(self, kargs={}):
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
            self.kargs["url_path"] = "/applications"

    def _get_token(self):
        """return token or None
        Get the user's token
        """
        return user.get_token()

    def print_details(self, data, max_width=150):
        x=[[]]
        if 'applications' in data:
            dic_list = data['applications']
        else:
            dic_list = data
        for dic in dic_list:
            if "id" not in dic:
                return 
            if "vendor" not in dic:
                dic["vendor"] = "unknown"

            #dic["versions"] = self.get_app_version_by_id(dic["id"])

            x.append([dic["id"], dic["name"], dic['display_name'], dic['is_public'], dic['description']])

        tab = tt.Texttable(max_width=max_width)
        tab.set_deco(tab.HEADER|tab.BORDER|tab.VLINES)
        tab.add_rows(x)
        tab.header(["id", "name", "display_name", "is_public", "description"])

        print(tab.draw())

    def get_app_version_by_id(self, appid):
        """return application version list"""
        token = self._get_token()
        __kargs = self.kargs.copy()
        __kargs["url_path"] = "/applications/%s/versions" %(str(appid))
        res = process_result(Request(__kargs,token).get())
        return res["versions"]

    def get_app_tag_by_id(self, appid):
        """return application tag list"""
        token = self._get_token()
        __kargs = self.kargs.copy() 
        __kargs["url_path"] = "/applications/tags"

        __kargs["params"] = {
            "app_ids": appid
        }
        res = process_result(Request(__kargs,token).get())
        return res["items"][appid]

    def query_apps(self):
        """return dict"""
        token = self._get_token()

        # Get private application
        ret1 = process_result(Request(self.kargs,token).get())

        # Get public application
        __kargs = self.kargs.copy()
        __kargs["url_path"] = "/applications/store"
        resp = process_result(Request(__kargs, token).get())

        if "applications" in resp:
            resp["applications"] += ret1["applications"]

        return resp

    def show(self, id):
        """return dict"""
        ret={}
        token = self._get_token()
        __kargs = self.kargs.copy()
        __kargs["url_path"] = "/applications/%s"%(str(id))
        ret["basic_info"] = process_result(Request(__kargs,token).get())

        __kargs["url_path"] = "/applications/%s/images"%(str(id))
        ret["image_info"] = process_result(Request(__kargs,token).get())
        return ret

    def __create_app_skin(self, name, disp_name, vendor_id, \
                          image=None, description=None):
        """return dict
        :name: application name type string
        :disp_name  display name string
        :vendor_id  application vendor id int
        :image:  picture link
        :description: application description sting
        """
        token = self._get_token()
        __kargs = self.kargs.copy()
        __kargs['request_body'] = {
            "application": {
                 "name": name,
                 "display_name": disp_name,
                 "vendor_id": vendor_id,
                 "description": description,
                 "image": image
            }
        }
        return process_result(Request(__kargs,token).post())

    def __create_app_docker(self, app_id, name, registry_id, \
                            image_name, version, commands, cmdargs, host_network=True):
        """return dict
        :app_id  application ID int
        :name: application name type string
        :registry_id  docker registry ID int
        :image_name  docker app name string
        :version     docker app version/tag string
        :commands    docker command string
        :cmdargs        docker command argrument string
        """

        """
        __kargs['request_body'] = {
            "dynamic_commands": commands,
            "dynamic_args": cmdargs
            "dynamic_cap_add": True,
            "dynamic_host_network": True,
            "dynamic_ports": [
                {
                    "containerPort": "",
                    "hostPort": ""
                }
            ],
            "dynamic_volumes": [
                {
                    "hostPath": "",
                    "mountPathReadOnly": False,
                    "mountPath": ""
                }
            ]
        }
        """
        token = self._get_token()
        __kargs = self.kargs.copy()
        __kargs['request_body'] = {
            "image": {
                 "application_id": app_id,
                 "registry_id": registry_id,
                 "image_name": image_name,
                 "version": version,
                 "commands": commands,
                 "args": cmdargs
            },
            "arguments":{
                "cap_add": True,
                "host_network": True,
                "ports": [
                    {
                        "containerPort": "",
                        "hostPort": ""
                    }
                ],
                "volumes": [
                    {
                        "hostPath": "",
                        "mountPathReadOnly": False,
                        "mountPath": ""
                    }
                ]
            }
        }
        if host_network != True:
            __kargs['request_body']['arguments'].update({"host_network": False})

        __kargs["url_path"] = __kargs["url_path"] + "/%d/images" %(app_id)

        return process_result(Request(__kargs,token).post())

    def create(self, name, registry_id, image_name, version="latest", \
          vendor_id=None, image=None, commands=None, args=None, description=None):

        """return dict
        :name: application name type string
        :registry_id  docker registry ID int
        :image_name  docker app name string
        :version     docker app version/tag string
        :commands    docker command string
        :args        docker command argrument string
        """
        resp_s = self.__create_app_skin(name, name, vendor_id, image, description)
        resp = self.__create_app_docker(resp_s["app_id"], name, registry_id, image_name, version, commands, args)
        #print dict(resp_s.items() + resp.items())
        return resp

    def deploy_app_to_device(self, device_id, app_id, host_net=True, app_version=None):
        """return dict
        device_id: int
        app_id: int
        app_version: string
        """
        token = self._get_token()

        version_list = self.get_app_version_by_id(app_id)
        if app_version == None:
            if len(version_list) > 0:
                app_version = version_list[0]
        else:
            if not app_version in version_list:
                raise Exception("valid app_version: %s" %str(json.dumps(version_list)))

        __kargs = self.kargs.copy()
        __kargs["url_path"] = "/deployment/applications"
        __kargs['request_body'] = {
            "deploy": {
                 "application_id": app_id,
                 "version": app_version,
                 "device_id": device_id,
            },
           #
           # "parameters": {
           #     "dynamic_commands": "",
           #     "dynamic_args": "",
           #     "dynamic_host_network": True,
           #     "dynamic_cap_add": False,
           #     "dynamic_ports": [
           #         {
           #             "containerPort": "",
           #             "hostPort": ""
           #         }
           #     ],
           #     "dynamic_volumes": [
           #         {
           #             "hostPath": "",
           #             "mountPathReadOnly": False,
           #             "mountPath": ""
           #         }
           #     ]

           # }
            "parameters": {
            }
        }
        if host_net == True:
            __kargs['request_body']['parameters'].update({"dynamic_host_network": True})

        return process_result(Request(__kargs,token).post())

    def delete_instance(self, name):
        """return dict"""
        token = self._get_token()
        __kargs = self.kargs.copy()
        __kargs["url_path"] = "/deployment/applications"
        __kargs['request_body'] = {
            "names": name
        }
        return process_result(Request(__kargs,token).delete())

    def delete_app_by_id(self, id):
        """
        id: int
        return dict"""
        token = self._get_token()
        __kargs = self.kargs.copy()
        __kargs["url_path"] = "/applications/%s" %(str(id))
        return process_result(Request(__kargs,token).delete())

    def print_registry(self, data):
        x=[[]]
        if 'mirrors' in data:
            dic_list = data['mirrors']
        else:
            dic_list = data
        for dic in dic_list:
            if "id" not in dic:
                return
            x.append([dic["id"], dic["name"], dic["public"], dic['desc']])

        tab = tt.Texttable()
        tab.set_deco(tab.HEADER|tab.BORDER|tab.VLINES)
        tab.add_rows(x)
        tab.header(["id", "name", "is_public", "description"])

        print(tab.draw())

    def get_registry(self):
        """
        id: int
        return dict"""
        token = self._get_token()
        __kargs = self.kargs.copy()
        __kargs["url_path"] = "/applications/mirrors"
        return process_result(Request(__kargs,token).get())

    def get_registry_login(self):
        """
        return dict"""
        token = self._get_token()
        __kargs = self.kargs.copy()
        __kargs["url_path"] = "/registry/login"
        return process_result(Request(__kargs,token).get())


    def instances(self):
        """
        get applications instances
        return dict"""
        token = self._get_token()
        __kargs = self.kargs.copy()
        __kargs["url_path"] = "/deployment/applications"
        return process_result(Request(__kargs,token).get())

    def instance_log(self, instance_name):
        """
        get applications instances log
        return text"""
        token = self._get_token()
        __kargs = self.kargs.copy()
        __kargs["url_path"] = "/deployment/applications/%s/conlog" %instance_name

        resp = Request(__kargs,token).get(to_dict=False)
        return resp

    def instance_history(self, instance_name):
        """
        get applications instance event logs
        return text"""
        token = self._get_token()
        __kargs = self.kargs.copy()
        __kargs["url_path"] = "/deployment/applications/%s/history" %instance_name

        resp = Request(__kargs,token).get(to_dict=False)
        process_result(json.loads(resp))
        return resp

    def print_instances(self, data, max_width=150):
        x=[[]]
        if 'items' in data:
            dic_list = data['items']
        else:
            dic_list = data
        for dic in dic_list:
            if "status" not in dic:
                return
            x.append([dic["metadata"]['name'], dic['status']['phase'], dic["metadata"]["nodename"]+"\n",\
                   dic["metadata"]["creationTimestamp"],  dic['status']['reason']+"\n"+dic['status']['message']])

        tab = tt.Texttable(max_width=max_width)
        tab.set_deco(tab.HEADER|tab.BORDER|tab.VLINES)
        tab.add_rows(x)
        #tab.set_cols_width([32, 10, 32, 15, 20])
        tab.header(["instance_name", "status", "deployed_device", "create_time", "message"])

        print(tab.draw())


    def del_instance_by_name(self, name_array):
        """
        del applications instances
        name_array: type is array[]
        return dict"""
        token = self._get_token()
        __kargs = self.kargs.copy()
        __kargs["url_path"] = "/deployment/applications"
        __kargs['request_body'] = {
                 "names": name_array,
        }
        resp = Request(__kargs,token).delete()
        for __resp in resp:
            process_result(__resp)
        return resp

    def reboot_instance_by_name(self, name):
        """
        reboot applications instances
        name: string
        return dict"""
        token = self._get_token()
        __kargs = self.kargs.copy()
        __kargs["url_path"] = "/deployment/applications/%s/reboot" %name
        return process_result(Request(__kargs,token).post())

