import os
import logging
import warnings
from app import create_app


__author__ = "Manuel Escriche <mev@tid.es>"

# warnings.filterwarnings(action='ignore', category=DeprecationWarning)
# warnings.filterwarnings(action='ignore', module='connectionpool')

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

if not app.debug:
    filename = os.path.join(app.config['LOGS'], 'backlogwebsite.log')
    logging.basicConfig(filename=filename,
                        format='%(asctime)s|%(levelname)s:%(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level='INFO')

logging.info('hello world!')


if __name__ == "__main__":
    app.run()
