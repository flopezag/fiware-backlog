__author__ = 'Manuel Escriche'

import logging
from flask import jsonify, request, Response
from functools import wraps
from kconfig import deliveryBook, trackersBook, enablersBook, helpdeskNodesBook, chaptersBook
from kernel.DataBoard import Data
from kernel.NM_Aggregates import EnablerDeck, DevBacklog
from kernel.NM_HelpDeskReporter import DeckReporter
from kernel.NM_BacklogReporter import BacklogReporter
from . import api


master_token = "adc842f790105942e095f5f77484ffa8242a2ec3"
def authentication(api_srv):
    @wraps(api_srv)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth and (auth.username == 'api' and auth.password == master_token):
            return api_srv(*args, **kwargs)
        else:
            return Response(response="wrong credentials or request configuration in server", status=401)
    return decorated

@api.route('/test')
@authentication
def test_service():
    return jsonify({'output':'OK'})


@api.route('/enabler/working_mode')
@authentication
def enabler_working_mode():
    book = {item:{'mode': enablersBook[item].mode} for item in enablersBook}
    return jsonify({'book':book})

#param  = request.args.get('param') if request.args.get('param') else None
@api.route('/helpdesk/enabler/<enablername>', methods=['GET'])
@authentication
def enabler_helpdesk(enablername):
    #print(enablername)
    enabler = enablersBook[enablername]
    deck = EnablerDeck(enabler, *Data.getEnablerHelpDesk(enablername))
    reporter = DeckReporter(deck)
    try:resolution_level = deck.resolution_level
    except ZeroDivisionError: resolution_level = None
    return jsonify({'stats': reporter.stats, 'resolution_level': resolution_level})

@api.route('/backlog/enabler/<enablername>', methods=['GET'])
@authentication
def enabler_backlog(enablername):
    #enabler = enablersBook[enablername]
    backlog = DevBacklog(*Data.getEnabler(enablername))
    #reporter = BacklogReporter(backlog)
    return jsonify({'stats': backlog.issueType})

@api.route("/deliveryboard/pending")
@authentication
def deliveryboard_pending():
    return jsonify({'book': {item.id: item.edition_issue.id for item in deliveryBook.scheduled if item.edition_issue}})

@api.route("/trackersbook/all")
@authentication
def trackersbook():
    trackers = ','.join(trackersBook[tracker].keystone for tracker in trackersBook)
    return jsonify({'trackers': trackers})

@api.route("/trackersbook/nodesk")
@authentication
def trackersbookNodesk():
    trackers = ','.join(trackersBook[tracker].keystone
                        for tracker in trackersBook if trackersBook[tracker].type not in ('ADESK', 'HDESK') )
    return jsonify({'trackers': trackers})

@api.route("/enablersbook")
@authentication
def get_enablersBook():
    book = {item:{'component': enablersBook[item].key,
                  'owner':enablersBook[item].leader,
                  'chapter': enablersBook[item].chapter,
                  'backlog_keyword':enablersBook[item].backlogKeyword} for item in enablersBook}
    return jsonify({'book':book})

@api.route("/nodesbook")
@authentication
def get_nodesBook():
    book = {item:{'support':helpdeskNodesBook[item].support} for item in helpdeskNodesBook}
    return jsonify({'book':book})

@api.route("/chaptersbook")
@authentication
def get_chaptersBook():
    #_book = chaptersBook
    book = {item:{'coordination_key':chaptersBook[item].coordination.key,
                  'leader':chaptersBook[item].coordination.leader} for item in chaptersBook}
    return jsonify({'book':book})