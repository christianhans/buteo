# -*- coding: utf-8 -*-
"""
    buteo.plugins
    =============
    
    Buteo plugin system.
    
    Copyright (c) 2009 Christian Hans
    Licensed under the terms of the GPL v2
"""
from sys import path

_instances = {}

class Plugin(object):
    pass

def load_plugins(plugins):
    for plugin in plugins:
        try:
            __import__(plugin, None, None, [''])
        except ImportError:
            print ' * ERROR: No plugin named %s.' % plugin

def init_plugin_system(cfg):
    if not cfg['plugin_path'] in path:
        path.insert(0, cfg['plugin_path'])
    load_plugins(cfg['plugins'])    

def get_plugins():
    result = []
    for plugin in Plugin.__subclasses__():
        if not plugin in _instances:
            _instances[plugin] = plugin()
        result.append(_instances[plugin])
    return result
