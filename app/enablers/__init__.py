from flask import Blueprint

__author__ = 'Manuel Escriche'

enablers = Blueprint('enablers', __name__)

from . import views
