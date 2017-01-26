__author__ = 'Manuel Escriche'

from flask import Blueprint

chapters = Blueprint('chapters', __name__)

from . import views