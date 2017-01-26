__author__ = 'Manuel Escriche'

from flask import render_template, redirect, url_for, request
from flask_login import login_required
from . import main


@main.route("/", methods=['GET', 'POST'])
@login_required
def home():
    return redirect(url_for('urgent.main'))
