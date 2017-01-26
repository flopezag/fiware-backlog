import logging

from . import settings
from kernel.IssuesList import IssuesFactory
from kernel.Backlog import BacklogFactory
from kconfig import chaptersBook, helpdeskBookByName, workGroupByName, accountsdeskBookByName
from kconfig.ComponentsBook import ComponentLeaders
from kernel.DataFactory import DataEngine
from kernel.Reporter import ChapterReporter, EnablersReporter, ChaptersReporter
from kernel.Analyser import ChaptersAnalyser, ChapterAnalyser, EnablersAnalyser
from kernel.DataBoard import Data
from kernel.NM_Aggregates import DeskDeck, WorkGroupBacklog, DevBacklog
from kernel.NM_HelpDeskReporter import DeskReporter
from kernel.NM_BacklogReporter import WorkGroupReporter, WorkGroupsReporter
from kernel.NM_AccountsDeskReporter import ADeck
from kernel.NM_AccountsDeskReporter import DeskReporter as aDeskReporter
from kernel.NM_LabReporter import LabReporter

__author__ = "Manuel Escriche <mev@tid.es>"


def updateTrackersLocalStorage():
    try:
        DataEngine.snapshot(settings.storeHome)
        logging.debug("Created TrackerStore.snapshot")
    except Exception as error:
        logging.exception(error)


def updateBacklogsLocalStorage():
    try:
        backlogFactory = BacklogFactory()
    except Exception as error:
        logging.exception(error)
        return

    try:
        backlog = backlogFactory.getChaptersBacklog()
    except Exception as error:
        logging.exception(error)
    else:
        reporter = ChaptersReporter(backlog)
        chaptersAnalyser = ChaptersAnalyser(reporter)
        logging.debug("Created Chapters analyser")
        chaptersAnalyser.save()
        chaptersAnalyser.clean()
    #
    for chaptername in chaptersBook:
        try:
            backlog = backlogFactory.getChapterBacklog(chaptername)
        except Exception as error:
            logging.exception(error)
        else:
            reporter = ChapterReporter(chaptername, backlog)
            analyser = ChapterAnalyser(reporter)
            analyser.save()
            analyser.clean()

    try:
        backlog = backlogFactory.getEnablersBacklog()
    except Exception as error:
        logging.exception(error)
    else:
        reporter = EnablersReporter(backlog)
        enablersAnalyser = EnablersAnalyser(reporter)
        logging.debug("Created enablers analyser")
        enablersAnalyser.save()
        enablersAnalyser.clean()


def updateLab():
    try:
        lab = LabReporter()
        logging.debug("Created Lab Reporter")
    except Exception as error:
        logging.exception(error)


def updateIssuesLocalStorage():
    try:
        factory = IssuesFactory.getInstance()
    except Exception as error:
        logging.exception(error)
        return
    for topic in ('upcoming', 'impeded', 'blockers', 'overdue', 'aged'):
        try:
            issues = factory.getUrgentIssues(topic)
            logging.debug("Created urgent issues for topic {}".format(topic))
        except Exception as error:
            logging.exception(error)


    for topic in ('main', 'main.lab', 'main.tech', 'coaches', 'tools'):
        try:
            issues = factory.getUnresolvedHelpDeskIssues(topic)
            logging.debug("Created unresolved Help Desk Issues for topic {}".format(topic))
        except Exception as error:
            logging.exception(error)


    for topic in ('main', 'main.lab', 'main.tech', 'coaches', 'tools'):
        issues = factory.getAllHelpDeskIssues(topic)

    for topic in ('lab.accounts',):
        issues = factory.getIssuesFromRequest(topic)


def updateComponentsLeaders():
    try:
        book = ComponentLeaders()
        logging.debug("Updated components leaders")
    except Exception as error:
        logging.exception(error)


def updateHelpDesk():
    for deskname in helpdeskBookByName:
        desk = helpdeskBookByName[deskname]
        try:
            data = DeskDeck(desk, *Data.getDesk(desk))
            reporter = DeskReporter(desk, data)
            logging.debug("Updating deskReporter {}".format(desk.name))
        except Exception as error:
            logging.exception(error)


def updateAccountsDesk():
    for deskname in accountsdeskBookByName:
        desk = accountsdeskBookByName[deskname]
        try:
            data = ADeck(*Data.getAccountDeskRequests())
            deskReporter = aDeskReporter(desk, data)
            logging.debug("Updated deskReporter {}".format(desk.name))
        except Exception as error:
            logging.exception(error)


def updateWorkGroups():
    for group in workGroupByName:
        workgroup = workGroupByName[group]
        try:
            #backlog = WorkGroupBacklog(*Data.getWorkGroup(workgroup.key))
            backlog = DevBacklog(*Data.getWorkGroup(workgroup.key))
            reporter = WorkGroupReporter(workgroup, backlog)
            logging.debug("Updated workGroupReporter {}".format(workgroup.name))
        except Exception as error:
            logging.exception(error)

    try:
        backlog = WorkGroupBacklog(*Data.getWorkGroups())
        reporter = WorkGroupsReporter(backlog)
        logging.debug("Updated workGroupsReporter")
    except Exception as error:
        logging.exception(error)


if __name__ == "__main__":
    pass
