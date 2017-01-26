__author__ = 'Manuel Escriche'

from flask import Blueprint
enablers = Blueprint('enablers', __name__)

from . import views