from flask import Blueprint

__author__ = 'Manuel Escriche'

guide = Blueprint('guide', __name__)

from . import views
