# -*- coding: utf-8 -*-
"""
    buteo.utils
    ===========
    
    Some utils for buteo.
    
    Copyright (c) 2009 Christian Hans
    Licensed under the terms of the GPL v2
"""

def get_cfg(path, default_options={}):
    options = {}
    try:
        for i, line in enumerate(file(path)):
            line = line.rstrip("\r\n").lstrip()
            if not line or line.startswith(';') or line.startswith('#'):
                continue
            if '=' in line:
                name, value = line.split('=', 1)
                options[name.rstrip().lower()] = value.strip()
    except:
        print ' * ERROR: Failed to parse the configuration file. Using default options now.'
        pass
    
    # Make sure all default config keys are defined
    for key in default_options:
        if not key in options:
            options[key] = default_options[key]
        
    return options
