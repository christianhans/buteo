# -*- coding: utf-8 -*-
"""
    Buteo System Plugin
    ====================
    
    This plugin provides system information.    
        
    Copyright (c) 2010 Christian Hans
    Licensed under the terms of the GPL v2
"""
from buteo.plugins import Plugin
import platform

class SystemPlugin(Plugin):
    
    def get_data(self, cfg):
        return {
            'system': {
                'system': platform.system(),
                'distribution':  " ".join(platform.linux_distribution()),
                'platform': platform.platform(),
                'kernel_release': platform.release(),
                'kernel_version': platform.version(),
                'architecture': " ".join(platform.architecture()),
                'machine': platform.machine()
            }
        }
