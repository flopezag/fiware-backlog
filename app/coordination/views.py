from flask import render_template, flash, request, redirect, url_for
from flask_login import login_required
from kernel import agileCalendar
from kernel.DataBoard import Data
from kernel.NM_Aggregates import WorkBacklog, DevBacklog, RiskBacklog
from kconfig import coordinationBookByName

from . import coordination

__author__ = 'Manuel Escriche'


@coordination.route("/")
@coordination.route("/overview")
@login_required
def overview():
    return redirect(url_for('coordination.delivery'))


@coordination.route("/success-stories")
@login_required
def success_stories():
    cmp = coordinationBookByName['SuccessStories']
    backlog = RiskBacklog(*Data.getGlobalComponent(cmp.key))
    if backlog.source == 'store':
        flash('Data from local storage obtained at {}'.format(backlog.timestamp))
    sortedby = request.args.get('sortedby') if request.args.get('sortedby') else 'timeSlot'

    return render_template('coordination/success_stories.html',
                           comp=cmp,
                           reporter=backlog,
                           sortedby=sortedby,
                           calendar=agileCalendar)


@coordination.route("/friendliness")
@login_required
def friendliness():
    cmp = coordinationBookByName['Friendliness']
    backlog = RiskBacklog(*Data.getGlobalComponent(cmp.key))
    if backlog.source == 'store':
        flash('Data from local storage obtained at {}'.format(backlog.timestamp))
    sortedby = request.args.get('sortedby') if request.args.get('sortedby') else 'timeSlot'

    return render_template('coordination/friendliness.html',
                           comp=cmp,
                           reporter=backlog,
                           sortedby=sortedby,
                           calendar=agileCalendar)


@coordination.route("/qualityassurance")
@login_required
def qualityassurance():
    cmp = coordinationBookByName['QualityAssurance']
    backlog = RiskBacklog(*Data.getGlobalComponent(cmp.key))
    if backlog.source == 'store':
        flash('Data from local storage obtained at {}'.format(backlog.timestamp))
    sortedby = request.args.get('sortedby') if request.args.get('sortedby') else 'timeSlot'

    return render_template('coordination/quality_assurance.html',
                           comp=cmp,
                           reporter=backlog,
                           sortedby=sortedby,
                           calendar=agileCalendar)


@coordination.route("/issues")
@login_required
def issues():
    cmp = coordinationBookByName['Issues']
    backlog = RiskBacklog(*Data.getGlobalComponent(cmp.key))
    if backlog.source == 'store':
        flash('Data from local storage obtained at {}'.format(backlog.timestamp))
    sortedby = request.args.get('sortedby') if request.args.get('sortedby') else 'timeSlot'

    return render_template('coordination/issues.html',
                           comp=cmp,
                           reporter=backlog,
                           sortedby=sortedby,
                           calendar=agileCalendar)


@coordination.route("/risks")
@login_required
def risks():
    cmp = coordinationBookByName['Risks']
    backlog = RiskBacklog(*Data.getGlobalComponent(cmp.key))
    if backlog.source == 'store':
        flash('Data from local storage obtained at {}'.format(backlog.timestamp))
    sortedby = request.args.get('sortedby') if request.args.get('sortedby') else 'timeSlot'

    return render_template('coordination/risks.html',
                           comp=cmp,
                           reporter=backlog,
                           sortedby=sortedby,
                           calendar=agileCalendar)


@coordination.route("/delivery")
@login_required
def delivery():
    cmp = coordinationBookByName['Deliverables']

    backlog = WorkBacklog(*Data.getGlobalComponent(cmp.key))
    if backlog.source == 'store':
        flash('Data from local storage obtained at {}'.format(backlog.timestamp))
    sortedby = request.args.get('sortedby') if request.args.get('sortedby') else 'timeSlot'

    return render_template('coordination/delivery.html',
                           comp=cmp,
                           reporter=backlog,
                           sortedby=sortedby,
                           calendar=agileCalendar)


@coordination.route("/docs")
@login_required
def docs():
    cmp = coordinationBookByName['Documentation']
    backlog = WorkBacklog(*Data.getGlobalComponent(cmp.key))
    if backlog.source == 'store':
        flash('Data from local storage obtained at {}'.format(backlog.timestamp))
    sortedby = request.args.get('sortedby') if request.args.get('sortedby') else 'timeSlot'

    return render_template('coordination/docs.html',
                           comp=cmp,
                           reporter=backlog,
                           sortedby=sortedby,
                           calendar=agileCalendar)


@coordination.route("/agile")
@login_required
def agile():
    cmp = coordinationBookByName['Agile']
    backlog = WorkBacklog(*Data.getGlobalComponent(cmp.key))
    if backlog.source == 'store':
        flash('Data from local storage obtained at {}'.format(backlog.timestamp))
    sortedby = request.args.get('sortedby') if request.args.get('sortedby') else 'timeSlot'

    return render_template('coordination/agile.html',
                           comp=cmp,
                           reporter=backlog,
                           sortedby=sortedby,
                           calendar=agileCalendar)


@coordination.route("/scrum-master")
@login_required
def scrumtools():
    cmp = coordinationBookByName['SMTools']
    backlog = DevBacklog(*Data.getGlobalComponent(cmp.key))
    if backlog.source == 'store':
        flash('Data from local storage obtained at {}'.format(backlog.timestamp))
    sortedby = request.args.get('sortedby') if request.args.get('sortedby') else 'timeSlot'

    return render_template('coordination/scrum_tools.html',
                           comp=cmp,
                           reporter=backlog,
                           sortedby=sortedby,
                           calendar=agileCalendar)
