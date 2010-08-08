#!/usr/bin/env python
import sys
from glob import glob

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name = 'Buteo',
    version = '0.1',
    description = 'A simple web-based system monitor written in Python.',
    license = 'GPL v2',
    author = 'Christian Hans',
    author_email = 'christian.hans@gmx.net',
    packages = ['buteo'],
    install_requires = ['Werkzeug>=0.5', 'Jinja2>=2.1'],
    scripts = ['manage-buteo.py'],
    data_files = [
        ('/etc', ['buteo.cfg']),
        ('/usr/share/buteo/plugins', glob('plugins/*.py')), 
        ('/usr/share/buteo/templates', glob('templates/*.html')),        
        ('/usr/share/buteo/scripts', ['scripts/buteo.cgi', 'scripts/buteo.fcgi']),        
    ],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: System :: Systems Administration',
        'Topic :: System :: Monitoring',
    ],
)
