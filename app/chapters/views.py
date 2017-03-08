import logging
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from flask_wtf import Form
from wtforms import SelectField
from kconfig import chaptersBookByName, chaptersBook
from kconfig import enablersBookByName
from kernel.Backlog import BacklogFactory, LocalBacklogFactory
from kernel.Analyser import ChapterAnalyser, ChaptersAnalyser
from kernel.Reporter import CoordinationReporter
from kernel import agileCalendar
from kernel.DataBoard import Data
from kernel.NM_Aggregates import ChapterDeck
from kernel.NM_HelpDeskReporter import DeckReporter

from . import chapters

__author__ = "Manuel Escriche <mev@tid.es>"


class SelectForm(Form):
    select = SelectField(u'Backlogs')


@chapters.route("/")
@chapters.route("/overview")
@login_required
def overview():
    analyser = ChaptersAnalyser.fromFile()
    analyser.chaptersBook = chaptersBookByName
    return render_template('chapters/overview.html', analyser=analyser, calendar=agileCalendar)


@chapters.route("helpdesk/<chaptername>", methods=['GET', 'POST'])
@login_required
def helpdesk(chaptername):
    chapter = chaptersBook[chaptername]
    form = SelectForm()
    options = [(n, item) for n, item in enumerate(enablersBookByName)]
    if request.method == 'POST':
        enablername = dict(options)[int(form.select.data)]
        return redirect(url_for('enablers.helpdesk', enablername=enablername))

    form.select.choices = [(n, '{} - {} - {} ({})'
                            .format(n+1, enablersBookByName[item].chapter, item, enablersBookByName[item].mode))
                           for n, item in enumerate(enablersBookByName)]

    data = ChapterDeck(chapter, *Data.getChapterHelpDesk(chaptername))
    if data.source == 'store':
        flash('Data from local storage obtained at {}'.format(data.timestamp))

    sortedby = request.args.get('sortedby') if request.args.get('sortedby') else 'age'
    reporter = DeckReporter(chaptername, data)

    return render_template('chapters/helpdesk.html',
                           chapter=chapter,
                           sortedby=sortedby,
                           data=data,
                           reporter=reporter,
                           form=form,
                           calendar=agileCalendar)


@chapters.route("backlog/<chaptername>", methods=['GET', 'POST'])
@login_required
def backlog(chaptername):
    analyser = ChapterAnalyser.fromFile(chaptername)
    form = SelectForm()
    options = [(n, item) for n, item in enumerate(analyser.enablers)]

    if request.method == 'POST':
        enablername = dict(options)[int(form.select.data)]
        return redirect(url_for('enablers.backlog', enablername=enablername))

    form.select.choices = [(n, '{} ({})'.format(item, enablersBookByName[item].mode))
                           for n, item in enumerate(analyser.enablers)]

    analyser.chaptersBook = chaptersBookByName

    try:
        backlog_factory = BacklogFactory.getInstance()
        my_backlog = backlog_factory.getCoordinationBacklog(chaptername)
    except Exception as e:
        logging.warning(e)
        local_factory = LocalBacklogFactory.getInstance()
        my_backlog = local_factory.getCoordinationBacklog(chaptername)
        flash('Data from local storage obtained at {}'.format(my_backlog.timestamp))

    sortedby = request.args.get('sortedby') if request.args.get('sortedby') else 'name'
    my_backlog.sort(key=my_backlog.sortDict[sortedby])
    reporter = CoordinationReporter(chaptername, my_backlog)

    return render_template('chapters/dashboard.html',
                           analyser=analyser, reporter=reporter,
                           calendar=agileCalendar, form=form)


@chapters.route("raw/<chaptername>")
@login_required
def raw(chaptername):
    analyser = ChapterAnalyser.fromFile(chaptername)
    analyser.chaptersBook = chaptersBookByName
    try:
        backlog_factory = BacklogFactory.getInstance()
        my_backlog = backlog_factory.getCoordinationBacklog(chaptername)
    except Exception as e:
        logging.warning(e)
        local_factory = LocalBacklogFactory.getInstance()
        my_backlog = local_factory.getCoordinationBacklog(chaptername)
        flash('Data from local storage obtained at {}'.format(my_backlog.timestamp))

    sortedby = request.args.get('sortedby') if request.args.get('sortedby') else 'name'
    my_backlog.sort(key=my_backlog.sortDict[sortedby])
    reporter = CoordinationReporter(chaptername, my_backlog)
    return render_template('chapters/raw.html', analyser=analyser, reporter=reporter, calendar=agileCalendar)


@chapters.route("review/<chaptername>")
@login_required
def review(chaptername):
    analyser = ChapterAnalyser.fromFile(chaptername)
    analyser.chaptersBook = chaptersBookByName
    try:
        backlog_factory = BacklogFactory.getInstance()
        my_backlog = backlog_factory.getCoordinationBacklog(chaptername)
    except Exception as e:
        logging.warning(e)
        local_factory = LocalBacklogFactory.getInstance()
        my_backlog = local_factory.getCoordinationBacklog(chaptername)
        flash('Data from local storage obtained at {}'.format(my_backlog.timestamp))

    sortedby = request.args.get('sortedby') if request.args.get('sortedby') else 'name'
    my_backlog.sort(key=my_backlog.sortDict[sortedby])
    reporter = CoordinationReporter(chaptername, my_backlog)

    return render_template('chapters/review.html', analyser=analyser, reporter=reporter, calendar=agileCalendar)
