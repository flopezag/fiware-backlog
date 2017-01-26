__author__ = 'Manuel Escriche'
from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views