#!/usr/local/bin/python
# -*- coding: utf-8 -*-
#Copyright (c) 2011 - Santiago Zavala
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.

import logging
import hashlib
import keys
import prefetch
import helper
import random

from google.appengine.api import mail
from google.appengine.api import memcache
from google.appengine.ext import webapp, db
from google.appengine.ext.webapp import util, template
from google.appengine.ext.webapp.util import run_wsgi_app

from datetime import datetime, date, timedelta
from gaesessions import get_current_session
from django.utils import simplejson

from libs import PyRSS2Gen
from models import User, Post, Comment, Vote, Notification, Ticket


#register the desdetiempo filter to print time since in spanish
template.register_template_library('CustomFilters')

class Handler(webapp.RequestHandler):
  def get(self, post_id):
    session = get_current_session()
    if session.has_key('user'):
      user = session['user']
      try:
        post = db.get(helper.parse_post_id(post_id))
        if post.can_edit():
          self.response.out.write(template.render('templates/edit-post.html', locals()))
        else:
          self.redirect('/')
      except db.BadKeyError:
        self.redirect('/')
    else:
      self.redirect('/')

  def post(self, post_id):
    session = get_current_session()
    title = helper.sanitizeHtml(self.request.get('title'))
    message = helper.sanitizeHtml(self.request.get('message'))

    if session.has_key('user'):
      user = session['user']
      try:
        post = db.get(helper.parse_post_id(post_id))
        if post.can_edit():
          if len(title) > 0:
            post.title = title
          if post.message is not None and message is not None:
            post.message = message
          post.edited = True
          post.put()
          self.redirect('/noticia/' + str(post.key()))
        else:
          self.redirect('/')
      except db.BadKeyError:
        self.redirect('/')  
    else:
      self.redirect('/')



