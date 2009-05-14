#!/usr/bin/env python
import sys
from glob import glob
from distutils.core import setup

if sys.version_info < (2, 4):
    print 'ERROR: Buteo requires at least Python 2.4 to run.'
    sys.exit(1)

setup(
    name = 'Buteo',
    version = '0.1 Alpha',
    description = 'A simple web-based system monitor written in Python.',
    license = 'GPL v2',
    author = 'Christian Hans',
    author_email = 'christian.hans@gmx.net',
    packages = ['buteo'],
    install_requires = ['Werkzeug>=0.5', 'Jinja2>=2.1'],
    scripts=['manage-buteo.py'],
    data_files = [
        ('/etc', ['buteo.cfg']),
        ('/usr/share/buteo/templates', glob('templates/*.html')),        
        ('/usr/share/buteo/scripts', ['scripts/buteo.cgi', 'scripts/buteo.fcgi']),        
    ],
    classifiers = ['Development Status :: 2 - Pre-Alpha',
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
