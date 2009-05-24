# -*- coding: utf-8 -*-
"""
    buteo.application
    =================
    
    This module implements the WSGI application.
    
    Copyright (c) 2009 Christian Hans
    Licensed under the terms of the GPL v2
"""
from os import path
from sys import version
from time import time

from werkzeug import Request, Response
from werkzeug.exceptions import HTTPException
from werkzeug import __version__ as werkzeug_version

from jinja2 import Environment, FileSystemLoader, Template
from jinja2 import __version__ as jinja_version

from buteo import utils
from buteo import plugins

# TODO: Add ability for plugins to add a version string
# TODO. Perhaps remove some math operations from templates in order to improve performance
# TODO: Improve handling of plugin exceptions (completely leave out plugin if a exception occured)
# TODO: Improve handling of non-existent options for plugins
# TODO: Make it bullet-proof (try...except where required)
# TODO: Percentage bars for memory
# TODO: Improve layout of percentage bars

# Future plans:
# - Configuration through a web interface
# - Get more detailed distribution data from /etc/*-release
# - Hardware information plugin
# - XML output (perhaps with a template)
# - Process list plugin
# - Services status plugin
# - Quota information plugin
# - Localization
# - Documentation

class Buteo(object):

    def __init__(self, cfg_file, plugin_path, template_path):             
        # get version string
        from buteo import __version__
        self.version = __version__
        
        # Get configuration
        if cfg_file:
            print ' * Using %s as configuration file.' % cfg_file             

        self.cfg = utils.get_cfg(cfg_file,
            {'plugins': '', 'auth': 0, 'template': 'default', 'template_autoreload': 0, 'refresh_interval': None, 'vnstat_ifaces': ''})
        
        # Load Plugins
        self.enabled_plugins = []

        if plugin_path and path.exists(plugin_path):
            print ' * Using %s as plugin directory.' % plugin_path
            self.enabled_plugins = self.cfg['plugins'].split()
            plugins.init_plugin_system({'plugin_path': plugin_path, 'plugins': self.enabled_plugins})            
        else:
            print ' * WARNING: Plugin system is diabled, since no plugin directory has been found.'
              
          
        # Get authentication data               
        self.users = {}
        self.realm = 'login required' 
      
        if int(self.cfg['auth']) == 1:
            users = self.cfg['auth_users'].split()
            passwords = self.cfg['auth_passwd'].split()
          
            for i, u in enumerate(users):
                try:
                    if passwords[i]: self.users[u.strip()] = passwords[i].strip()
                except:
                    pass                    
        
        # Load template engine
        self.tmplenv = Environment(loader=FileSystemLoader(template_path), auto_reload=self.cfg['template_autoreload'])
        self.template = self.tmplenv.get_template('%s.html' % self.cfg['template'])
        
        if self.template.filename:
            print ' * Using %s as template file.' % self.template.filename

    def check_auth(self, username, password):
        return username in self.users and self.users[username] == password

    def auth_required(self, request):
        return Response('401 Unauthorized', 401,
                        {'WWW-Authenticate': 'Basic realm="%s"' % self.realm})

    def dispatch_request(self, request):
        # Process variables        
        self.var_dict = {
            'refresh_interval': self.cfg['refresh_interval'],
                        
            'python_version': version,
            'werkzeug_version': werkzeug_version,
            'jinja_version': jinja_version,
            'buteo_version': self.version
        }

        # add data from plugins
        if self.enabled_plugins != []:
            for plugin in plugins.get_plugins():
                try:
                    data = plugin.get_data(self.cfg)
                except Exception as inst:
                    print ' * ERROR: %s. Skipping plugin %r.' % (inst, plugin.__class__.__name__)
                    continue
                
                for key in data:
                    if not key in self.var_dict:
                        self.var_dict[key] = data[key]
                        
        self.var_dict['exectime'] = round(time()-self.starttime, 4)                
              
        try:
            response = Response(mimetype='text/html')                           
            response.data = self.template.render(self.var_dict)            
            return response
            
        except HTTPException, e:
            return e
            
    def __call__(self, environ, start_response):
        self.starttime = time()
        request = Request(environ)
        
        if int(self.cfg['auth']) == 1:
            auth = request.authorization
            if not auth or not self.check_auth(auth.username, auth.password):
                response = self.auth_required(request)
            else:
                response = self.dispatch_request(request)
        else:
            response = self.dispatch_request(request)
        return response(environ, start_response)            
