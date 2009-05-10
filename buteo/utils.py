# -*- coding: utf-8 -*-
"""
    buteo.utils
    ===========
    
    Some utils for buteo.
    
    Copyright (c) 2009 Christian Hans
    Licensed under the terms of the GPL v2
"""
from os import path
from subprocess import Popen, PIPE

distributions = {
	'Ubuntu': '/etc/lsb-release',
	'Debian': '/etc/debian_version',
	'SuSe': '/etc/SuSE-release',
	'Mandrake': '/etc/mandrake-release',
	'Gentoo': '/etc/gentoo-release',
	'RedHat': '/etc/redhat-release',
	'Fedora': '/etc/fedora-release',
	'Slackware': '/etc/slackware-release',
	'Arch': '/etc/arch-release',
	'LinuxFromScratch': '/etc/lfs-release',
}

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
        pass
    
    # Make sure all default config keys are defined
    for key in default_options:
        if not key in options:
            options[key] = default_options[key]
        
    return options

def get_uptime():
    try:
        up = float(file('/proc/uptime').read().split()[0])
        return [int(up/86400), int((up/3600)%24), int((up/60)%60), int(up%60)]
    except:
        return [0, 0, 0, 0]
  
def get_loadavg():
    loadavg = file('/proc/loadavg').read().split()
    return '%s %s %s' % (loadavg[0], loadavg[1], loadavg[2])
    
def get_meminfo():
    mem = {}
    for i in file('/proc/meminfo').readlines():
        try:
            isplit = i.split()
            mem[isplit[0].rstrip(':').lower()] = int(isplit[1])            
        except:
	        pass	        
    return mem

def get_filesystems():	
	out = Popen('df -h -T', shell=True, stdout=PIPE).stdout.readlines()
	out.remove(out[0])
	for i in xrange(len(out)):
		out[i] = out[i].split()
		
	return out

def get_distribution():	
	for distribution, dpath in distributions.iteritems():
		if path.exists(dpath):
			return distribution
