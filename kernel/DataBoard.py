__author__ = "Manuel Escriche <mev@tid.es>"

from kconfig import settings
from kconfig import enablersBook, helpdeskCompBook
from kconfig import trackersBook, workGroupBook
from kernel.DataFactory import DataFactory

class Data:

    @staticmethod
    def getUrgentDeskUpcoming():
        trackers = ','.join(trackersBook[tracker].keystone for tracker in trackersBook)
        jql = "duedate >= 0d AND duedate <= 7d AND status != Closed AND project in ({})".format(trackers)
        return DataFactory(settings.storeHome).getQueryData('urgent.upcoming', jql)

    @staticmethod
    def getUrgentDeskOverdue():
        trackers = ','.join(trackersBook[tracker].keystone for tracker in trackersBook)
        jql = "duedate < now() AND status != Closed AND project in ({})".format(trackers)
        return DataFactory(settings.storeHome).getQueryData('urgent.upcoming', jql)

    @staticmethod
    def getHelpDesk():
        return DataFactory(settings.storeHome).getTrackerData('HELP')

    @staticmethod
    def getHelpDeskTechChannel():
        techChannel = helpdeskCompBook['Tech']
        return DataFactory(settings.storeHome).getComponentData(techChannel.key)

    @staticmethod
    def getDesk(desk):
        return DataFactory(settings.storeHome).getTrackerData(desk.tracker)
    @staticmethod
    def getFocusedDesk(desk):
        jql = "project = {} AND (resolution = Unresolved OR resolutiondate <= 60d)".format(desk.tracker)
        return DataFactory(settings.storeHome).getQueryData('{}.focused'.format(desk.tracker), jql)
    @staticmethod
    def getChannel(channel):
        return DataFactory(settings.storeHome).getComponentData(channel.id)

    @staticmethod
    def getFocusedChannel(channel):
        jql = "component = {} AND (resolution = Unresolved OR resolutiondate <= 60d)".format(channel.key)
        return DataFactory(settings.storeHome).getQueryData('{}.focused'.format(channel.key), jql)

    @staticmethod
    def getEnabler(enablername):
        cmp_id = enablersBook[enablername]
        return DataFactory(settings.storeHome).getComponentData(cmp_id.key)

    @staticmethod
    def getAccountDeskRequests():
        jql = "project = FLUA AND issuetype = UpgradeAccount"
        return DataFactory(settings.storeHome).getQueryData('account.requests', jql)
    @staticmethod
    def getFocusedAccountDeskRequest():
        jql = "project = FLUA AND issuetype = UpgradeAccount AND (resolution = Unresolved OR resolutiondate <= 60d)"
        return DataFactory(settings.storeHome).getQueryData('account.focusedRequests', jql)

    @staticmethod
    def getAccountChannelRequests(channnel):
        jql = "component = {} AND issuetype = UpgradeAccount".format(channnel.key)
        return DataFactory(settings.storeHome).getQueryData('account.requests', jql)
    @staticmethod
    def getFocusedAccountChannelRequest(channel):
        jql = "component = {} AND issuetype = UpgradeAccount AND (resolution = Unresolved OR resolutiondate <= 60d)".format(channel.key)
        return DataFactory(settings.storeHome).getQueryData('account.focusedRequests', jql)






    @staticmethod
    def getAccountDeskProvisioning():
        jql = "project = FLUA AND issuetype = AccountUpgradeByNode"
        return DataFactory(settings.storeHome).getQueryData('account.provisioning', jql)
    @staticmethod
    def getFocusedAccountDeskProvisioning():
        jql = "project = FLUA AND issuetype = AccountUpgradeByNode AND (resolution = Unresolved OR resolutiondate <= 60d)"
        return DataFactory(settings.storeHome).getQueryData('account.focusedProvisioning', jql)



    @staticmethod
    def getEnablerHelpDesk(enablername):
        enabler = enablersBook[enablername]
        jql = "project = HELP AND issuetype in (Monitor, extRequest) AND HD-Enabler = '{}'".format(enablername)
        return DataFactory(settings.storeHome).getQueryData('helpdesk.enabler-{}'.format(enabler.backlogKeyword), jql)

    @staticmethod
    def getChapterHelpDesk(chaptername):
        jql = "project = HELP AND issuetype in (Monitor, extRequest) AND HD-Chapter = '{}'".format(chaptername)
        return DataFactory(settings.storeHome).getQueryData('helpdesk.chapter-{}'.format(chaptername), jql)

    @staticmethod
    def getNodeHelpDesk(nodename):
        jql = "project = HELP AND issuetype in (Monitor, extRequest) AND HD-Node = '{}'".format(nodename)
        return DataFactory(settings.storeHome).getQueryData('helpdesk.node-{}'.format(nodename), jql)

    @staticmethod
    def getGlobalComponent(key):
        return DataFactory(settings.storeHome).getComponentData(key)

    @staticmethod
    def getChannel(key):
        return DataFactory(settings.storeHome).getComponentData(key)

    @staticmethod
    def getWorkGroups():
        trackers = ','.join([workGroupBook[item].tracker for item in workGroupBook])
        jql = 'project in ({})'.format(trackers)
        return DataFactory(settings.storeHome).getQueryData('workgroups',jql)

    @staticmethod
    def getWorkGroup(key):
        return DataFactory(settings.storeHome).getTrackerData(key)

    @staticmethod
    def getWorkGroupComponent(key):
        return DataFactory(settings.storeHome).getComponentData(key)

    @staticmethod
    def getWorkGroupNoComponent(key):
        return DataFactory(settings.storeHome).getTrackerNoComponentData(key)

    @staticmethod
    def getLab():
        return DataFactory(settings.storeHome).getTrackerData('LAB')

    @staticmethod
    def getLabComponent(cmp):
        return DataFactory(settings.storeHome).getComponentData(cmp.key)


if __name__ == "__main__":
    pass
