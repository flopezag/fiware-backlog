__author__ = 'Manuel Escriche'

from flask import Blueprint
accountsdesk = Blueprint('accountsdesk', __name__)

from . import views