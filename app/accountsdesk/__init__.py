from flask import Blueprint

accountsdesk = Blueprint('accountsdesk', __name__)

__author__ = 'Manuel Escriche'

from . import views
