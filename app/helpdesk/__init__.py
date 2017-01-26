from flask import Blueprint

__author__ = 'Manuel Escriche'

helpdesk = Blueprint('helpdesk', __name__)

from . import views
