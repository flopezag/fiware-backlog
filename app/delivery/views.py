from flask import  render_template, abort
from flask_login import login_required
from jinja2 import TemplateNotFound
from kconfig import calendar, agileCalendar, deliveryBook

from . import delivery

__author__ = "Manuel Escriche <mev@tid.es>"


@delivery.route("/")
@delivery.route("/dashboard")
@login_required
def dashboard():
    month = calendar.currentMonth[0]
    try:
        return render_template('delivery/dashboard.html',
                               month=month,
                               data=deliveryBook.dashboard,
                               calendar=agileCalendar)
    except TemplateNotFound:
        abort(404)


@delivery.route("/delivered")
@login_required
def delivered():
    month = calendar.currentMonth[0]
    try:
        return render_template('delivery/delivered.html',
                               month=month,
                               data=deliveryBook.delivered,
                               calendar=agileCalendar)
    except TemplateNotFound:
        abort(404)


@delivery.route("/pending")
@login_required
def pending():
    month = calendar.currentMonth[0]
    try:
        return render_template('delivery/pending.html',
                               month=month,
                               data=deliveryBook.scheduled,
                               calendar=agileCalendar)
    except TemplateNotFound:
        abort(404)


if __name__ == "__main__":
    pass
