#####################################
#
# Copyright 2018 NXP
#
#####################################

#!/usr/bin/env python

"""HTTP/HTTPs Client library"""
import json
import logging
import sys

try:
    # Python 3
    import urllib.request as urllib
    from urllib.parse import urlencode
    from urllib.error import HTTPError
except:
    # Python 2
    import urllib2 as urllib
    from urllib2 import HTTPError
    from urllib import urlencode

log = logging.getLogger("c")

class Resp(object):

    def __init__(self, resp):
        """init """
        self._body = resp.read()
        log.debug("Response: %s", self._body)

    @property
    def body(self):
        # python3
        try:
            return self._body.decode('utf-8')
        # Python 2
        except:
            return self._body


class Client(object):

    def __init__(self,
                 host,
                 request_headers=None,
                 version=None,
                 url_path=None):
        """
        :param host: Base URL for the api.
        :type host:  string
        :param request_headers: A dictionary
        :type request_headers: dictionary
        :param version: The version number of the API.
        :type version: integer
        :param url_path: A list of the url path segments
        :type url_path: list of strings
        """
        self.host = host
        self.request_headers = request_headers or {}
        self.version = version
        # _url_path keeps track of the dynamically built url
        self._url_path = url_path or []
        # These are the supported HTTP verbs
        self.methods = ['put', 'get', 'patch', 'post', 'put', 'delete']


    def _make_url(self, query_params):
        """Make the URL according to parameters

        :param query_params: A dictionary of all the query parameters
        :type query_params: dictionary
        :return: string
        """
        url = self._url_path

        if query_params:
            url_values = urlencode(sorted(query_params.items()), True)
            url = '{0}?{1}'.format(url, url_values)

        if self.version:
            url =  '{0}/{1}{2}'.format(self.host, str(self.version), url)
        else:
            url = self.host + url

        return url


    def _make_client(self, name=None):
        """Make a new Client object

        :param name: url to build
        :type name: string
        :return: A Client object
        """
        url_path = self._url_path
        return Client(host=self.host,
                      version=self.version,
                      request_headers=self.request_headers,
                      url_path=url_path)

    def _make_request(self, opener, request, data):
        """Make the API call and return the response. This is separated into
           it's own function, so we can mock it easily for testing.

        :param opener:
        :type opener:
        :param request: url payload to request
        :type request: urllib.Request object
        :return: urllib response
        """
        log.debug("curl -X %s %s -H %s -d %s", request.get_method(), request.get_full_url(), request.header_items(), str(data))
        try:
            return opener.open(request)
        except HTTPError as e:
            print "HttpError %s" %str(e)
            raise Exception(e)
        except Exception as e:
            raise Exception(e)


    def __getattr__(self, name):
        """
        :param name: Name of the url segment or method call
        :type name: string or integer if name == version
        :return: mixed
        """
        if name in self.methods:
            method = name.upper()
            def http_request(*_make_client, **kwargs):
                if 'request_headers' in kwargs:
                    self.request_headers.update(kwargs['request_headers'])
                if 'request_body' not in kwargs or kwargs['request_body'] == None:
                    data = None
                else:

                    # Don't serialize to a JSON formatted str
                    # if we don't have a JSON Content-Type
                    if 'Content-Type' in self.request_headers:
                        if self.request_headers['Content-Type'] != 'application/json':
                            try:
                                data = kwargs['request_body'].encode('utf-8')
                            except:
                                data = kwargs['request_body']
                        else:
                            try:
                                data = json.dumps(kwargs['request_body']).encode('utf-8')
                            except:
                                data = json.dumps(kwargs['request_body'])
                    else:
                        try:
                            data = json.dumps(kwargs['request_body']).encode('utf-8')
                        except:
                            data = json.dumps(kwargs['request_body'])

                if 'query_params' in kwargs:
                    params = kwargs['query_params']
                else:
                    params = None

                opener = urllib.build_opener()
                request = urllib.Request(self._make_url(params), data=data)
                if self.request_headers:
                    for key, value in self.request_headers.items():
                        request.add_header(key, value)
                request.add_header('Content-Type', 'application/json')
                request.get_method = lambda: method
                return Resp(self._make_request(opener, request, data))
            return http_request
        else:
            return self._make_client(name)


