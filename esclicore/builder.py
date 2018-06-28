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

class Builder(object):
    """cli builder query and management class"""

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
            self.kargs["url_path"] = "/builder"

    def _get_token(self):
        """return token or None
        Get the user's token
        """
        return user.get_token()

    def get_environments(self):
        """Get all of the build environment list
        """
        token = self._get_token()
        __kargs = self.kargs.copy()
        __kargs["url_path"] += "/environments"
        return process_result(Request(__kargs,token).get())

    def get_repositories(self):
        """Get all of the AWS codecommit repository list
        """
        token = self._get_token()
        __kargs = self.kargs.copy()
        __kargs["url_path"] += "/repositories"
        return process_result(Request(__kargs,token).get())

    def get_projects(self):
        """Get all of the project list
        """
        token = self._get_token()
        __kargs = self.kargs.copy()
        __kargs["url_path"] += "/projects"
        return process_result(Request(__kargs,token).get())

    def create_project(self, name, image, source, description="", \
            pollForSourceChanges="false", timeoutInMinutes=40):
        """Create a new project
        """
        token = self._get_token()
        __kargs = self.kargs.copy()
        __kargs["url_path"] += "/projects"
        __kargs["request_body"] = {
            "name": name,
            "image": image,
            "source": source,
            "description": description,
            "pollForSourceChanges": pollForSourceChanges,
            "timeoutInMinutes": timeoutInMinutes
        }
        return process_result(Request(__kargs,token).post())

    def update_project(self, name, image, source, description="", \
            pollForSourceChanges="false", timeoutInMinutes=40):
        """Update a project
        """
        token = self._get_token()
        __kargs = self.kargs.copy()
        __kargs["url_path"] += "/projects/%s" % name
        __kargs["request_body"] = {
            "name": name,
            "image": image,
            "source": source,
            "description": description,
            "pollForSourceChanges": pollForSourceChanges,
            "timeoutInMinutes": timeoutInMinutes
        }
        return process_result(Request(__kargs,token).put())

    def query_project(self, name):
        """Query a project
        """
        token = self._get_token()
        __kargs = self.kargs.copy()
        __kargs["url_path"] += "/projects/%s" % name
        return process_result(Request(__kargs,token).get())

    def start_project_build(self, name):
        """Start a build for project
        """
        token = self._get_token()
        __kargs = self.kargs.copy()
        __kargs["url_path"] += "/projects/%s" % name
        __kargs["request_body"] = {
            "action": "start"
        }
        return process_result(Request(__kargs,token).post())

    def delete_project(self, name):
        """Delete a project
        """
        token = self._get_token()
        __kargs = self.kargs.copy()
        __kargs["url_path"] += "/projects/%s" % name
        return process_result(Request(__kargs,token).delete())

