__author__ = 'Manuel Escriche'

from flask import Blueprint

workgroups = Blueprint('workgroups', __name__)

from . import views