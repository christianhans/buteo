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

# TODO: Get more detailed distribution data from /etc/*-release
# TODO: Make it bullet-proof (try...except where required)
# TODO: Percentage bars for memory

# Future plans:
# - Configuration through a web interface
# - Easy plugin system (put vnstat and network in external plugins)
# - Hardware information (external plugin)
# - XML output (perhaps with a template)
# - Process list
# - Services status
# - Quota information
# - Localization
# - Documentation

class Buteo(object):

    def __init__(self, cfg_file, template_path):             
        from buteo import __version__
        self.version = __version__
        
        if cfg_file:
            print ' * Using %s as configuration file.' % cfg_file  
        
        self.cfg = utils.get_cfg(cfg_file,
            {'auth': 0, 'template': 'default', 'template_autoreload': 0, 'refresh_interval': None, 'network': 1, 'vnstat': 0, 'vnstat_ifaces': ''})
       
        self.users = {}
        self.realm = 'login required' 
      
        if int(self.cfg['auth']) == 1:
            users = self.cfg['auth_users'].split(',')
            passwords = self.cfg['auth_passwd'].split(',')
          
            for i, u in enumerate(users):
                try:
                    if passwords[i]: self.users[u.strip()] = passwords[i].strip()
                except:
                    pass                    
        
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
        if int(self.cfg['vnstat']) == 1:
            from  buteo.vnstat import get_vnstat
            vnstatdata = get_vnstat(self.cfg['vnstat_ifaces'].split(','))
        else:
            vnstatdata = {}
            
        if int(self.cfg['network']) == 1:
            from buteo.network import get_ifaces
            networkdata = get_ifaces()
        else:
            networkdata = {}
           
        users = Popen('users', shell=True, stdout=PIPE).stdout.read().split()
        un = uname()
   
        try:
            response = Response(mimetype='text/html')
                           
            response.data = self.template.render(
                refresh_interval = self.cfg['refresh_interval'],
                     
                hostname = un[1],
		        time = ctime(),
		        uptime = utils.get_uptime(),
		        users = ' '.join(users),
		        usercount = len(users),
		        loadavg = utils.get_loadavg(),
		
		        system = un[0],
		        distribution = utils.get_distribution(),
		        kernel_version = un[2],
		        kernel_release = un[3],
		        architecture = un[4],				
		        
                mem = utils.get_meminfo(),	    
		
		        filesystems = utils.get_filesystems(),		    
		        ifaces = networkdata,		    
		        vnstat = vnstatdata,	
		
		        python_version = version,
		        werkzeug_version = werkzeug_version,
		        jinja_version = jinja_version,
		        buteo_version = self.version,
		        
		        exectime = round(time()-self.starttime, 4)
            )
            
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
