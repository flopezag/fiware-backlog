import re
from flask import Blueprint, render_template, abort, request, redirect, url_for, flash
from flask_login import login_required
from flask_wtf import Form
from wtforms import SelectField
from operator import attrgetter
from . import accountsdesk

from kconfig import agileCalendar
from kconfig import accountsdeskBookByName, labsBookByName
from kernel.IssuesList import IssuesList, IssuesFactory
from kernel.Desk import TrackerDeskReporter
from kernel.DataBoard import Data
from kernel.NM_AccountsDeskReporter import ADeck, DeskReporter, ChannelReporter

__author__ = "Manuel Escriche <mev@tid.es>"


class SelectForm(Form):
    select = SelectField(u'Items')


@accountsdesk.route("/")
@accountsdesk.route("/overview")
@login_required
def overview():
    return redirect(url_for('.requests'))


@accountsdesk.route("/accounts/requests", methods=['GET', 'POST'])
@login_required
def requests():
    refresh = request.args.get('refresh') if request.args.get('refresh') else False
    form = SelectForm()
    deskname = 'Accounts-Desk'
    desk = accountsdeskBookByName[deskname]
    options = [(n, item) for n, item in enumerate(desk.channels)]

    if request.method == 'POST':
        channelname = dict(options)[int(form.select.data)]

        return redirect(url_for('.requestToChannel', channelname=channelname))

    form.select.choices = options

    if refresh:
        data = ADeck(*Data.getAccountDeskRequests())
        
        if data.source == 'store':
            flash('Unable to get fresh data from JIRA server')
        else:
            reporter = DeskReporter(desk, data)
    else:
        data = ADeck(*Data.getFocusedAccountDeskRequest())
        if data.source == 'store':
            flash('Data from local storage obtained at {}'.format(data.timestamp))

    reporter = DeskReporter.fromFile(desk)

    return render_template('accountsdesk/requests.html',
                           desk=desk,
                           data=data,
                           reporter=reporter,
                           form=form,
                           calendar=agileCalendar)


@accountsdesk.route("/accounts/requests/<channelname>", methods=['GET', 'POST'])
@login_required
def requestFromChannel(channelname):
    refresh = request.args.get('refresh') if request.args.get('refresh') else False
    form = SelectForm()
    deskname = 'Accounts-Desk'
    desk = accountsdeskBookByName[deskname]
    options = [(n, item) for n, item in enumerate(desk.channels)]
    if request.method == 'POST':
        channelname = dict(options)[int(form.select.data)]
        return redirect(url_for('.requestFomChannel', channelname=channelname))
    form.select.choices = options
    channel = desk.channels[channelname]
    if refresh:
        data = ADeck(*Data.getAccountChannelRequests(channel))
        if data.source == 'store':
            flash('Unable to get fresh data from JIRA server')
            reporter = ChannelReporter.fromFile(channel)
        else:
            if data.source == 'store':
                flash('Data from local storage obtained at {}'.format(data.timestamp))
            reporter = ChannelReporter(channel, data)
    else:
        data = ADeck(*Data.getFocusedAccountChannelRequest(channel))
        reporter = ChannelReporter.fromFile(channel)

    return render_template('accountsdesk/requestFromChannel.html',
                           book=accountsdeskBookByName,
                           deskname=deskname,
                           channelname=channelname,
                           data=data,
                           reporter=reporter,
                           form=form,
                           calendar=agileCalendar)


@accountsdesk.route("/accounts/provisioning")
@login_required
def provision():
    try:
        issues_factory = IssuesFactory.getInstance()
        account_list = issues_factory.getIssuesFromRequest('lab.accounts.unresolved')
    except Exception:
        # print(Exception)
        account_list = IssuesList.fromFile('lab.accounts.unresolved')
        flash('Data from local storage obtained at {}'.format(account_list.timestamp))

    request_issues = [issue for issue in account_list if re.match(r'Assign Resources [\w\s]+ for:', issue.reference)]
    account_list = IssuesList('lab.accountsImpl.unresolved.requests', request_issues)
    account_list.sort(key=attrgetter('age'), reverse=True)
    account_list.sort(key=attrgetter('priority'))
    if request.args.get('sortedby'):
        sortedby = request.args.get('sortedby')
        account_list.sort(key=account_list.sortDict[sortedby], reverse=True)

    request_issues = [issue for issue in IssuesList.fromFile('lab.accounts')
                      if re.match(r'Assign Resources [\w\s]+ for:', issue.reference)]

    accountlab_list = IssuesList('lab.accountsImpl.requests', request_issues)
    accountlab_list.sort(key=attrgetter('age'))
    reporter = TrackerDeskReporter(accountlab_list, 'FLUA', 'ACCOUNTS PROVISIONING')

    return render_template('accountsdesk/provision.html',
                           reporter=reporter,
                           issuesList=account_list,
                           allList=accountlab_list,
                           calendar=agileCalendar)


@accountsdesk.route("/provisioning/nodes/<nodename>")
@login_required
def provisionInNode(nodename):
    nodes = labsBookByName['Lab'].nodes

    try:
        issues_factory = IssuesFactory.getInstance()
        accountlab_list = issues_factory.getIssuesFromRequest('lab.accounts')
    except Exception:
        accountlab_list = IssuesList.fromFile('lab.accounts')
        flash('Data from local storage obtained at {}'.format(accountlab_list.timestamp))

    accountlab_list = [issue for issue in accountlab_list if re.match(r'Assign Resources [\w\s]+ for:', issue.reference)]

    reporter = TrackerDeskReporter(accountlab_list, 'FLUA', 'ACCOUNTS PROVISIONING')

    return render_template('accountsdesk/provisionInNode.html',
                           reporter=reporter,
                           calendar=agileCalendar)
