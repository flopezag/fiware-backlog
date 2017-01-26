__author__ = 'Manuel Escriche'

from flask import Blueprint
coordination = Blueprint('coordination', __name__)

from . import views