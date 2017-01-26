from flask import Blueprint

__author__ = 'Manuel Escriche'

auth = Blueprint('auth', __name__)

from . import views
