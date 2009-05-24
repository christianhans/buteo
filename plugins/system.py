# -*- coding: utf-8 -*-
"""
    Buteo System Plugin
    ====================
    
    This plugin provides system information.    
        
    Copyright (c) 2009 Christian Hans
    Licensed under the terms of the GPL v2
"""
from os import path, uname
from buteo.plugins import Plugin

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

class SystemPlugin(Plugin):

    def _distribution(self):	
	    for distribution, dpath in distributions.iteritems():
		    if path.exists(dpath):
			    return distribution

    def get_data(self, cfg):
        un = uname()
        
        return {
            'system': {
                'system': un[0],
                'distribution': self._distribution(),
                'kernel_version': un[2],
                'kernel_release': un[3],
                'architecture': un[4]
            }
        }
