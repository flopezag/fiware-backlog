__author__ = "Manuel Escriche <mev@tid.es>"

from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from flask_wtf import Form
from wtforms import SelectField
from kconfig import agileCalendar, helpdeskNodesBook, helpdeskBookByName, labsBookByName
from kernel.DataBoard import Data
from kernel.NM_Aggregates import Deck, Backlog, WorkBacklog, ChannelDeck, NodeDeck
from kernel.NM_BacklogReporter import BacklogReporter
from kernel.NM_HelpDeskReporter import DeckReporter, ChannelReporter
from kernel.NM_LabReporter import LabReporter

from . import lab

class SelectForm(Form):
    select = SelectField(u'Items')


@lab.route("/")
@lab.route("/overview")
@login_required
def overview():
    labchapter = labsBookByName['Lab']
    labchannel = helpdeskBookByName['Main-Help-Desk'].channels['Lab']

    reporter = LabReporter().fromFile()

    return render_template('lab/overview.html',
                           lab = (labchapter,labchannel),
                           reporter = reporter,
                           calendar = agileCalendar )

@lab.route("/coordination")
@login_required
def coordination():
    lab = labsBookByName['Lab']
    backlog = WorkBacklog(*Data.getLabComponent(lab.coordination))
    if backlog.source == 'store':
        flash('Data from local storage obtained at {}'.format(backlog.timestamp))
    sortedby = request.args.get('sortedby') if request.args.get('sortedby') else 'timeSlot'
    breporter = BacklogReporter(backlog)
    return render_template('lab/coordination.html',
                            reporter = backlog, analyser = breporter,
                           sortedby = sortedby,
                           calendar = agileCalendar)


@lab.route("/helpdesk", methods=['GET', 'POST'])
@login_required
def ghelpdesk():
    refresh = request.args.get('refresh') if request.args.get('refresh') else False
    form = SelectForm()
    nodesWithHelpDesk = helpdeskNodesBook
    options = [(n, item) for n,item in enumerate(nodesWithHelpDesk)]
    if request.method == 'POST':
        nodename = dict(options)[int(form.select.data)]
        return redirect(url_for('.helpdesk', nodename=nodename))
    form.select.choices = [(n,'{} - {} ({})'.format(n+1, item, nodesWithHelpDesk[item].mode))
                           for n,item in enumerate(nodesWithHelpDesk)]

    channel = helpdeskBookByName['Main-Help-Desk'].channels['Lab']
    channeldata = ChannelDeck(channel, *Data.getChannel(channel.key))

    if channeldata.source == 'store':
        flash('Data from local storage obtained at {}'.format(channeldata.timestamp))


    if refresh:
        reporter = ChannelReporter(channel, channeldata)
    else:
        reporter = ChannelReporter.fromFile(channel)

    return render_template('lab/helpdesk.html',
                           channel = channel,
                           data = channeldata,
                           reporter = reporter,
                           form = form,
                           calendar = agileCalendar)


@lab.route("/helpdesk/<nodename>", methods=['GET', 'POST'])
@login_required
def helpdesk(nodename):
    node = helpdeskNodesBook[nodename]
    nodesWithHelpDesk = helpdeskNodesBook
    form = SelectForm()
    options = [(n, item) for n,item in enumerate(nodesWithHelpDesk)]
    if request.method == 'POST':
        nodename = dict(options)[int(form.select.data)]
        return redirect(url_for('.helpdesk', nodename=nodename))
    form.select.choices = [(n,'{} - {} ({})'.format(n+1, item, nodesWithHelpDesk[item].mode))
                           for n,item in enumerate(nodesWithHelpDesk)]
    deck = NodeDeck(node, *Data.getNodeHelpDesk(nodename))
    if deck.source == 'store':
        flash('Data from local storage obtained at {}'.format(deck.timestamp))
    sortedby = request.args.get('sortedby') if request.args.get('sortedby') else 'age'
    reporter = DeckReporter(deck)
    return render_template('lab/node_helpdesk.html',
                           node = node,
                           sortedby = sortedby,
                           data = deck,
                           reporter = reporter,
                           form = form,
                           calendar = agileCalendar)

@lab.route("/backlog", methods=['GET', 'POST'])
@login_required
def gbacklog():
    lab = labsBookByName['Lab']
    form = SelectForm()
    options = [(n,item) for n,item in enumerate(lab.nodes)]
    if request.method == 'POST':
        nodename = dict(options)[int(form.select.data)]
        return redirect(url_for('.backlog', nodename=nodename))
    form.select.choices = [(n,'{} - {} ({})'.format(n+1, item, lab.nodes[item].mode))
                           for n,item in enumerate(lab.nodes)]

    backlog = WorkBacklog(*Data.getLab())
    if backlog.source == 'store':
        flash('Data from local storage obtained at {}'.format(backlog.timestamp))

    sortedby = request.args.get('sortedby') if request.args.get('sortedby') else 'timeSlot'
    reporter = BacklogReporter(backlog)
    #analyser = LabReporter.fromFile()

    #noBacklog = WorkBacklog(*Data.getWorkGroupNoComponent(lab.keystone))
    return render_template('lab/backlog.html',
                           backlog = backlog,
                           reporter = reporter,
                           form = form,
                           calendar = agileCalendar)

@lab.route("/backlog/<nodename>", methods=['GET', 'POST'])
@login_required
def backlog(nodename):
    lab = labsBookByName['Lab']
    node = lab.nodes[nodename]
    form = SelectForm()
    options = [(n,item) for n,item in enumerate(lab.nodes)]
    if request.method == 'POST':
        nodename = dict(options)[int(form.select.data)]
        return redirect(url_for('.backlog', nodename=nodename))
    form.select.choices = [(n,'{} - {} ({})'.format(n+1, item, lab.nodes[item].mode))
                           for n,item in enumerate(lab.nodes)]

    backlog = WorkBacklog(*Data.getLabComponent(node))
    if backlog.source == 'store':
        flash('Data from local storage obtained at {}'.format(backlog.timestamp))
    sortedby = request.args.get('sortedby') if request.args.get('sortedby') else 'timeSlot'
    reporter = BacklogReporter(backlog)

    return render_template('lab/node_backlog.html',
                           node = node,
                           backlog = backlog,
                           reporter = reporter,
                           form = form,
                           sortedby = sortedby,
                           calendar = agileCalendar)

@lab.route("/recovery")
@login_required
def recovery():
    cmp = labsBookByName['Lab'].comps['Recovery']
    backlog = WorkBacklog(*Data.getLabComponent(cmp))
    if backlog.source == 'store':
        flash('Data from local storage obtained at {}'.format(backlog.timestamp))
    sortedby = request.args.get('sortedby') if request.args.get('sortedby') else 'timeSlot'
    breporter = BacklogReporter(backlog)

    return render_template('lab/recovery.html',
                           reporter = backlog, analyser = breporter,
                           sortedby=sortedby,
                           calendar=agileCalendar)

@lab.route("/deployment")
@login_required
def deployment():
    cmp = labsBookByName['Lab'].comps['Deployment']
    backlog = WorkBacklog(*Data.getLabComponent(cmp))
    if backlog.source == 'store':
        flash('Data from local storage obtained at {}'.format(backlog.timestamp))
    sortedby = request.args.get('sortedby') if request.args.get('sortedby') else 'timeSlot'
    breporter = BacklogReporter(backlog)

    return render_template('lab/deployment.html',
                           reporter = backlog, analyser = breporter,
                           sortedby = sortedby,
                           calendar=agileCalendar)

@lab.route("/testbed")
@login_required
def testbed():
    cmp = labsBookByName['Lab'].comps['Test Bed']
    backlog = WorkBacklog(*Data.getLabComponent(cmp))
    if backlog.source == 'store':
        flash('Data from local storage obtained at {}'.format(backlog.timestamp))
    sortedby = request.args.get('sortedby') if request.args.get('sortedby') else 'timeSlot'
    breporter = BacklogReporter(backlog)
    return render_template('lab/testbed.html',
                            reporter = backlog, analyser = breporter,
                           sortedby = sortedby,
                           calendar = agileCalendar)