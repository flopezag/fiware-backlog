from flask import Blueprint

__author__ = 'Manuel Escriche'

lab = Blueprint('lab', __name__)

from . import views
