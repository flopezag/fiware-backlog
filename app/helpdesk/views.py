__author__ = "Manuel Escriche <mev@tid.es>"
import time
from operator import attrgetter
from flask import Blueprint, render_template, abort, request, redirect, url_for, flash
from flask_login import login_required
from flask_wtf import FlaskForm
from wtforms import SelectField

from kconfig import agileCalendar, helpdeskBookByName
from kernel.DataBoard import Data
from kernel.NM_Aggregates import Deck, iDeck, DeskDeck, DeskiDeck, ChannelDeck, InnChannel
from kernel.NM_HelpDeskReporter import ChannelReporter, DeskReporter

from . import helpdesk

class SelectForm(FlaskForm):
    select = SelectField(u'Channels')


@helpdesk.route("/", methods=['GET', 'POST'])
@login_required
def overview():
    refresh = request.args.get('refresh') if request.args.get('refresh') else False
    maindesk = helpdeskBookByName['Main-Help-Desk']
    coachdesk = helpdeskBookByName['Coaches-Help-Desk']

    if refresh:
        deskdata = DeskDeck(maindesk, *Data.getDesk(maindesk))
        maindeskreporter = DeskReporter(maindesk, deskdata)
        coachdata = DeskDeck(coachdesk, *Data.getDesk(coachdesk))
        coachdeskreporter = DeskReporter(coachdesk, coachdata)
    else:
        maindeskreporter = DeskReporter.fromFile(maindesk)
        coachdeskreporter = DeskReporter.fromFile(coachdesk)

    return render_template('helpdesk/overview.html',
                           maindesk = maindesk,
                           mainreporter = maindeskreporter,
                           coachdesk = coachdesk,
                           coachreporter = coachdeskreporter,
                           calendar = agileCalendar)


@helpdesk.route("/main", methods=['GET', 'POST'])
@login_required
def main():
    refresh = request.args.get('refresh') if request.args.get('refresh') else False
    desk = helpdeskBookByName['Main-Help-Desk']
    form = SelectForm()
    options = [(n,item) for n,item in enumerate(desk.channels)]
    if request.method == 'POST':
        channelname = dict(options)[int(form.select.data)]
        return redirect(url_for('helpdesk.channel', channelname=channelname))
    form.select.choices = options

    if refresh:
        data = Deck(*Data.getFocusedDesk(desk))
        if data.source == 'store':
            flash('Unable to get fresh data from JIRA server')
        else:
            reporter = DeskReporter(desk, data)
    else:
        data = Deck(*Data.getDesk(desk))
        if data.source == 'store':
            flash('Data from local storage obtained at {}'.format(data.timestamp))

    reporter = DeskReporter.fromFile(desk)

    return render_template('helpdesk/maindesk.html',
                           desk=desk,
                           data=data,
                           reporter=reporter,
                           form=form,
                           calendar=agileCalendar)


@helpdesk.route("/channel/<channelname>", methods=['GET', 'POST'])
@login_required
def channel(channelname):
    refresh = request.args.get('refresh') if request.args.get('refresh') else False
    deskname = 'Main-Help-Desk'
    form = SelectForm()
    options = [(n,item) for n,item in enumerate(helpdeskBookByName[deskname].channels)]
    if request.method == 'POST':
        channelname = dict(options)[int(form.select.data)]
        return redirect(url_for('.channel', channelname=channelname))
    form.select.choices = options

    channel = helpdeskBookByName[deskname].channels[channelname]
    channeldata = ChannelDeck(channel, *Data.getChannel(channel.key))

    if channeldata.source == 'store':
        flash('Data from local storage obtained at {}'.format(channeldata.timestamp))

    if refresh:
        if channeldata.source == 'store':
            flash('Unable to get fresh data from JIRA server')
            reporter = ChannelReporter.fromFile(channel)
        else:
            reporter = ChannelReporter(channel, channeldata)
    else:
        reporter = ChannelReporter.fromFile(channel)

    return render_template('helpdesk/maindeskchannel.html',
                           book = helpdeskBookByName, helpdeskname = deskname, channelname=channelname,
                           data = channeldata,
                           reporter = reporter,
                           form = form,
                           calendar=agileCalendar)

@helpdesk.route("/lab")
#@login_required
def lab():
    deskname = 'Main-Help-Desk'
    channelname = 'Lab'
    channel = helpdeskBookByName[deskname].channels[channelname]
    channeldata = ChannelDeck(channel, *Data.getChannel(channel.key))
    if channeldata.source == 'store':
        flash('Data from local storage obtained at {}'.format(channeldata.timestamp))
    reporter = ChannelReporter.fromFile(channel)
    return render_template('helpdesk/pchannel.html',
                           book = helpdeskBookByName, helpdeskname = deskname, channelname=channelname,
                           data = channeldata,
                           reporter = reporter,
                           calendar=agileCalendar)

@helpdesk.route("/tech")
#@login_required
def tech():
    deskname = 'Main-Help-Desk'
    channelname = 'Tech'
    channel = helpdeskBookByName[deskname].channels[channelname]
    channeldata = ChannelDeck(channel, *Data.getChannel(channel.key))
    if channeldata.source == 'store':
        flash('Data from local storage obtained at {}'.format(channeldata.timestamp))
    reporter = ChannelReporter.fromFile(channel)

    return render_template('helpdesk/pchannel.html',
                           book = helpdeskBookByName, helpdeskname = deskname, channelname=channelname,
                           data = channeldata,
                           reporter = reporter,
                           calendar=agileCalendar)

@helpdesk.route("/coaches", methods=['GET', 'POST'])
@login_required
def coaches():
    refresh = request.args.get('refresh') if request.args.get('refresh') else False
    desk = helpdeskBookByName['Coaches-Help-Desk']

    form = SelectForm()
    options = [(n,item) for n,item in enumerate(desk.channels)]
    if request.method == 'POST':
        channelname = dict(options)[int(form.select.data)]
        return redirect(url_for('.cchannel', channelname=channelname))
    form.select.choices = options

    if refresh:
        data = Deck(*Data.getFocusedDesk(desk))
        if data.source == 'store':
            flash('Unable to get fresh data from JIRA server')
        else:
            reporter = DeskReporter(desk, data)
    else:
        data = Deck(*Data.getDesk(desk))
        if data.source == 'store':
            flash('Data from local storage obtained at {}'.format(data.timestamp))

    reporter = DeskReporter.fromFile(desk)

    return render_template('helpdesk/coachesdesk.html',
                           desk=desk,
                           form=form,
                           data=data,
                           reporter=reporter,
                           calendar=agileCalendar)

@helpdesk.route("/coaches/channel/<channelname>", methods=['GET', 'POST'])
@login_required
def cchannel(channelname):
    refresh = True if request.args.get('refresh') else False
    deskname = 'Coaches-Help-Desk'
    form = SelectForm()
    options = [(n,item) for n,item in enumerate(helpdeskBookByName[deskname].channels)]
    if request.method == 'POST':
        channelname = dict(options)[int(form.select.data)]
        return redirect(url_for('.cchannel', channelname=channelname))

    form.select.choices = options
    channel = helpdeskBookByName[deskname].channels[channelname]
    channeldata = ChannelDeck(channel, *Data.getChannel(channel.key))

    if channeldata.source == 'store':
        flash('Data from local storage obtained at {}'.format(channeldata.timestamp))

    if refresh:
        if channeldata.source == 'store':
            flash('Unable to get fresh data from JIRA server')
            reporter = ChannelReporter.fromFile(channel)
        else:
            reporter = ChannelReporter(channel, channeldata)
    else:
        reporter = ChannelReporter.fromFile(channel)

    return render_template('helpdesk/coachesdeskchannel.html',
                           book = helpdeskBookByName, helpdeskname = deskname, channelname=channelname,
                           data = channeldata,
                           reporter = reporter, form = form,
                           calendar=agileCalendar)


@helpdesk.route("/tools", methods=['GET', 'POST'])
@login_required
def tools():
    refresh = True if request.args.get('refresh') else False
    desk = helpdeskBookByName['ToolsSupport-Help-Desk']
    form = SelectForm()
    options = [(n,item) for n,item in enumerate(desk.channels)]
    if request.method == 'POST':
        channelname = dict(options)[int(form.select.data)]
        return redirect(url_for('.tchannel', channelname=channelname))
    form.select.choices = options

    if refresh:
        data = iDeck(*Data.getFocusedDesk(desk))
        if data.source == 'store':
            flash('Unable to get fresh data from JIRA server')
        else:
            reporter = DeskReporter(desk, data)
    else:
        data = iDeck(*Data.getDesk(desk))
        if data.source == 'store':
            flash('Data from local storage obtained at {}'.format(data.timestamp))

    reporter = DeskReporter.fromFile(desk)



    return render_template('helpdesk/toolsdesk.html',
                           desk=desk,
                           form=form,
                           data=data,
                           reporter=reporter,
                           calendar=agileCalendar)


@helpdesk.route("/tools/channel/<channelname>", methods=['GET', 'POST'])
@login_required
def tchannel(channelname):
    refresh = True if request.args.get('refresh') else False
    deskname = 'ToolsSupport-Help-Desk'
    form = SelectForm()
    options = [(n,item) for n,item in enumerate(helpdeskBookByName[deskname].channels)]
    if request.method == 'POST':
        channelname = dict(options)[int(form.select.data)]
        return redirect(url_for('.tchannel', channelname=channelname))

    form.select.choices = options
    channel = helpdeskBookByName[deskname].channels[channelname]

    data = iDeck(*Data.getFocusedChannel(channel))
    if data.source == 'store':
        flash('Data from local storage obtained at {}'.format(data.timestamp))
    #sortedby = request.args.get('sortedby') if request.args.get('sortedby') else 'age'

    refresh = True if request.args.get('refresh') else False

    if refresh:
        channeldata = InnChannel(*Data.getChannel(channel.key))
        reporter = ChannelReporter(channel, channeldata)
    else:
        reporter = ChannelReporter.fromFile(channel)

    return render_template('helpdesk/toolsdeskchannel.html',
                           book = helpdeskBookByName, helpdeskname = deskname, channelname=channelname,
                           data = data,
                           reporter = reporter, form = form,
                           calendar=agileCalendar)

