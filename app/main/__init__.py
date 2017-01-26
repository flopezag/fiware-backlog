from flask import Blueprint
from . import views, errors

__author__ = 'Manuel Escriche'

main = Blueprint('main', __name__)
