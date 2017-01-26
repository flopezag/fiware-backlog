__author__ = 'Manuel Escriche'

from flask import Blueprint
helpdesk = Blueprint('helpdesk', __name__)

from . import views