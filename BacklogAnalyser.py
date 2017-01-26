#!/usr/bin/env python3
import sys
import os
import logging
from config import config
from kernel import settings
from kernel.LocalStorage import updateIssuesLocalStorage, updateBacklogsLocalStorage, updateComponentsLeaders
from kernel.LocalStorage import updateTrackersLocalStorage, updateHelpDesk, updateWorkGroups, updateAccountsDesk
from kernel.LocalStorage import updateLab

__author__ = "Manuel Escriche <mev@tid.es>"

if os.getenv('FLASK_CONFIG') == 'production':
    activate_this = '/var/www/fiware-backlog/venv/bin/activate_this.py'
    # exec(open(activate_this, "rb").read(), globals(), locals())
    exec(open(activate_this, "rb").read(), dict(__file__=activate_this))
    sys.path.insert(0, '/var/www/fiware-backlog/app')
    sys.path.insert(0, '/var/www/fiware-backlog/app/kernel')


config = config[os.getenv('FLASK_CONFIG') or 'default']
settings.storeHome = config.STORE

filename = os.path.join(config.LOGS, 'backloganalyser.log')
logging.basicConfig(filename=filename,
                    format='%(asctime)s|%(levelname)s:%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level='INFO')

logging.info('hello world!')
logging.info('FLASK_CONFIG={}'.format(os.getenv('FLASK_CONFIG')))
logging.info('LOGS={}'.format(config.LOGS))

logging.info('>>>>> updateHelpDesk')
updateHelpDesk()

logging.info('>>>>> updateAccountsDesk')
updateAccountsDesk()

logging.info('>>>>> updateWorkGroups')
updateWorkGroups()

logging.info('>>>>> updateLab')
updateLab()

logging.info('>>>>> updateTrackersLocalStorage')
updateTrackersLocalStorage()

logging.info('>>>>> updateComponentsLeaders')
updateComponentsLeaders()

logging.info('>>>>> updateIssuesLocalStorage')
updateIssuesLocalStorage()

logging.info('>>>>> updateBacklogsLocalStorage')
updateBacklogsLocalStorage()

logging.info('>>>>> Finished')
