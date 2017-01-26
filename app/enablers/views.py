__author__ = "Manuel Escriche <mev@tid.es>"

from flask import Blueprint, render_template, abort, request, redirect, url_for, flash
from flask_login import login_required
from flask_wtf import FlaskForm
from wtforms import SelectField
from kconfig import agileCalendar, enablersBook, enablersBookByName
from kernel.Backlog import BacklogFactory, LocalBacklogFactory
from kernel.Reporter import EnablerReporter
from kernel.Analyser import EnablersAnalyser
from kernel.DataBoard import Data
from kernel.NM_Aggregates import EnablerDeck
from kernel.NM_HelpDeskReporter import DeckReporter

from . import enablers

class SelectForm(FlaskForm):
    select = SelectField(u'Enabler')

@enablers.route("/", methods=['GET', 'POST'])
@enablers.route("/overview", methods=['GET', 'POST'])
@login_required
def overview():
    form = SelectForm()
    options = [(n, item) for n,item in enumerate(enablersBookByName)]
    if request.method == 'POST':
        enablername = dict(options)[int(form.select.data)]
        return redirect(url_for('enablers.backlog', enablername=enablername))
    form.select.choices = [(n,'{} - {} - {} ({})'.format(n+1,
                                                         enablersBookByName[item].chapter,
                                                         item, enablersBookByName[item].mode))
                           for n,item in enumerate(enablersBookByName)]
    analyser = EnablersAnalyser.fromFile()
    analyser.enablersBook = enablersBook
    return render_template('enablers/overview.html', analyser = analyser, calendar=agileCalendar, form=form)

@enablers.route("/backlog/<enablername>", methods=['GET', 'POST'])
@login_required
def backlog(enablername):
    enabler = enablersBook[enablername]
    form = SelectForm()

    options = [(n, item) for n,item in enumerate(enablersBookByName)]
    if request.method == 'POST':
        enablername = dict(options)[int(form.select.data)]
        return redirect(url_for('enablers.backlog', enablername=enablername))

    form.select.choices = [(n,'{} - {} - {} ({})'.format(n+1, enablersBookByName[item].chapter, item, enablersBookByName[item].mode)) for n,item in enumerate(enablersBookByName)]

    try:
        backlogFactory = BacklogFactory.getInstance()
        backlog = backlogFactory.getEnablerBacklog(enablername)
    except Exception:
        localFactory = LocalBacklogFactory.getInstance()
        backlog = localFactory.getEnablerBacklog(enablername)
        flash('Data from local storage obtained at {}'.format(backlog.timestamp))

    sortedby = request.args.get('sortedby') if request.args.get('sortedby') else 'name'
    backlog.sort(key=backlog.sortDict[sortedby])
    reporter = EnablerReporter(enablername, backlog)
    return render_template('enablers/backlog.html',
                           enabler=enabler,
                           reporter=reporter,
                           calendar=agileCalendar, form=form)

@enablers.route("/backlog/<enablername>/raw")
@login_required
def raw(enablername):
    enabler = enablersBook[enablername]
    try:
        backlogFactory = BacklogFactory.getInstance()
        backlog = backlogFactory.getEnablerBacklog(enablername)
    except Exception:
        localFactory = LocalBacklogFactory.getInstance()
        backlog = localFactory.getEnablerBacklog(enablername)
        flash('Data from local storage obtained at {}'.format(backlog.timestamp))

    sortedby = request.args.get('sortedby') \
        if request.args.get('sortedby') else 'name'
    backlog.sort(key=backlog.sortDict[sortedby])
    reporter = EnablerReporter(enablername, backlog)
    return render_template('enablers/raw.html',
                           enabler = enabler,
                           reporter=reporter,
                           calendar=agileCalendar)

@enablers.route("/backlog/<enablername>/review")
@login_required
def review(enablername):
    enabler = enablersBook[enablername]
    try:
        backlogFactory = BacklogFactory.getInstance()
        backlog = backlogFactory.getEnablerBacklog(enablername)
    except Exception:
        localFactory = LocalBacklogFactory.getInstance()
        backlog = localFactory.getEnablerBacklog(enablername)
        flash('Data from local storage obtained at {}'.format(backlog.timestamp))
    sortedby = request.args.get('sortedby') if request.args.get('sortedby') else 'name'
    backlog.sort(key=backlog.sortDict[sortedby])
    reporter = EnablerReporter(enablername, backlog)
    return render_template('enablers/review.html',
                           enabler = enabler,
                           reporter=reporter,
                           calendar=agileCalendar)

@enablers.route("/helpdesk/<enablername>", methods=['GET', 'POST'])
@login_required
def helpdesk(enablername):
    enabler = enablersBook[enablername]
    form = SelectForm()
    options = [(n, item) for n,item in enumerate(enablersBookByName)]
    if request.method == 'POST':
        enablername = dict(options)[int(form.select.data)]
        return redirect(url_for('enablers.helpdesk', enablername=enablername))

    form.select.choices = [(n,'{} - {} - {} ({})'.format(n+1, enablersBookByName[item].chapter, item, enablersBookByName[item].mode)) for n,item in enumerate(enablersBookByName)]

    deck = EnablerDeck(enabler, *Data.getEnablerHelpDesk(enablername))
    if deck.source == 'store':
        flash('Data from local storage obtained at {}'.format(deck.timestamp))


    sortedby = request.args.get('sortedby') if request.args.get('sortedby') else 'age'

    reporter = DeckReporter(deck)

    return render_template('enablers/helpdesk.html',
                           enabler=enabler,
                           sortedby=sortedby,
                           data = deck,
                           reporter=reporter,
                           form=form,
                           calendar=agileCalendar)


@enablers.route("/<enablername>/publish")
@login_required
def publish():
    pass


@enablers.route("/<enablername>/packages")
@login_required
def packages():
    pass

@enablers.route("/<enablername>/deploy")
@login_required
def deploy():
    pass