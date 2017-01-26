__author__ = 'Manuel Escriche'

from flask import Blueprint
lab = Blueprint('lab', __name__)

from . import views