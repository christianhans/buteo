Buteo System Monitor
====================

Copyright (c) 2010 Christian Hans
Licensed under the terms of the GPL v2

Buteo is a simple web-based system monitor written in Python. It displays all
relevant information about your system on a single web page. Buteo is fast,
easy-to-use and it can easily be extended with your own plugins. By default
Buteo is supplied with a lot of plugins, like a plugin for network details or a
plugin that lists vnStat data.

Requirements
------------

Currently Buteo only supports Linux systems. In order to use Buteo a recent
version of Python 2.x is required. Python should normally be supplied by your
distribution, unless you have a minimalist Linux installation.

Besides the Werkzeug and Jinja2 python modules have to be installed. If you have
setuptools on your system just do:

    # easy_install werkzeug jinja2

First run
---------

Running Buteo is possible without a complete installation. For testing purposes
a simple web server is included. To start the test server use the
manage-buteo.py script:

    $ python manage-buteo.py runserver
    
If you run Buteo e.g. on a server and you want to access the web service from
outside, you have to bind the web server to a hostname. To do this, specify with
the -h option a hostname (e.g. the IP or the domain over which your machine is
reachable).

    $ python manage-buteo.py runserver -h yourdomain.com

Run the manage-buteo.py script with the --help option to get more detailed usage
information.

Installation
------------

Although a installation isn't necessary, a persistent installation might be
considered for production environments. Just use the supplied setup.py script:

    # python setup.py install

The plugins, templates and and server scripts will be installed to
/usr/share/buteo. The configuration file is located then at /etc/buteo.cfg.
After installation the manage-buteo.py script can be used system-wide:

    $ manage-buteo.py runserver

Configuration
-------------

Have a look at the /etc/buteo.cfg file to configure Buteo. For example it's
possible to activate authentication, change the template, activate vnStat
information or to define a refresh interval.

Production environment
----------------------

It's not recommended to use the built-in web server in larger production
environments. For few traffic, the built-in web server is completely fine. To
run the Buteo web server in background, simply use the nohup command:

    nohup python manage-buteo.py runserver &

But if you expect more traffic, configure your system's web server to run Buteo
via CGI, FastCGI oder mod_wsgi (Apache). Example scripts for a web server setup
can be found in the scripts/ folder.

For further details refer to the Werkzeug documentation at:
http://werkzeug.pocoo.org/documentation/
