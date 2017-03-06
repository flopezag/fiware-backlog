__author__ = 'Manuel Escriche'

from kernel.NM_Issue import AccountRequest, AccountProvision
from kconfig.TTrackerBook import accountsDeskBookByName
from kernel.NM_Aggregates import _Deck
from kernel.Recorder import Recorder
from kernel.NM_HelpDeskReporter import DeckReporter
from kernel.DataBoard import Data

_IssueTypes = {'UpgradeAccount': AccountRequest,
               'AccountUpgradeByNode': AccountProvision}

class ADeck(_Deck):
    _issueTypes = ('UpgradeAccount','AccountUpgradeByNode')

    def __init__(self, data, timestamp, source):
        super().__init__()
        self.data = data
        self.timestamp = timestamp
        self.source = source
        for item in data:
            _type = item['fields']['issuetype']['name']
            if not _type in ADeck._issueTypes: continue
            try:
                self.append(_IssueTypes[_type](item))
            except Exception:
                raise Exception('Error while creating issue')


class ChannelDeck(ADeck):
    '''External help desk channel'''
    def __init__(self, channel, data, timestamp, source):
        self.channel = channel
        super().__init__(data, timestamp, source)


class ChannelReporter(DeckReporter, Recorder):
    def __init__(self, channel, deck):
        self.channel = channel
        DeckReporter.__init__(self, channel.name, deck)
        Recorder.__init__(self, 'FIWARE.AccChannelReporter.' + channel.name + '.pkl')
        self.save()

    @classmethod
    def fromFile(cls, channel):
        return super().fromFile('FIWARE.AccChannelReporter.' + channel.name + '.pkl')


class DeskReporter(DeckReporter, Recorder):
    def __init__(self, desk, deck):
        self.desk = desk
        DeckReporter.__init__(self, deck)
        Recorder.__init__(self,'FIWARE.DeskReporter.' + desk.name + '.pkl')
        value = lambda x: x if x else 'null'
        reporters = dict()
        for channelname in desk.channels:
            channel = accountsDeskBookByName[channelname]
            data, timestamp, source = Data.getChannel(channel.key)
            channeldeck = ChannelDeck(channel, data, timestamp, source)
            reporters[channelname] = ChannelReporter(channel, channeldeck)

        self._composition_data = dict()
        self._composition_data['categories'] = [channel for channel in desk.channels]
        self._composition_data['all'] = [[channel, len(reporters[channel])] for channel in desk.channels]
        self._composition_data['veryrecent'] = [reporters[channel].statsOfVeryRecent['n'] for channel in desk.channels]
        self._composition_data['pending'] = [reporters[channel].statsOfPending['n'] for channel in desk.channels]
        self._composition_data['vveryrecent'] = [[channel, reporters[channel].statsOfVeryRecent['n']] for channel in desk.channels]
        self._composition_data['ppending'] = [[channel, reporters[channel].statsOfPending['n']] for channel in desk.channels]


        self._behaviour_data = dict()
        self._behaviour_data['categories'] = [channel for channel in desk.channels]
        self._behaviour_data['all'] = [value(reporters[channel].stats['mean']) for channel in desk.channels]
        self._behaviour_data['recent'] = [value(reporters[channel].statsOfRecent['mean']) for channel in desk.channels]
        self._behaviour_data['veryrecent'] = [value(reporters[channel].statsOfVeryRecent['mean']) for channel in desk.channels]
        self._behaviour_data['pending'] = [value(reporters[channel].statsOfPending['mean']) for channel in desk.channels]

        self.save()

    @property
    def composition_graph(self):
        return self._composition_data
    @property
    def behaviour_graph(self):
        return self._behaviour_data

    @classmethod
    def fromFile(cls, desk):
        return super().fromFile('FIWARE.DeskReporter.'+ desk.name +'.pkl')


if __name__ == "__main__":
    pass
