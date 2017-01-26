from flask import Blueprint

__author__ = 'Manuel Escriche'

chapters = Blueprint('chapters', __name__)

from . import views
