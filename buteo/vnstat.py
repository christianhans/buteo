# -*- coding: utf-8 -*-
"""
    buteo.vnstat
    ============
    
    This module provides functions to get vnStat data.
    
    Copyright (c) 2009 Christian Hans
    Licensed under the terms of the GPL v2
"""
from subprocess import Popen, PIPE

def _vnstat(iface=""):
    # All values are in kB
    data = {'totalrx': 0, 'totaltx': 0, 'todayrx': 0, 'todaytx': 0, 'monthrx': 0, 'monthtx': 0}
    hours = []
    
    if iface:
        out = Popen('vnstat --dumpdb -i %s' % iface, shell=True, stdout=PIPE).stdout.readlines()
    else:
        out = Popen('vnstat --dumpdb', shell=True, stdout=PIPE).stdout.readlines()

    for l in out:
        if 'Not enough data available yet' in l:
            return {}
                    
        l = l.rstrip('\n')  
        s = l.split(';')        

        if s[0] == 'interface':
            data['interface'] = s[1]
        if s[0] == 'nick':
            data['nick'] = s[1]            
        if s[0] == 'created':
            data['created'] = s[1]
        if s[0] == 'updated':
            data['updated'] = s[1]
        if s[0] == 'active':
            data['active'] = s[1]                
        elif s[0] == 'totalrx':
            data['totalrx'] += int(s[1])*1024
        elif s[0] == 'totaltx':
            data['totaltx'] += int(s[1])*1024
        elif s[0] == 'totalrxk':
            data['totalrx'] += int(s[1])
        elif s[0] == 'totaltxk':
            data['totaltx'] += int(s[1])
        elif s[0] == 'd' and s[1] == '0':
            data['todayrx'] = (int(s[3])*1024) + int(s[5])
            data['todaytx'] = (int(s[4])*1024) + int(s[6])
        elif s[0] == 'm' and s[1] == '0':
            data['monthrx'] = (int(s[3])*1024) + int(s[5])
            data['monthtx'] = (int(s[4])*1024) + int(s[6])
                  
    return data      

def get_vnstat(ifaces=[]):
    data = []
    
    if ifaces:
        for iface in ifaces:
            vnstatdata = _vnstat(iface)
            if vnstatdata:
                data.append(vnstatdata)
    else:
        data = _vnstat()
    
    return data
