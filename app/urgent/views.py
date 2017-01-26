__author__ = "Manuel Escriche <mev@tid.es>"

import logging
from operator import attrgetter
from flask import render_template,request, redirect, url_for, flash
from flask_login import login_required
from kconfig import agileCalendar
from kernel.IssuesList import IssuesList, IssuesFactory
from . import urgent

@urgent.route("/")
@login_required
def main():
    logging.info('Urgent.main')
    try:
        issuesFactory = IssuesFactory.getInstance()
    except Exception:
        return redirect(url_for('urgent.upcoming'))
    if len(issuesFactory.getUrgentIssues('upcoming')):
        return redirect(url_for('urgent.upcoming'))
    elif len(issuesFactory.getUrgentIssues('overdue')):
        return redirect(url_for('urgent.overdue'))
    elif len(issuesFactory.getUrgentIssues('blockers')):
        return redirect(url_for('urgent.blockers'))
    elif len(issuesFactory.getUrgentIssues('impeded')):
        return redirect(url_for('urgent.impeded'))
    else:
        return redirect(url_for('urgent.aged'))

@urgent.route("/upcoming")
@login_required
def upcoming():
    logging.info('upcoming')
    try:
        issuesFactory = IssuesFactory.getInstance()
        upcomingList = issuesFactory.getUrgentIssues('upcoming')
    except:
        upcomingList = IssuesList.fromFile('urgent.upcoming')
        flash('Data from local storage obtained at {}'.format(upcomingList.timestamp))
    upcomingList.sort(key=attrgetter('upcoming'))
    #approachingList.sort(key=attrgetter('priority'))
    if request.args.get('sortedby'):
        sortedby = request.args.get('sortedby')
        upcomingList.sort(key=upcomingList.sortDict[sortedby], reverse=True)
    return render_template('urgent/upcoming.html',approaching=upcomingList, calendar=agileCalendar)


@urgent.route("/overdue")
@login_required
def overdue():
    try:
        issuesFactory = IssuesFactory.getInstance()
        overdueList = issuesFactory.getUrgentIssues('overdue')
    except:
        overdueList = IssuesList.fromFile('urgent.overdue')
        flash('Data from local storage obtained at {}'.format(overdueList.timestamp))
    overdueList.sort(key=attrgetter('delay'), reverse=True)
    overdueList.sort(key=attrgetter('priority'))
    if request.args.get('sortedby'):
        sortedby = request.args.get('sortedby')
        overdueList.sort(key=overdueList.sortDict[sortedby], reverse=True)
    return render_template('urgent/overdue.html',overdue=overdueList, calendar=agileCalendar)

@urgent.route("/blockers")
@login_required
def blockers():
    try:
        issuesFactory = IssuesFactory.getInstance()
        blockersList = issuesFactory.getUrgentIssues('blockers')
        #impededList = issuesFactory.getUrgentIssues('impeded')
    except:
        blockersList = IssuesList.fromFile('urgent.blockers')
        #impededList = IssuesList.fromFile('urgent.impeded')
        flash('Data from local storage obtained at {}'.format(blockersList.timestamp))
    blockersList.sort(key=attrgetter('age'), reverse=True)
    blockersList.sort(key=attrgetter('status'))
    #impededList.sort(key=attrgetter('age'), reverse=True)
    if request.args.get('sortedby'):
        sortedby = request.args.get('sortedby')
        blockersList.sort(key=blockersList.sortDict[sortedby], reverse=True)
        #impededList.sort(key=impededList.sortDict[sortedby], reverse=True)
    return render_template('urgent/blockers.html', blockersL=blockersList, calendar=agileCalendar)

@urgent.route("/impeded")
@login_required
def impeded():
    try:
        issuesFactory = IssuesFactory.getInstance()
        impededList = issuesFactory.getUrgentIssues('impeded')
    except:
        impededList = IssuesList.fromFile('urgent.impeded')
        flash('Data from local storage obtained at {}'.format(impededList.timestamp))
    impededList.sort(key=attrgetter('age'), reverse=True)
    if request.args.get('sortedby'):
        sortedby = request.args.get('sortedby')
        impededList.sort(key=impededList.sortDict[sortedby], reverse=True)
    return render_template('urgent/impeded.html', impededL=impededList, calendar=agileCalendar)


@urgent.route("/aged")
@login_required
def aged():
    try:
        issuesFactory = IssuesFactory.getInstance()
        agedList = issuesFactory.getUrgentIssues('aged')
    except:
        agedList = IssuesList.fromFile('urgent.aged')
        flash('Data from local storage obtained at {}'.format(agedList.timestamp))
    agedList.sort(key=attrgetter('age'), reverse=True)
    agedList.sort(key=attrgetter('priority'))
    if request.args.get('sortedby'):
        sortedby = request.args.get('sortedby')
        agedList.sort(key=agedList.sortDict[sortedby], reverse=True)
    return render_template('urgent/aged.html', aged=agedList, calendar=agileCalendar)
