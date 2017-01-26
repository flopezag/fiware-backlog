__author__ = 'Manuel Escriche'
from flask import Blueprint

main = Blueprint('main', __name__)
from . import views, errors