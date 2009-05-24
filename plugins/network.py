# -*- coding: utf-8 -*-
"""
    Buteo Network Plugin
    ====================
    
    This plugin provides network information.    
        
    Copyright (c) 2009 Christian Hans
    Licensed under the terms of the GPL v2
"""
from socket import socket, SOCK_DGRAM, AF_INET, inet_ntoa
from fcntl import ioctl
from struct import pack, unpack
from array import array
from os import uname

from buteo.plugins import Plugin

class NetworkPlugin(Plugin):

    # helper function for _ifaces()
    def _ifinfo(self, sock, addr, ifname):
        iface = pack('256s', ifname[:15])
        info  = ioctl(sock.fileno(), addr, iface)
        if addr == 0x8927:
            hwaddr = []
            for char in info[18:24]:
                hwaddr.append(hex(ord(char))[2:])
            return ':'.join(hwaddr)
        else:
            return inet_ntoa(info[20:24])
      
    # returns a list with dictionaries including network interface data
    # like ifconfig (for 32bit and 64bit Linux kernels)
    def _ifaces(self):
        max_possible = 128  # arbitrary. raise if needed.
        bytes = max_possible * 32
        s = socket(AF_INET, SOCK_DGRAM)
        names = array('B', '\0' * bytes)
        outbytes = unpack('iL', ioctl(
            s.fileno(),
            0x8912,  # SIOCGIFCONF
            pack('iL', bytes, names.buffer_info()[0])
        ))[0]
        namestr = names.tostring()    
        
        ifreq = []   
        
        # Get interface names
        if uname()[4] == 'x86_64':
            for i in range(0, outbytes, 40):
                ifreq.append({'ifname': namestr[i:i+16].split('\0', 1)[0]})
        else:
            for i in range(0, outbytes, 32):    
                ifreq.append({'ifname': namestr[i:i+32].split('\0', 1)[0]})
               
        # Get interface data    
        for iface in ifreq:
            try:
                iface['ipaddr'] = self._ifinfo(s, 0x8915, iface['ifname']) # SIOCGIFADDR
                iface['brdaddr'] = self._ifinfo(s, 0x8919, iface['ifname']) # SIOCGIFBRDADDR
                iface['netmask'] = self._ifinfo(s, 0x891b, iface['ifname']) # SIOCGIFNETMASK
                iface['macaddr'] = self._ifinfo(s, 0x8927, iface['ifname']) # SIOCSIFHWADDR
            except:
                pass
        
        s.close()        
        return ifreq

    def get_data(self, cfg):
        default_iface = {'hwaddr': 'n/a', 'ifname': 'n/a', 'netmask': 'n/a', 'ipaddr': 'n/a', 'brdaddr': 'n/a'}    
        ifaces = self._ifaces()

        for iface in ifaces:   
            for key in default_iface:
                if not key in iface:
                    iface[key] = default_iface[key]            
              
        return {'network': ifaces}
