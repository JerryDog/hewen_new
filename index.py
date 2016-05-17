#!/usr/bin/python
# -*- coding: utf-8 -*-
 
import web 
 
urls = ("/.*", "hello")
 
class hello:
    def GET(self):
        return 'Hello, world!'
 
app = web.application(urls, globals())
application = app.wsgifunc()
