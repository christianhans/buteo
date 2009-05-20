# -*- coding: utf-8 -*-
"""
    buteo.application
    =================
    
    This module implements the WSGI application.
    
    Copyright (c) 2009 Christian Hans
    Licensed under the terms of the GPL v2
"""
from os import path, uname
from sys import version
from time import time, ctime
from subprocess import Popen, PIPE

from werkzeug import Request, Response
from werkzeug.exceptions import HTTPException
from werkzeug import __version__ as werkzeug_version

from jinja2 import Environment, FileSystemLoader, Template
from jinja2 import __version__ as jinja_version

from buteo import utils
from buteo import plugins

# TODO: Improve handling of non-existent options for plugins
# TODO: Get more detailed distribution data from /etc/*-release
# TODO: Make it bullet-proof (try...except where required)
# TODO: Percentage bars for memory

# Future plans:
# - Configuration through a web interface
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
        users = Popen('users', shell=True, stdout=PIPE).stdout.read().split()
        un = uname()
        
        self.var_dict = {
            'refresh_interval': self.cfg['refresh_interval'],
                 
            'hostname': un[1],
            'time': ctime(),
            'uptime': utils.get_uptime(),
            'users': ' '.join(users),
            'usercount': len(users),
            'loadavg': utils.get_loadavg(),

            'system': un[0],
            'distribution': utils.get_distribution(),
            'kernel_version': un[2],
            'kernel_release': un[3],
            'architecture': un[4],				
            
            'mem': utils.get_meminfo(),	    

            'filesystems': utils.get_filesystems(),	    

            'python_version': version,
            'werkzeug_version': werkzeug_version,
            'jinja_version': jinja_version,
            'buteo_version': self.version,
             
            'exectime': round(time()-self.starttime, 4)
        }
        
        # add data from plugins
        if self.enabled_plugins != []:
            for plugin in plugins.get_plugins():
                try:
                    data = plugin.get_data(self.cfg)
                except Exception as inst:
                    print ' * ERROR: %s. Skipping this plugin.' % inst
                    continue
                
                for key in data:
                    if not key in self.var_dict:
                        self.var_dict[key] = data[key]
              
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
