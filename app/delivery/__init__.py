from flask import Blueprint

__author__ = 'Manuel Escriche'

delivery = Blueprint('delivery', __name__)

from . import views
