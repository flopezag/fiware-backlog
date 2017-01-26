import pickle

import os
from kernel import settings
from kconfig import helpdeskBookByName, labsBookByName
from kernel.DataBoard import Data
from kernel.NM_Aggregates import Deck, WorkBacklog
from kernel.NM_BacklogReporter import BacklogReporter
from kernel.NM_HelpDeskReporter import DeckReporter

__author__ = 'Manuel Escriche'


class LabReporter(BacklogReporter, DeckReporter):
    def __init__(self):
        lab = labsBookByName['Lab']
        backlog = WorkBacklog(*Data.getLab())
        channel = helpdeskBookByName['Main-Help-Desk'].channels['Lab']
        deck = Deck(*Data.getChannel(channel.key))
        BacklogReporter.__init__(self, backlog)
        # super(BacklogReporter).__init__(backlog)
        DeckReporter.__init__(self, deck)
        # super(DeckReporter).__init__(deck)
        self.save()

    def __getstate__(self):
        state = self.__dict__.copy()
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

    def save(self):
        filename = 'FIWARE.LabReporter.pkl'
        longfilename = os.path.join(settings.storeHome, filename)
        with open(longfilename, 'wb') as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)

    @classmethod
    def fromFile(cls):
        filename = 'FIWARE.LabReporter.pkl'
        with open(os.path.join(settings.storeHome, filename), 'rb') as f:
            return pickle.load(f)


if __name__ == "__main__":
    pass
