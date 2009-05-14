#!/usr/bin/python
from wsgiref.handlers import CGIHandler
from buteo import Buteo

# absolute path to your Buteo configuration file
CFG_FILE = '/etc/buteo.cfg'

# path to your template files.
TEMPLATE_PATH = '/usr/share/buteo/templates'

# use this if you have more than one directory with templates
#TEMPLATE_PATH = ['/path/to/templates', '/path/to/other/templates']

app = Buteo(CFG_FILE, TEMPLATE_PATH)
CGIHandler().run(app)
