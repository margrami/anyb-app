#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import re
import random
import hashlib
import hmac
import string
import json
import logging
import time


import webapp2
import jinja2

from google.appengine.ext import db
from google.appengine.api import urlfetch


# Commands to access the directory where the files html, js are.

template_dir = os.path.join(os.path.dirname(__file__))
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                              autoescape = True)


def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class BaseHandler(webapp2.RequestHandler):
    def render(self, template, **kw):
        self.response.out.write(render_str(template, **kw))

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def set_cookie(self, name, val):
        self.response.headers.add_header('Set-Cookie',
                                         '%s=%s; Path=/' % (name, val))


#### Funciones 

def data_payload(url, obj,  offset, count):
    return str(str(url) + '/' + str(obj) + '?'+ 'offset='+ str(offset) + '&count=' + str(count))

def connexion_obj_data(url):
	url1 = data_payload(url, 'adi/data.json', 0, 16)
	res  = urlfetch.fetch(url1)
	adi_list = json.loads(res.content) 
	return {x: adi_list[x] for x in range(0, 16)}

def metadata_request(url, offset, count):
	url = data_payload(url, 'adi/metadata.json', offset, count)
	res = urlfetch.fetch(url)
	return json.loads(res.content)

def info_request(url):
    ip_OK = False
    obj = 'module/info.json'
    url = str(url + '/' + obj)
    res = urlfetch.fetch(url)
    if res:
        ip_OK = True
    return json.loads(res.content) # no olvidar anadir una verificacion !


#### Update section 

def data_payload_update(url, a, b):
	return str(url + '?' + 'inst='+ a + '&value='  + b)

def request_update_mod(target, instance, value):
    if len(value) == 1:
        val = '0' + value + '000000'
    if len(value) == 2:
        val =  value + '000000'
    if len(value) == 7:
        val = '0' + value
    if len(value) == 8:
        val = value
    url = data_payload_update(target + '/adi/update.json', instance, val)
    res = urlfetch.fetch(url)
    return json.loads(res.content)



######  


class MainDisplay(BaseHandler):
    the_url = ''
    def get(self):
        self.the_url = self.request.get('url')
        k = info_request(self.the_url)
        self.render('index2.html', over_outcome = k, dirr = self.the_url )

    def post(self):
        inst = self.request.get('inst')
        val = self.request.get('val')
        result_error = request_update_mod(self.request.get('url'), inst, val) # send update request to device, get error
        k = info_request(self.request.get('url'))
       
        # display
        self.render('index2.html', 
                     up_outcome = result_error['result'], last_request = 'Instance:' + inst + " " + 'Value:' + val, 
                     dirr = self.request.get('url'), over_outcome = k)

    

class FirstDisplay(BaseHandler):
    URL = ''
    def get(self):
        self.render('index1.html')

    def post(self):
        IP = self.request.get('ip')
        port = self.request.get('port')
        self.URL = str('http://' + IP + ':' + port)
        self.set_cookie('connex_url', str(self.URL)) #create the cookie
        self.redirect('/update?url=' + self.URL)



class Result(BaseHandler):
    def get(self):
        cookieValue = self.request.cookies.get('connex_url')
        list_name = metadata_request(cookieValue, 0, 16)
        list_value = connexion_obj_data(cookieValue)
        k = {x: [list_name[x]["instance"], list_name[x]["name"], list_name[x]["datatype"],list_name[x]["access"], list_value[x]] for x in range (0, 16)}
        self.render('resultspage.html', ADI_dict = k)





app = webapp2.WSGIApplication([
    ('/', FirstDisplay),
    ('/result', Result),
    ('/update', MainDisplay)], 
    debug=True)
