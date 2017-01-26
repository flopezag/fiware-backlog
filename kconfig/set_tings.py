#!/usr/bin/env python
# -*- encoding: utf-8 -*-
##
# Copyright 2017 FIWARE Foundation, e.V.
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
##

import os.path
from configparser import ConfigParser

__author__ = 'fla'

__version__ = '1.0.0'

"""
Default configuration.

The configuration `cfg_defaults` are loaded from `cfg_filename`, if file exists in
/etc/fiware.d/backlog.ini

Optionally, user can specify the file location manually using an Environment variable
called BACKLOG_SETTINGS_FILE.
"""

name = 'backlog'

cfg_dir = "/etc/fiware.d"

if os.environ.get("BACKLOG_SETTINGS_FILE"):
    cfg_filename = os.environ.get("BACKLOG_SETTINGS_FILE")

else:
    cfg_filename = os.path.join(cfg_dir, '%s.ini' % name)

Config = ConfigParser()

Config.read(cfg_filename)


def config_section_map(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                print("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1


if Config.sections():
    # Data from oauth2 section
    print("Config Parser method")
    # oauth_section = config_section_map("oauth2")

    # ACCESS_TOKEN = oauth_section['access_token']

else:
    msg = '\nERROR: There is not defined BACKLOG_SETTINGS_FILE environment variable ' \
          '\n       pointing to configuration file or there is no backlog.ini file' \
          '\n       in the /etd/init.d directory.' \
          '\n\n       Please correct at least one of them to execute the program.'
    exit(msg)

