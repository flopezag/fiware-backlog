import os
from xml.etree import ElementTree as ET
from datetime import date, datetime
from collections import OrderedDict
from . import calendar
from kernel.Jira import JIRA

__author__ = "Manuel Escriche <mev@tid.es>"


class Workflow:
    """Workflow used for deliverables"""
    """ Statuses: Planned, Scheduled, Delivered, Closed"""
    """ Resolutions: Accepted, Rejected-NReq, Planned-NReq """
    __instance = None

    def __init__(self):
        if Workflow.__instance: return
        self.scheduled = ('Scheduled',)
        self.active = ('Planned',) + self.scheduled
        self.delivered = ('Delivered',)
        self.closed = ('Accepted',)
        self.excluded = ('Rejected-NReq', 'Planned-NReq', 'Canceled')
        self.submitted = ('Scheduled', 'Delivered', 'Accepted', 'Rejected-NReq')
        self.assessed = ('Accepted', 'Rejected-NReq')
        Workflow.__instance = self
    @property
    def open(self): return self.active + self.delivered
    @property
    def resolved(self): return self.closed + self.excluded
    @property
    def status(self): return self.active + self.delivered + self.resolved
    @property
    def pending(self):
        return self.active


workflow = Workflow()

class Issue:
    jira = JIRA()
    def __init__(self, id):
        self.id = id
        self.url = 'http://{}/browse/{}'.format('jira.fiware.org', self.id)
        self.status = Issue.jira.getIssue(self.id)['fields']['status']['name']


class Deliverable:
    jira = JIRA()
    def __init__(self, deliverable):
        tagsList = [child.tag for child in deliverable]
        self.id = deliverable.get('id')
        self.title = deliverable.find('title').text
        self.n_month = deliverable.find('planned_month').text
        self.owner = deliverable.find('owner').text if 'owner' in tagsList else "Unknown"
        self.leader = deliverable.find('leader').text if 'leader' in tagsList else "Unknown"
        self.status = deliverable.find('status').text if 'status' in tagsList else "Planned"
        try: self.delivery_issue = Issue(deliverable.find('delivery_issue').text)
        except Exception: self.delivery_issue = None
        try : self.edition_issue = Issue(deliverable.find('edition_issue').text)
        except Exception: self.edition_issue = None
        self.resolution = deliverable.find('resolution').text if 'resolution' in tagsList else "Undefined"
        self.deadline = calendar.getMonth(self.month)[1]
        self.submissions = list()
        if 'submission' in tagsList:
            for _date in deliverable.find('submission').findall('date'):
                self.submissions.append(datetime.strptime(_date.text, '%d-%m-%Y').date())
                #self.submissions.append(date(int(__date[6:11]), int(__date[3:5]), int(__date[0:2])))
    @property
    def month(self):
        return int(self.n_month[1:])

    @property
    def first_submission(self):
        if len(self.submissions):
            return min(self.submissions)
        else:
            return None

    @property
    def last_submission(self):
        if len(self.submissions) > 0:
            return max(self.submissions)
        else:
            return None

    @property
    def delay(self):
        return (date.today() - self.deadline).days

    def __str__(self):
        return "{0.id!r}, {0.title!r}, {0.owner!r}-{0.leader!r}, {0.status!r}, {0.n_month!r}, {0.deadline!r}, {0.submissions!r}".format(self)

    def __repr__(self):
        return "Delivery Record ({0.id!r}, {0.title!r}, {0.owner!r}-{0.leader!r}, {0.status!r}, {0.n_month!r}, {0.deadline!r}, {0.submissions!r})".format(self)

    @property
    def isDelayed(self):
        assert(self.status in workflow.active)
        return True if date.today() > self.deadline else False

    @property
    def isUpcoming(self):
        assert(self.status in workflow.active)
        return True if 0 <= (self.deadline - date.today()).days < 45 else False

    @property
    def isPending(self):
        return True if self.status in workflow.active else False

    @property
    def isDelivered(self):
        return True if len(self.submissions) > 0 else False


class DeliverableBook(OrderedDict):
    def __init__(self):
        super().__init__()
        self.codeHome = os.path.dirname(os.path.abspath(__file__))
        self.configHome = os.path.join(os.path.split(self.codeHome)[0], 'site_config')
        xmlfile = os.path.join(self.configHome, 'Deliverables.xml')
        #print(xmlfile)
        tree = ET.parse(xmlfile)
        root = tree.getroot()
        for _deliverable in root.findall('deliverable'):
            name = _deliverable.get('id')
            self[name] = Deliverable(_deliverable)
            #print(self[name])

    @property
    def dashboard(self):
        #last two deliveries
        deliveries = [item for item in self.values() if item.status in workflow.delivered]
        deliveries.sort(key=lambda e:e.last_submission, reverse=True)
        _dashboard = deliveries[:4]
        _dashboard.reverse()
        #planned
        working = [item for item in self.values() if item.status in workflow.active]
        delayed = [item for item in working  if item.isDelayed]
        #print('delayed=', delayed)
        _dashboard += delayed
        upcoming = [item for item in working if item.isUpcoming]
        #print('upcoming=', upcoming)
        _dashboard += upcoming
        _dashboard.sort(key=lambda e:e.deadline)
        return _dashboard

    @property
    def delivered(self):
        return [item for item in self.values() if item.status in workflow.delivered]

    @property
    def scheduled(self):
        return [item for item in self.values() if item.isPending]

#deliveryBook = DeliverableBook()

if __name__ == "__main__":
    pass