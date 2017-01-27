from flask import Blueprint

__author__ = 'Manuel Escriche'

urgent = Blueprint('urgent', __name__)

from . import views
