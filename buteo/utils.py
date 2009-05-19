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

# TODO: Add these distributions:
#Arch Linux: /etc/arch-release
#Arklinux: /etc/arklinux-release
#Aurox Linux: /etc/aurox-release
#BlackCat: /etc/blackcat-release
#Cobalt: /etc/cobalt-release
#Conectiva: /etc/conectiva-release
#Debian: /etc/debian_version, /etc/debian_release (rare)
#Immunix: /etc/immunix-release
#Knoppix: knoppix_version
#Linux-PPC: /etc/linuxppc-release
#Mandriva/Mandrake Linux: /etc/mandriva-release, /etc/mandrake-release, /etc/mandakelinux-release
#MkLinux: /etc/mklinux-release
#PLD Linux: /etc/pld-release
#Red Hat: /etc/redhat-release, /etc/redhat_version (rare)
#Slackware: /etc/slackware-version, /etc/slackware-release (rare)
#SME Server (Formerly E-Smith): /etc/e-smith-release
#Solaris SPARC: /etc/release
#Sun JDS: /etc/sun-release
#SUSE Linux ES9: /etc/sles-release
#Tiny Sofa: /etc/tinysofa-release
#TurboLinux: /etc/turbolinux-release
#UltraPenguin: /etc/ultrapenguin-release
#UnitedLinux: /etc/UnitedLinux-release (covers SUSE SLES8)
#VA-Linux/RH-VALE: /etc/va-release

distributions = {
	'Arch Linux': '/etc/arch-release',
	'Debian': '/etc/debian_version',
	'Fedora': '/etc/fedora-release',
	'Gentoo': '/etc/gentoo-release',
	'LinuxFromScratch': '/etc/lfs-release',
	'Mandrake': '/etc/mandrake-release',
	'Mandrivia': '/etc/mandriva-release',
	'Red Hat': '/etc/redhat-release',
	'Slackware': '/etc/slackware-release',
	'SuSe': '/etc/SuSE-release',
	'SuSe (Novell)': '/etc/novell-release',
	'Novell Linux Desktop': '/etc/nld-release',
	'Ubuntu': '/etc/lsb-release',
	'Yellow Dog': '/etc/yellowdog-release',
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
        print ' * ERROR: Failed to parse the configuration file. Using default options now.'
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
