__author__ = "Manuel Escriche <mev@tid.es>"
from flask import Blueprint, render_template, abort, request, redirect, url_for, flash
from flask_login import login_required
from kernel.Backlog import BacklogFactory, LocalBacklogFactory
from kernel.Reporter import ToolReporter
from kernel import agileCalendar
from . import tools

#user = User.get(current_user.get_id())

@tools.route("/<toolname>")
@login_required
def tool(toolname):
    return redirect(url_for('.dashboard', toolname=toolname))

@tools.route("/<toolname>/dashboard")
@login_required
def dashboard(toolname):
    try:
        backlogFactory = BacklogFactory.getInstance()
        backlog = backlogFactory.getToolBacklog(toolname)
    except Exception:
        localFactory = LocalBacklogFactory.getInstance()
        backlog = localFactory.getToolBacklog(toolname)
        flash('Data from local storage obtained at {}'.format(backlog.timestamp))

    sortedby = request.args.get('sortedby') if request.args.get('sortedby') else 'name'
    backlog.sort(key=backlog.sortDict[sortedby])
    reporter = ToolReporter(toolname, backlog)
    return render_template('tools/dash.html', reporter=reporter, calendar=agileCalendar)

@tools.route("/<toolname>/raw")
@login_required
def raw(toolname):
    try:
        backlogFactory = BacklogFactory.getInstance()
        backlog = backlogFactory.getToolBacklog(toolname)
    except Exception:
        localFactory = LocalBacklogFactory.getInstance()
        backlog = localFactory.getToolBacklog(toolname)
        flash('Data from local storage obtained at {}'.format(backlog.timestamp))

    sortedby = request.args.get('sortedby') \
        if request.args.get('sortedby') else 'name'
    backlog.sort(key=backlog.sortDict[sortedby])
    reporter = ToolReporter(toolname, backlog)
    return render_template('tools/raw.html', reporter=reporter, calendar=agileCalendar)

@tools.route("/<toolname>/review")
@login_required
def review(toolname):
    try:
        backlogFactory = BacklogFactory.getInstance()
        backlog = backlogFactory.getToolBacklog(toolname)
    except Exception:
        localFactory = LocalBacklogFactory.getInstance()
        backlog = localFactory.getToolBacklog(toolname)
        flash('Data from local storage obtained at {}'.format(backlog.timestamp))
    sortedby = request.args.get('sortedby') if request.args.get('sortedby') else 'name'
    backlog.sort(key=backlog.sortDict[sortedby])
    reporter = ToolReporter(toolname, backlog)
    return render_template('tools/review.html', reporter=reporter, calendar=agileCalendar)
