# -*- coding: utf-8 -*-
"""
    Buteo Memory Plugin
    ====================
    
    This plugin provides memory information.    
        
    Copyright (c) 2009 Christian Hans
    Licensed under the terms of the GPL v2
"""
from buteo.plugins import Plugin

class MemoryPlugin(Plugin):

    def get_data(self, cfg):
        mem = {}
        for i in file('/proc/meminfo').readlines():
            try:
                isplit = i.split()
                mem[isplit[0].rstrip(':').lower()] = int(isplit[1])
            except:
                pass

        return {'memory': mem}
