# -*- coding: utf-8 -*-
"""
    Buteo General Plugin
    ====================
    
    This plugin provides general information.    
        
    Copyright (c) 2009 Christian Hans
    Licensed under the terms of the GPL v2
"""
from os import uname
from time import ctime
from subprocess import Popen, PIPE

from buteo.plugins import Plugin

class GeneralPlugin(Plugin):
    
    def _loadavg(self):
        loadavg = file('/proc/loadavg').read().split()
        return '%s %s %s' % (loadavg[0], loadavg[1], loadavg[2])
        
    def _uptime(self):
        try:
            up = float(file('/proc/uptime').read().split()[0])
            return [int(up/86400), int((up/3600)%24), int((up/60)%60), int(up%60)]
        except:
            return [0, 0, 0, 0]        
    
    def get_data(self, cfg):
        users = Popen('users', shell=True, stdout=PIPE).stdout.read().split()
       
        return {
            'general': {
                'hostname': uname()[1],
                'time': ctime(),
                'uptime': self._uptime(),
                'users': ' '.join(users),
                'usercount': len(users),
                'loadavg': self._loadavg()
            }
        }
