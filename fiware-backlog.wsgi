activate_this = '/var/www/fiware-backlog/venv/bin/activate_this.py'
exec(open(activate_this, "rb").read(), dict(__file__=activate_this))

from BacklogWebSite import app as application
