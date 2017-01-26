__author__ = 'Manuel Escriche'

from flask import Blueprint
guide = Blueprint('guide', __name__)

from . import views