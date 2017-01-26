__author__ = "Manuel Escriche <mev@tid.es>"

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from flask_wtf import Form
from wtforms import SelectField
from kconfig import agileCalendar, workGroupByName
from kernel.DataBoard import Data
from kernel.NM_Aggregates import WorkBacklog, WorkGroupBacklog
from kernel.NM_BacklogReporter import BacklogReporter, WorkGroupReporter, WorkGroupsReporter

from . import workgroups

class SelectForm(Form):
    select = SelectField(u'Backlogs')

@workgroups.route("/")
@workgroups.route("/overview")
@login_required
def overview():
    refresh = request.args.get('refresh') if request.args.get('refresh') else False
    if refresh:
        backlog = WorkGroupBacklog(*Data.getWorkGroups())
        analyser = WorkGroupsReporter(backlog)
    else:
        analyser = WorkGroupsReporter.fromFile('')
    analyser.workgroupBook = workGroupByName
    return render_template('workgroups/overview.html',
                           reporter=analyser,
                           calendar=agileCalendar)


@workgroups.route("/<workgroupname>", methods=['GET', 'POST'])
@login_required
def gbacklog(workgroupname):
    refresh = request.args.get('refresh') if request.args.get('refresh') else False
    form = SelectForm()
    _workgroup = workGroupByName[workgroupname]
    options = [(n,item) for n,item in enumerate(_workgroup.groups)]
    if request.method == 'POST':
        groupname = dict(options)[int(form.select.data)]
        return redirect(url_for('workgroups.backlog', workgroupname=workgroupname, groupname=groupname))
    #form.select.choices = options
    form.select.choices = [(n,'{} - {} ({})'.format(n+1, item, workGroupByName[workgroupname].groups[item].mode))
                           for n,item in enumerate(workGroupByName[workgroupname].groups)]

    backlog = WorkBacklog(*Data.getWorkGroupComponent(_workgroup.coordination.key))
    if backlog.source == 'store':
        flash('Data from local storage obtained at {}'.format(backlog.timestamp))
    sortedby = request.args.get('sortedby') if request.args.get('sortedby') else 'timeSlot'

    if refresh:
        analyser = WorkGroupReporter(_workgroup, backlog)
    else:
        analyser = WorkGroupReporter.fromFile(_workgroup)


    noBacklog = WorkBacklog(*Data.getWorkGroupNoComponent(_workgroup.keystone))
    return render_template('workgroups/dashboard.html',
                           book = workGroupByName, workgroupname = workgroupname,
                           reporter = backlog, analyser = analyser, noBacklog = noBacklog,
                           form = form,
                           sortedby=sortedby, calendar=agileCalendar)


@workgroups.route("/<workgroupname>/<groupname>", methods=['GET', 'POST'])
@login_required
def backlog(workgroupname, groupname):
    form = SelectForm()
    options = [(n,item) for n,item in enumerate(workGroupByName[workgroupname].groups)]
    if request.method == 'POST':
        groupname = dict(options)[int(form.select.data)]
        return redirect(url_for('workgroups.backlog', workgroupname=workgroupname, groupname=groupname))
    #form.select.choices = options
    form.select.choices = [(n,'{} - {} ({})'.format(n+1, item, workGroupByName[workgroupname].groups[item].mode))
                           for n,item in enumerate(workGroupByName[workgroupname].groups)]

    group = workGroupByName[workgroupname].groups[groupname]
    backlog = WorkBacklog(*Data.getWorkGroupComponent(group.key))
    if backlog.source == 'store':
        flash('Data from local storage obtained at {}'.format(backlog.timestamp))
    sortedby = request.args.get('sortedby') if request.args.get('sortedby') else 'timeSlot'

    breporter = BacklogReporter(backlog)
    return render_template('workgroups/group.html',
                           book = workGroupByName, workgroupname = workgroupname, groupname=groupname,
                           reporter = backlog, analyser = breporter,
                           form = form,
                           sortedby=sortedby, calendar=agileCalendar)
