__author__ = 'Manuel Escriche'

from .Settings import Settings
settings = Settings()

from .Calendar import AgileCalendar
agileCalendar = AgileCalendar()
calendar = agileCalendar.calendar

from .DeliveryBook import DeliverableBook
deliveryBook = DeliverableBook()

from .NodesBook import NodesBook
tHelpDeskNodesBook = NodesBook()
helpdeskNodesBook = tHelpDeskNodesBook

from .ComponentsBook import ComponentsBook
tComponentsBook = ComponentsBook()
enablersBook = tComponentsBook.enablersByName
enablersBookByName = tComponentsBook.enablersByName
enablersBookByKey = tComponentsBook.enablersByKey

toolsBook = tComponentsBook.toolsByName
toolsBookByName = tComponentsBook.toolsByName
toolsBookByKey = tComponentsBook.toolsByKey

coordinationBook = tComponentsBook.coordinatorsByKey
coordinationBookByName = tComponentsBook.coordinatorsByName
coordinationBookByKey = coordinationBook

helpdeskCompBook = tComponentsBook.helpDeskByName
helpdeskCompBookByName = tComponentsBook.helpDeskByName
helpdeskCompBookByKey = tComponentsBook.helpDeskByKey

accountsDeskBook = tComponentsBook.labAccountsDeskByName
accountsDeskBookByName = tComponentsBook.labAccountsDeskByName
accountsDeskBookByKey = tComponentsBook.labAccountsDeskByKey

workingGroupsBook = tComponentsBook.groupsByName
workingGroupsBookByName = tComponentsBook.groupsByName
workingGroupsBookByKey = tComponentsBook.groupsByKey

labCompBook = tComponentsBook.labCompByName
labCompBookByName = tComponentsBook.labCompByName
labCompBookByKey = tComponentsBook.labCompByKey

labNodesBook = tComponentsBook.labNodesByName
labNodesBookByName = tComponentsBook.labNodesByName
labNodesBookByKey = tComponentsBook.labNodesByKey


from .TTrackerBook import TrackerBook, ChapterBook, WorkGroupBook, HelpDeskBook, AccountsDeskBook, LabBook
trackersBook = TrackerBook()
trackersBookByKey = trackersBook.trackersByKey
trackersBookByName = trackersBook.trackersByName

chaptersBook = ChapterBook()
chaptersBookByName = chaptersBook.chaptersByName
chaptersBookByKey = chaptersBook.chaptersByKey

workGroupBook = WorkGroupBook()
workGroupByName = workGroupBook.workingGroupByName
workGroupByKey = workGroupBook.workingGroupByKey

helpdeskBook = HelpDeskBook()
helpdeskBookByName = helpdeskBook.deskByName
helpdeskBookByKey = helpdeskBook.deskByKey

accountsdeskBook = AccountsDeskBook()
accountsdeskBookByName = accountsdeskBook.deskByName
accountsdeskBookByKey = accountsdeskBook.deskByKey

labsBook = LabBook()
labsBookByName = labsBook.labsByName
labsBookByKey = labsBook.labsByKey
