import logging
from flask import jsonify, request, Response
from functools import wraps
from kconfig import deliveryBook, trackersBook, enablersBook, helpdeskNodesBook, chaptersBook
from kernel.DataBoard import Data
from kernel.NM_Aggregates import EnablerDeck, DevBacklog
from kernel.NM_HelpDeskReporter import DeckReporter
from kernel.NM_BacklogReporter import BacklogReporter
from . import api
from kconfig.parameters import USER, PASSWORD

__author__ = 'Manuel Escriche'


def authentication(api_srv):
    @wraps(api_srv)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth and (auth.username == USER and auth.password == PASSWORD):
            return api_srv(*args, **kwargs)
        else:
            return Response(response="wrong credentials or request configuration in server", status=401)
    return decorated


@api.route('/test')
@authentication
def test_service():
    return jsonify({'output': 'OK'})


@api.route('/enabler/working_mode')
@authentication
def enabler_working_mode():
    book = {item: {'mode': enablersBook[item].mode} for item in enablersBook}
    return jsonify({'book': book})


# param  = request.args.get('param') if request.args.get('param') else None
@api.route('/helpdesk/enabler/<enablername>', methods=['GET'])
@authentication
def enabler_helpdesk(enablername):
    # print(enablername)
    enabler = enablersBook[enablername]
    deck = EnablerDeck(enabler, *Data.getEnablerHelpDesk(enablername))
    reporter = DeckReporter(enabler.chapter, deck)

    try:
        resolution_level = deck.resolution_level
    except ZeroDivisionError:
        resolution_level = None

    return jsonify({'stats': reporter.stats, 'resolution_level': resolution_level})


@api.route('/backlog/enabler/<enablername>', methods=['GET'])
@authentication
def enabler_backlog(enablername):
    # enabler = enablersBook[enablername]
    backlog = DevBacklog(*Data.getEnabler(enablername))
    # reporter = BacklogReporter(backlog)
    return jsonify({'stats': backlog.issueType})


@api.route("/deliveryboard/pending")
@authentication
def deliveryboard_pending():
    return jsonify({'book': {item.id: item.edition_issue.id for item in deliveryBook.scheduled if item.edition_issue}})


@api.route("/trackersbook/all")
@authentication
def trackers_book():
    trackers = ','.join(trackersBook[tracker].keystone for tracker in trackersBook)
    return jsonify({'trackers': trackers})


@api.route("/trackersbook/nodesk")
@authentication
def trackers_book_nodesk():
    trackers = ','.join(trackersBook[tracker].keystone
                        for tracker in trackersBook if trackersBook[tracker].type not in ('ADESK', 'HDESK'))
    return jsonify({'trackers': trackers})


@api.route("/enablersbook")
@authentication
def get_enablersbook():
    book = {item: {'component': enablersBook[item].key,
                   'owner': enablersBook[item].leader,
                   'chapter': enablersBook[item].chapter,
                   'backlog_keyword': enablersBook[item].backlogKeyword} for item in enablersBook}

    return jsonify({'book': book})


@api.route("/nodesbook")
@authentication
def get_nodesbook():
    book = {item: {'support': helpdeskNodesBook[item].support} for item in helpdeskNodesBook}
    return jsonify({'book': book})


@api.route("/chaptersbook")
@authentication
def get_chaptersbook():
    # _book = chaptersBook
    book = {item: {'coordination_key': chaptersBook[item].coordination.key,
                   'leader': chaptersBook[item].coordination.leader} for item in chaptersBook}

    return jsonify({'book': book})
