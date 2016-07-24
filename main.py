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


import webapp2
import jinja2

from google.appengine.ext import db


# commands to call the directory where the files html, js are.
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


## funciones 
letters_dic = {'A':1, 'B':2, 'C':3, 'D':4, 'E':5, 'F':6, 'G':7, 'H':8, 'I':9,
                   'J':1, 'K':2, 'L':3, 'M':4, 'N':5, 'O':6, 'P':7, 'Q':8, 'R':9,
                   'S':1, 'T':2, 'U':3, 'V':4, 'W':5, 'X':6, 'Y':7, 'Z':8,
                   '1':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '0':0}

def format_string(mystring):
    new_string = mystring.upper()
    new_string = new_string.replace(" ", "")
    new_string = new_string.replace("-", "")
    return new_string

def format_string_num(mystring):
    new_string = mystring.replace(" ", "")
    return new_string


def result_text(mylist):
    numberOfText = []
    frecuency_dico = {}
    for i in mylist:
        numberOfText.append(letters_dic[i])
    for j in range(1, 10):
        frecuency_dico[j] = numberOfText.count(j)
    return frecuency_dico, numberOfText

def suma_digits(lista):
    suma = sum(lista)
    new_lista = list(map(int, str(suma)))
    if len(new_lista) == 1:
        return new_lista[0]
    else :
        return suma_digits(new_lista)   

def result_number(mylist):
    frecuency_num_dico = {}
    for j in range(1, 10):
        frecuency_num_dico[j] = mylist.count(j)
    return frecuency_num_dico


######  

class Rot13(BaseHandler):
    def get(self):
        self.render('rot13-form.html')

    def post(self):
        rot13 = ''
        text = self.request.get('text')
        if text:
            listaString = list(format_string(text))
            rot13 = suma_digits(result_text(listaString))

        self.render('rot13-form.html', text = rot13)


class MainDisplay(BaseHandler):
    def get(self):
        self.render('index.html')

    def post(self):
        text = self.request.get('name')
        num = self.request.get('number')
        listaStringName = list(format_string(text))
        frecuencyName, nameNumbersList = result_text(listaStringName)
        listaStringNum = list(format_string_num(num))
        frecuencyNum, numNumbersList = result_text(listaStringNum)
        #numberList = result_number(listaStringNum) no se si se va a usar, la salida es un dict
        resultName = suma_digits(nameNumbersList) 
        resultNum = suma_digits(numNumbersList)

    	self.render('welcome.html', sum_name = str(resultName), sum_brnum = str(resultNum),
                    name_list_num = str(nameNumbersList), frec_num = str(frecuencyName), test_dict = frecuencyName, num_dict = frecuencyNum, name = text, number = num )


        #self.render('index.html', sum_name = str(resultName), sum_brnum = str(resultNum),
        #            name_list_num = str(nameNumbersList), frec_num = str(frecuencyName), test_dict = frecuencyName, num_dict = frecuencyNum, name = text, number = num )

        #self.render('index.html', sum_name = str(resultName), sum_brnum = str(resultNum))



    	#self.redirect('/unit2/welcome?username=' + username)
    	#self.redirect('/result?name=' + str(result))                                    

class Result(BaseHandler):
    def get(self):
        name = 'prueba'
        self.render('welcome.html')

     

app = webapp2.WSGIApplication([
	('/rot13', Rot13),
    ('/', MainDisplay),
    ('/result', Result)], 
    debug=True)
