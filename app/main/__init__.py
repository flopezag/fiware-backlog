from flask import Blueprint

__author__ = 'Manuel Escriche'

main = Blueprint('main', __name__)

from . import views, errors
