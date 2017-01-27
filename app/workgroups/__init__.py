from flask import Blueprint

__author__ = 'Manuel Escriche'

workgroups = Blueprint('workgroups', __name__)

from . import views
