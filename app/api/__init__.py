__author__ = 'Manuel Escriche'

from flask import Blueprint
api = Blueprint('api', __name__)

from . import services