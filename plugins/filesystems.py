# -*- coding: utf-8 -*-
"""
    Buteo Filesystems Plugin
    ====================
    
    This plugin provides a list of filesystems.    
        
    Copyright (c) 2009 Christian Hans
    Licensed under the terms of the GPL v2
"""
from subprocess import Popen, PIPE
from buteo.plugins import Plugin

class FilesystemsPlugin(Plugin):

    def get_data(self, cfg):
        out = Popen('df -h -T', shell=True, stdout=PIPE).stdout.readlines()
        out.remove(out[0])
        for i in xrange(len(out)):
            out[i] = out[i].split()

        return {'filesystems': out}
