__author__ = "Manuel Escriche <mev@tid.es>"

from flask import current_app
from flask_login import login_required
from flask import Blueprint, render_template, abort, request, redirect, url_for, flash
from . import guide

@guide.route('/')
@login_required
def dochome():
    return redirect('http://backlog.fiware.org/guide/index.html')
