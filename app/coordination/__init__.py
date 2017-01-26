from flask import Blueprint

__author__ = 'Manuel Escriche'

coordination = Blueprint('coordination', __name__)

from . import views
