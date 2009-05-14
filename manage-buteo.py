#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Buteo System Monitor
    ====================
    
    A simple web-based system monitor written in Python. 
    Displays information about your system on a single webpage.
    
    Run this management script with the -h option to display usage information.
    
    Copyright (c) 2009 Christian Hans
    Licensed under the terms of the GPL v2
"""
import sys
from os import path
from werkzeug import script

# own runserver function, since additional command line arguments are required
def _runserver(config='', templates='', hostname='localhost', port=5000, use_reloader=False, use_debugger=False,
                use_evalex=True, threaded=False, processes=1, static_files=None, extra_files=None):
    def action(config=('c', config), templates=('t', templates), hostname=('h', hostname), port=('p', port),
               reloader=use_reloader, debugger=use_debugger,
               evalex=use_evalex, threaded=threaded, processes=processes):
        """Start a new development server."""    
        
        # get path of configuration file
        cfg_file = None
        if config != '':
            config = path.realpath(path.expanduser(config))
            if path.exists(config):
                cfg_file = config
            else:
                print ' * ERROR: The specified configuration file wasn\'t found'
                sys.exit(1)
        else:               
            if path.exists(path.join(path.dirname(__file__), 'buteo.cfg')):
                cfg_file = path.abspath(path.join(path.dirname(__file__), 'buteo.cfg'))
            elif path.exists('/etc/buteo.cfg'):
                cfg_file = '/etc/buteo.cfg'
            else:
                print ' * ERROR: No configuration file was found.'
                print ' * Specify a configuration file with the -c option.'           

        # get paths of templates
        template_paths = []        
        if templates != '':
            templates = path.realpath(path.expanduser(templates))
            if path.exists(templates):
                template_paths.append(templates)
            else:
                print ' * ERROR: The specified templates path wasn\'t found'
                sys.exit(1)
        else:        
            if path.exists(path.join(path.dirname(__file__), 'templates')):
                template_paths.append(path.abspath(path.join(path.dirname(__file__), 'templates')))
            if path.exists('/usr/share/buteo/templates'):
                template_paths.append('/usr/share/buteo/templates')
            
        if template_paths == []:
            print ' * ERROR: No template files have been found. Specify a template path with the -t option.'
            sys.exit(1)
         
        from buteo import Buteo
        from werkzeug.serving import run_simple
        app = Buteo(cfg_file, template_paths)
        run_simple(hostname, port, app, reloader, debugger, evalex,
                   extra_files, 1, threaded, processes, static_files)
    return action

action_runserver = _runserver()
action_shell = script.make_shell(lambda: {'app': make_app()})

if __name__ == '__main__':       
    script.run()   
