from datetime import date
from itertools import accumulate
from calendar import monthrange

from collections import Counter
from kernel.IssuesModel import backlogIssuesModel
from kconfig import calendar as FWcalendar
from kconfig import workGroupBook
from kernel.Recorder import Recorder

__author__ = "Manuel Escriche <mev@tid.es>"


class BacklogReporter:
    def __init__(self, backlog):
        self._length = len(backlog)
        self.issueType = backlog.issueType
        self.perspective = backlog.perspective
        self.status = backlog.status
        self.sprint_status = backlog.sprint_status
        self.issueType_graph_data = self._issueType_graph_data(backlog)
        self.perspective_graph_data = self._perspective_graph_data(backlog)
        self.sprint_status_graph_data = self._sprint_status_graph_data(backlog)
        self.burndown_graph_data = self._burndown_graph_data(backlog)
        self.implemented_graph_data = self._implemented_graph_data(backlog)

    def __len__(self):
        return self._length

    def _implemented_graph_data(self, backlog):
        book = FWcalendar.monthBook

        createdIssues = Counter(['{:02d}-{}'.format(issue.created.month, issue.created.year) for issue in backlog])
        createdData = list(accumulate([createdIssues[book[month]] for month in FWcalendar.pastMonths]))

        updatedIssues = Counter(['{:02d}-{}'.format(issue.updated.month, issue.updated.year) for issue in backlog])
        updatedData = list(accumulate([updatedIssues[book[month]] for month in FWcalendar.pastMonths]))

        closedIssues = [issue for issue in backlog if issue.status == 'Closed']
        resolvedIssues = Counter(['{:02d}-{}'.format(issue.resolutionDate.month, issue.resolutionDate.year) for issue in closedIssues])
        resolvedData = list(accumulate([resolvedIssues[book[month]] for month in FWcalendar.pastMonths]))

        finishedIssues = [issue for issue in closedIssues if issue.frame in ('Working On','Implemented')]
        releasedIssues = Counter(['{:02d}-{}'.format(issue.releaseDate.month, issue.releaseDate.year) for issue in finishedIssues])

        progressData = [releasedIssues[book[month]] for month in FWcalendar.pastMonths]
        releasedData = list(accumulate(progressData))

        outdata = dict()
        outdata['categories'] = FWcalendar.timeline
        outdata['ncategories'] = len(FWcalendar.timeline) - 1
        outdata['created'] = dict()
        outdata['created']['type'] = 'spline'
        outdata['created']['name'] = 'Created'
        outdata['created']['data'] = createdData
        outdata['resolved'] = dict()
        outdata['resolved']['type'] = 'spline'
        outdata['resolved']['name'] = 'Resolved'
        outdata['resolved']['data'] = resolvedData
        outdata['updated'] = dict()
        outdata['updated']['type'] = 'spline'
        outdata['updated']['name'] = 'Updated'
        outdata['updated']['data'] = updatedData
        outdata['released'] = dict()
        outdata['released']['type'] = 'spline'
        outdata['released']['name'] = 'Released'
        outdata['released']['data'] = releasedData
        outdata['progress'] = dict()
        outdata['progress']['type'] = 'column'
        outdata['progress']['name'] = 'Progress'
        outdata['progress']['data'] = progressData
        return outdata

    def _issueType_graph_data(self, backlog):
        count = backlog.issueType
        return [[issueType, count[issueType]] for issueType in backlog.issueType ]

    def _perspective_graph_data(self, backlog):
        count = backlog.perspective
        return [[frame, count[frame]] for frame in backlog.Perspectives]

    def _sprint_status_graph_data(self, backlog):
        count = backlog.sprint_status
        return [[status, count[status]] for status in count]

    def _burndown_graph_data(self, backlog):
        issues = [issue for issue in backlog if issue.frame == 'Working On' \
            and issue.issueType in backlogIssuesModel.shortTermTypes]

        closedIssues = Counter([issue.updated.day for issue in issues if issue.status == 'Closed'])
        # print(closedIssued)
        NIssues = len(issues)
        month_length = monthrange(date.today().year, date.today().month)[1]

        data = [(day, closedIssues[day]) for day in range(1, date.today().day+1)]
        # print(data)
        data = zip([item[0] for item in data], accumulate([item[1] for item in data]))
        data = {item[0]: NIssues-item[1] for item in data}
        # print(data)

        n = lambda x: NIssues/month_length if x > 0 else 0
        ref_data = {day : n(day) for day in range(1, month_length+1)}
        ref_data = dict(zip(ref_data.keys(), accumulate(ref_data.values())))
        ref_data = {day : round(abs(NIssues-ref_data[day]), 1) for day in ref_data}
        # print(ref_data)

        cdata = lambda d: data[d] if d in data else 'null'
        outdata = dict()
        outdata['categories'] = [day for day in range(1, month_length+1)]
        outdata['reference'] = dict()
        outdata['reference']['type'] = 'spline'
        outdata['reference']['name'] = 'Reference'
        outdata['reference']['data'] = [ref_data[day] for day in range(1, month_length+1)]
        outdata['reference']['marker'] = {'enabled': 'false'}
        outdata['reference']['dashStyle'] = 'shortdot'
        outdata['actual'] = dict()
        outdata['actual']['type'] = 'spline'
        outdata['actual']['name'] = 'Actual'
        outdata['actual']['data'] = [cdata(day) for day in range(1, date.today().day+1)]
        outdata['closed'] = dict()
        outdata['closed']['type'] = 'column'
        outdata['closed']['name'] = 'Closed'
        outdata['closed']['data'] = [closedIssues[day] for day in range(1, date.today().day+1)]
        return outdata


class WorkGroupReporter(BacklogReporter, Recorder):
    def __init__(self, workgroup, backlog):
        BacklogReporter.__init__(self, backlog)
        Recorder.__init__(self, 'FIWARE.WorkGroupReporter.'+ workgroup.name + '.pkl')
        self.groups = [workgroup.groups[group].name for group in workgroup.groups]
        self.frame_status_graph_data = self._frame_status_graph_data(workgroup, backlog)

        self.composition_graph_data = [[name, len([issue for issue in backlog if workgroup.groups[name].key in issue.component])]
                                       for name in self.groups]
        self.save()

    def _frame_status_graph_data(self, workgroup, backlog):
        frame = 'Working On'
        issues = [issue for issue in backlog if issue.frame == frame and issue.component]

        statuses = sorted(set([issue.status for issue in issues]))
        workgroupIssuesBook = dict()
        for key in workgroup.groups:
            group = workgroup.groups[key]
            workgroupIssuesBook[key] = Counter([issue.status for issue in issues if group.key in issue.component])

        _frame_status_graph_data = []
        for status in statuses:
            status_dict = dict()
            status_dict['name'] = status
            status_dict['data'] = [workgroupIssuesBook[group][status] for group in workgroup.groups]
            _frame_status_graph_data.append(status_dict)
        return _frame_status_graph_data

    @classmethod
    def fromFile(cls, workgroup):
        return super().fromFile('FIWARE.WorkGroupReporter.'+ workgroup.name + '.pkl')


class WorkGroupsReporter(BacklogReporter, Recorder):
    def __init__(self, backlog):
        BacklogReporter.__init__(self,backlog)
        Recorder.__init__(self, 'FIWARE.WorkGroupsReporter.pkl')
        self.workGroups = [workGroupBook[item].name for item in workGroupBook]
        self.composition_graph_data = [[workGroupBook[item].name, len([issue for issue in backlog if issue.project == workGroupBook[item].tracker])]
                                       for item in self.workGroups]
        self.wg_sprint_status_graph_data = self._wg_sprint_status_graph_data(backlog)
        self.save()

    def _wg_sprint_status_graph_data(self, backlog):
        frame = 'Working On'
        issues = [issue for issue in backlog
                  if issue.frame == frame and issue.issueType in backlogIssuesModel.shortTermTypes]

        statuses = sorted(set([issue.status for issue in issues]))

        wgIssuesBook = dict()
        for wgname in workGroupBook:
            workgroup = workGroupBook[wgname]
            wgIssuesBook[wgname] = Counter([issue.status for issue in issues if workgroup.tracker == issue.project ])

        _frame_status_graph_data = []
        for status in statuses:
            status_dict = {}
            status_dict['name'] = status
            status_dict['data'] = [wgIssuesBook[wg][status] for wg in workGroupBook]
            _frame_status_graph_data.append(status_dict)
        return _frame_status_graph_data

    @classmethod
    def fromFile(cls, name):
        return super().fromFile('FIWARE.WorkGroupsReporter.pkl')


class ChapterReporter:
    """
    aggregated of enablers and tools' backlogs and worklists
    """
    def __init__(self):
        pass


if __name__ == "__main__":
    pass
