__author__ = 'Manuel Escriche'
from flask import Blueprint

urgent = Blueprint('urgent', __name__)

from . import views

