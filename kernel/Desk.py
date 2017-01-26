__author__ = "Manuel Escriche <mev@tid.es>"

import statistics
from datetime import date, datetime
from itertools import accumulate
from collections import Counter
from . import calendar as FWcalendar
from kconfig import tComponentsBook
from kconfig import tHelpDeskNodesBook


class ChannelDeskReporter:
    def __init__(self, issuesList, title, channel):
        self.title = title
        self.issues = issuesList
        self.channel = channel

    @property
    def leader(self):
        return tComponentsBook[self.channel].leader

    @property
    def resolutionTime_graph_data(self):
        count = Counter([issue.age for issue in self.issues])
        pending_count = Counter([issue.age for issue in self.issues if not issue.resolved ])

        _min,_max = min(count.keys()), max(count.keys())
        data = [count[k] for k in range(_min,_max+1)]

        pending_data = [pending_count[k] for k in range(_min,_max+1)]

        recent_count = Counter([issue.age for issue in self.issues if (date.today() - issue.created).days <= 60 ])
        recent_data = [recent_count[k] for k in range(_min,_max+1)]

        outdata = {}
        outdata['categories'] = [k for k in range(_min,_max+1)]
        outdata['time'] = dict()
        outdata['time']['type'] = 'column'
        outdata['time']['name'] = 'Mature issues'
        outdata['time']['data'] = data
        outdata['age'] = dict()
        outdata['age']['type'] = 'column'
        outdata['age']['name'] = "Pending issues"
        outdata['age']['color'] = '#ff4040'
        outdata['age']['data'] = pending_data
        outdata['recent'] = dict()
        outdata['recent']['type'] = 'column'
        outdata['recent']['name'] = "Recent issues"
        outdata['recent']['color'] = 'green'
        outdata['recent']['data'] = recent_data
        return outdata

    @property
    def stats(self):
        #count = Counter([issue.age for issue in self.issues])
        data = [issue.age for issue in self.issues]
        outdata = {}
        outdata['n'] = len(data)
        try:
            outdata['min'] = min(data)
        except: pass
        try:
            outdata['max'] = max(data)
        except: pass
        try:
            outdata['mean'] = statistics.mean(data)
        except: pass
        try:
            outdata['median'] = statistics.median(data)
        except: pass
        try:
            outdata['mode'] = statistics.mode(data)
        except: pass
        try:
            outdata['stdev'] = statistics.stdev(data)
        except: pass
        try:
            outdata['variance'] = statistics.variance(data)
        except: pass
        return outdata

    @property
    def statsOfPending(self):
        #count = Counter([issue.age for issue in self.issues])
        data = [issue.age for issue in self.issues if not issue.resolved]
        outdata = {}
        outdata['n'] = len(data)
        try:
            outdata['min'] = min(data)
        except: pass
        try:
            outdata['max'] = max(data)
        except: pass
        try:
            outdata['mean'] = statistics.mean(data)
        except: pass
        try:
            outdata['median'] = statistics.median(data)
        except: pass
        try:
            outdata['mode'] = statistics.mode(data)
        except: pass
        try:
            outdata['stdev'] = statistics.stdev(data)
        except: pass
        try:
            outdata['variance'] = statistics.variance(data)
        except: pass
        return outdata

    @property
    def statsOfRecent(self):
        #count = Counter([issue.age for issue in self.issues])
        data = [issue.age for issue in self.issues if (date.today() - issue.created).days <= 60]
        outdata = {}
        outdata['n'] = len(data)
        try:
            outdata['min'] = min(data)
        except: pass
        try:
            outdata['max'] = max(data)
        except: pass
        try:
            outdata['mean'] = statistics.mean(data)
        except: pass
        try:
            outdata['median'] = statistics.median(data)
        except: pass
        try:
            outdata['mode'] = statistics.mode(data)
        except: pass
        try:
            outdata['stdev'] = statistics.stdev(data)
        except: pass
        try:
            outdata['variance'] = statistics.variance(data)
        except: pass
        return outdata


    @property
    def achievement_graph_data(self):
        color = {'Resolved':'#bada55', 'Pending':'#ff4040'}
        value = { True: 'Resolved', False:'Pending'}
        count = Counter([value[issue.resolved != None] for issue in self.issues])
        return [{'name':_type, 'y': count[_type], 'color': color[_type]} for _type in count]

    @property
    def evolution_graph_data(self):
        book = FWcalendar.monthBook

        createdIssues = Counter(['{:02d}-{}'.format(issue.created.month, issue.created.year) for issue in self.issues])
        createdData = list(accumulate([createdIssues[book[month]] for month in FWcalendar.pastMonths]))

        issues = [issue for issue in self.issues if issue.resolved]
        resolvedIssues = Counter(['{:02d}-{}'.format(issue.resolved.month, issue.resolved.year) for issue in issues])
        progressData = [resolvedIssues[book[month]] for month in FWcalendar.pastMonths]
        resolvedData = list(accumulate(progressData))

        outdata = {}
        outdata['categories'] = FWcalendar.timeline
        outdata['created'] = dict()
        outdata['created']['type'] = 'spline'
        outdata['created']['name'] = 'Created'
        outdata['created']['data'] = createdData
        outdata['resolved'] = dict()
        outdata['resolved']['type'] = 'spline'
        outdata['resolved']['name'] = 'Resolved'
        outdata['resolved']['data'] = resolvedData
        outdata['progress'] = dict()
        outdata['progress']['type'] = 'column'
        outdata['progress']['name'] = 'Progress'
        outdata['progress']['data'] = progressData
        outdata['summary'] = dict()
        outdata['summary']['type'] = 'pie'
        outdata['summary']['name'] = 'Status'
        outdata['summary']['data'] = [{'name': 'Resolved', 'y': resolvedData[-1], 'color': 'Highcharts.getOptions().colors[1]' },
                                      {'name': 'Pending', 'y': createdData[-1] - resolvedData[-1], 'color': '#ff4040'}]
        outdata['summary']['center'] = [70, 60]
        outdata['summary']['size'] = 80
        outdata['summary']['dataLabels'] = {'enabled': 'true',
                                            'format': '<b>{point.name}</b>: <br/> {point.y} ({point.percentage:.1f}%)'}

        return outdata


class TrackerDeskReporter:

    def __init__(self, issuesList, tracker, title):
        #print(tracker)
        self.title = title
        self.issuesList = issuesList
        self.issues = issuesList
        self.components = [comp for comp in tComponentsBook if tComponentsBook[comp].tracker == tracker]
        self.nodes = iter(tHelpDeskNodesBook)
        self.compNames = {cmp: tComponentsBook[cmp].name for cmp in self.components}
        #print(self.components)
        self._issuesByCompDict = {cmp: [issue for issue in issuesList if tComponentsBook[cmp].key in issue.components]
                            for cmp in self.components }
        #for cmp in self.components:
        #    print(cmp, len(self._issuesDict[cmp]))
        self._issuesByNodeDict = {node: [issue for issue in issuesList if issue.assignee in tHelpDeskNodesBook[node].workers]
                                  for node in tHelpDeskNodesBook}
        self.__cmp = None
        self.__node = None

    def setIssues(self, cmp):
        self.__cmp = cmp
        self.issues = self._issuesByCompDict[cmp]

    def setNodeIssues(self, node):
        self.__node = node
        self.issues = self._issuesByNodeDict[node]

    @property
    def cmpLeader(self):
        return tComponentsBook[self.__cmp].leader

    @property
    def resolutionTime_graph_data(self):
        count = Counter([issue.age for issue in self.issues])
        pending_count = Counter([issue.age for issue in self.issues if not issue.resolved ])
        _min,_max = min(count.keys()), max(count.keys())
        data = [count[k] for k in range(_min,_max+1)]
        pending_data = [pending_count[k] for k in range(_min,_max+1)]

        recent_count = Counter([issue.age for issue in self.issues
                                if issue.resolved and (date.today() - issue.created).days <= 60 ])
        recent_data = [recent_count[k] for k in range(_min,_max+1)]

        outdata = {}
        outdata['categories'] = [k for k in range(_min,_max+1)]
        outdata['time'] = dict()
        outdata['time']['type'] = 'column'
        outdata['time']['name'] = 'Mature issues'
        outdata['time']['data'] = data
        outdata['age'] = dict()
        outdata['age']['type'] = 'column'
        outdata['age']['name'] = "Pending issues"
        outdata['age']['color'] = '#ff4040'
        outdata['age']['data'] = pending_data
        outdata['recent'] = dict()
        outdata['recent']['type'] = 'column'
        outdata['recent']['name'] = "Recent issues"
        outdata['recent']['color'] = 'green'
        outdata['recent']['data'] = recent_data
        return outdata

    @property
    def stats(self):
        #count = Counter([issue.age for issue in self.issues])
        data = [issue.age for issue in self.issues]
        outdata = {}
        outdata['n'] = len(data)
        try:
            outdata['min'] = min(data)
        except: pass
        try:
            outdata['max'] = max(data)
        except: pass
        try:
            outdata['mean'] = statistics.mean(data)
        except: pass
        try:
            outdata['median'] = statistics.median(data)
        except: pass
        try:
            outdata['mode'] = statistics.mode(data)
        except: pass
        try:
            outdata['stdev'] = statistics.stdev(data)
        except: pass
        try:
            outdata['variance'] = statistics.variance(data)
        except: pass
        return outdata

    @property
    def statsOfPending(self):
        #count = Counter([issue.age for issue in self.issues])
        data = [issue.age for issue in self.issues if not issue.resolved]
        outdata = {}
        outdata['n'] = len(data)
        try:
            outdata['min'] = min(data)
        except: pass
        try:
            outdata['max'] = max(data)
        except: pass
        try:
            outdata['mean'] = statistics.mean(data)
        except: pass
        try:
            outdata['median'] = statistics.median(data)
        except: pass
        try:
            outdata['mode'] = statistics.mode(data)
        except: pass
        try:
            outdata['stdev'] = statistics.stdev(data)
        except: pass
        try:
            outdata['variance'] = statistics.variance(data)
        except: pass
        return outdata

    @property
    def statsOfRecent(self):
        #count = Counter([issue.age for issue in self.issues])
        data = [issue.age for issue in self.issues if (date.today() - issue.created).days <= 60]
        outdata = {}
        outdata['n'] = len(data)
        try:
            outdata['min'] = min(data)
        except: pass
        try:
            outdata['max'] = max(data)
        except: pass
        try:
            outdata['mean'] = statistics.mean(data)
        except: pass
        try:
            outdata['median'] = statistics.median(data)
        except: pass
        try:
            outdata['mode'] = statistics.mode(data)
        except: pass
        try:
            outdata['stdev'] = statistics.stdev(data)
        except: pass
        try:
            outdata['variance'] = statistics.variance(data)
        except: pass
        return outdata

    @property
    def achievement_graph_data(self):
        color = {'Resolved':'#bada55', 'Pending':'#ff4040'}
        value = { True: 'Resolved', False:'Pending'}
        count = Counter([value[issue.resolved != None] for issue in self.issues])
        return [{'name':_type, 'y': count[_type], 'color': color[_type]} for _type in count]

    @property
    def evolution_graph_data(self):
        book = FWcalendar.monthBook

        createdIssues = Counter(['{:02d}-{}'.format(issue.created.month, issue.created.year) for issue in self.issues])
        createdData = list(accumulate([createdIssues[book[month]] for month in FWcalendar.pastMonths]))

        issues = [issue for issue in self.issues if issue.resolved]
        resolvedIssues = Counter(['{:02d}-{}'.format(issue.resolved.month, issue.resolved.year) for issue in issues])
        progressData = [resolvedIssues[book[month]] for month in FWcalendar.pastMonths]
        resolvedData = list(accumulate(progressData))

        outdata = {}
        outdata['categories'] = FWcalendar.timeline
        outdata['created'] = dict()
        outdata['created']['type'] = 'spline'
        outdata['created']['name'] = 'Created'
        outdata['created']['data'] = createdData
        outdata['resolved'] = dict()
        outdata['resolved']['type'] = 'spline'
        outdata['resolved']['name'] = 'Resolved'
        outdata['resolved']['data'] = resolvedData
        outdata['progress'] = dict()
        outdata['progress']['type'] = 'column'
        outdata['progress']['name'] = 'Progress'
        outdata['progress']['data'] = progressData
        outdata['summary'] = dict()
        outdata['summary']['type'] = 'pie'
        outdata['summary']['name'] = 'Status'
        outdata['summary']['data'] = [{'name': 'Resolved', 'y': resolvedData[-1], 'color': 'Highcharts.getOptions().colors[1]' },
                                      {'name': 'Pending', 'y': createdData[-1] - resolvedData[-1], 'color': '#ff4040'}]
        outdata['summary']['center'] = [70, 60]
        outdata['summary']['size'] = 80
        outdata['summary']['dataLabels'] = {'enabled': 'true',
                                            'format': '<b>{point.name}</b>: <br/> {point.y} ({point.percentage:.1f}%)'}

        return outdata


if __name__ == "__main__":
    pass