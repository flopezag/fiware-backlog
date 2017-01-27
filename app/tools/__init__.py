from flask import Blueprint

__author__ = 'Manuel Escriche'

tools = Blueprint('tools', __name__)

from . import views
