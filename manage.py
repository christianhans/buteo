#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Buteo System Monitor
    ====================
    
    A simple web-based system monitor written in Python. 
    Displays information about your system on a single webpage.
    
    Run this manage script without command line arguments to display usage information.
    
    Copyright (c) 2009 Christian Hans
    Licensed under the terms of the GPL v2
"""
from werkzeug import script
from os import path

def make_app():
    from buteo import Buteo
    return Buteo(path.join(path.abspath(path.dirname(__file__)), 'buteo.cfg'))

action_runserver = script.make_runserver(make_app)
action_shell = script.make_shell(lambda: {'app': make_app()})

if __name__ == '__main__':    
    script.run()
