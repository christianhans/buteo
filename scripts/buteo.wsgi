#!/usr/bin/python
from buteo import Buteo

# path to your Buteo configuration file
CFG_FILE = '/etc/buteo.cfg'

# path to your Buteo plugin directory
PLUGIN_PATH = '/usr/share/buteo/plugins'

# absolute path to your template files
TEMPLATE_PATH = '/usr/share/buteo/templates'

# use this if you have more than one directory with templates
#TEMPLATE_PATH = ['/path/to/templates', '/path/to/other/templates']

application = Buteo(CFG_FILE, PLUGIN_PATH, TEMPLATE_PATH)
