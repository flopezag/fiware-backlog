import os
import re
import pickle
from operator import attrgetter
from datetime import datetime
from collections import namedtuple
from kconfig import settings

__author__ = "Manuel Escriche <mev@tid.es>"


class Analyser:
    def __init__(self, reporter):
        self.issueType = reporter.issueType
        self.perspective = reporter.perspective
        self.status = reporter.status
        self.sprint_status = reporter.sprint_status
        self.issueType_graph_data = reporter.issueType_graph_data
        self.perspective_graph_data = reporter.perspective_graph_data
        self.sprint_status_graph_data = reporter.sprint_status_graph_data
        self.errors_graph_data = reporter.errors_graph_data
        self.burndown_graph_data = reporter.burndown_graph_data
        self.implemented_graph_data = reporter.implemented_graph_data
        self.length = reporter.length

    def __getstate__(self):
        state = self.__dict__.copy()
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

    def cleanList(self, filelist):
        filelist.sort(key=attrgetter('day', 'time'), reverse=True)
        filename = filelist[0].filename
        #print('last file created :', filename)
        toRemove = filelist[5:]
        #print('files to remove')
        if len(toRemove) > 0:
            for item in toRemove:
                os.remove(os.path.join(settings.storeHome, item.filename))
                #print('\t>',item.filename)


class ChapterAnalyser(Analyser):
    def __init__(self, reporter):
        super().__init__( reporter)
        self.chaptername = reporter.chaptername
        self.enablers = reporter.enablers
        self.tools = reporter.tools
        self.coordination = reporter.coordination
        self.frame_status_graph_data = reporter.frame_status_graph_data
        self.tools_frame_status_graph_data = reporter.tools_frame_status_graph_data

    def save(self):
        timestamp = datetime.now().strftime("%Y%m%d-%H%M")
        filename = 'FIWARE.backlog.chapterAnalyser.'+ self.chaptername +'.'+ timestamp + '.pkl'
        longFilename = os.path.join(settings.storeHome, filename)
        #print('W: {0}'.format(longFilename))

        with open(longFilename, 'wb') as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)

    def clean(self):
        fileList = os.listdir(settings.storeHome)
        mfilter = re.compile(r'\bFIWARE[.]backlog[.]chapterAnalyser[.](?P<chapter>\w+)[.](?P<day>\d{8})[-](?P<time>\d{4})[.]pkl\b')
        record = namedtuple('record', 'filename, day, time')
        filelist = [record(mfilter.match(f).group(0),
                           mfilter.match(f).group('day'),
                           mfilter.match(f).group('time')) for f in fileList if mfilter.match(f)
                    if mfilter.match(f).group('chapter') == self.chaptername]
        super().cleanList(filelist)

    @classmethod
    def fromFile(cls, chaptername):
        fileList = os.listdir(settings.storeHome)
        mfilter = re.compile(r'\bFIWARE[.]backlog[.]chapterAnalyser[.](?P<chapter>\w+)[.](?P<day>\d{8})[-](?P<time>\d{4})[.]pkl\b')
        record = namedtuple('record', 'filename, day, time')
        filelist = [record(mfilter.match(f).group(0),
                           mfilter.match(f).group('day'),
                           mfilter.match(f).group('time')) for f in fileList if mfilter.match(f)
                    if mfilter.match(f).group('chapter') == chaptername]
        filelist.sort(key=attrgetter('day', 'time'), reverse=True)
        filename = filelist[0].filename
        with open(os.path.join(settings.storeHome, filename), 'rb') as f:
            return pickle.load(f)


class ChaptersAnalyser(Analyser):
    def __init__(self, reporter):
        super().__init__(reporter)
        self.chapters_sprint_status_graph_data = reporter.chapters_sprint_status_graph_data
        self.chapters_errors_graph_data = reporter.chapters_errors_graph_data
        self.chapters = reporter.chapters
        self.nChapters = reporter.nChapters
    def save(self):
        timestamp = datetime.now().strftime("%Y%m%d-%H%M")
        filename = 'FIWARE.backlog.chaptersAnalyser.' + timestamp + '.pkl'
        longFilename = os.path.join(settings.storeHome, filename)
        #print('W: {0}'.format(longFilename))
        with open(longFilename, 'wb') as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)

    def clean(self):
        fileList = os.listdir(settings.storeHome)
        mfilter = re.compile(r'\bFIWARE[.]backlog[.]chaptersAnalyser[.](?P<day>\d{8})[-](?P<time>\d{4})[.]pkl\b')
        record = namedtuple('record', 'filename, day, time')
        filelist = [record(mfilter.match(f).group(0),
                           mfilter.match(f).group('day'),
                           mfilter.match(f).group('time')) for f in fileList if mfilter.match(f)]
        super().cleanList(filelist)

    @classmethod
    def fromFile(cls):
        fileList = os.listdir(settings.storeHome)
        mfilter = re.compile(r'\bFIWARE[.]backlog[.]chaptersAnalyser[.](?P<day>\d{8})[-](?P<time>\d{4})[.]pkl\b')
        record = namedtuple('record', 'filename, day, time')
        filelist = [record(mfilter.match(f).group(0),
                           mfilter.match(f).group('day'),
                           mfilter.match(f).group('time')) for f in fileList if mfilter.match(f)]
        filelist.sort(key=attrgetter('day', 'time'), reverse=True)
        filename = filelist[0].filename
        #print(filename)
        with open(os.path.join(settings.storeHome, filename), 'rb') as f:
            return pickle.load(f)


class EnablersAnalyser(Analyser):
    def __init__(self, reporter):
        super().__init__(reporter)
        self.enablers_sprint_status_graph_data = reporter.enablers_sprint_status_graph_data
        self.enablers_errors_graph_data = reporter.enablers_errors_graph_data
        self.enablers = reporter.enablers

    def save(self):
        timestamp = datetime.now().strftime("%Y%m%d-%H%M")
        filename = 'FIWARE.backlog.enablersAnalyser.' + timestamp + '.pkl'
        longFilename = os.path.join(settings.storeHome, filename)
        #print('W: {0}'.format(longFilename))
        with open(longFilename, 'wb') as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)

    def clean(self):
        fileList = os.listdir(settings.storeHome)
        mfilter = re.compile(r'\bFIWARE[.]backlog[.]enablersAnalyser[.](?P<day>\d{8})[-](?P<time>\d{4})[.]pkl\b')
        record = namedtuple('record', 'filename, day, time')
        filelist = [record(mfilter.match(f).group(0),
                           mfilter.match(f).group('day'),
                           mfilter.match(f).group('time')) for f in fileList if mfilter.match(f)]
        super().cleanList(filelist)

    @classmethod
    def fromFile(cls):
        fileList = os.listdir(settings.storeHome)
        mfilter = re.compile(r'\bFIWARE[.]backlog[.]enablersAnalyser[.](?P<day>\d{8})[-](?P<time>\d{4})[.]pkl\b')
        record = namedtuple('record', 'filename, day, time')
        filelist = [record(mfilter.match(f).group(0),
                           mfilter.match(f).group('day'),
                           mfilter.match(f).group('time')) for f in fileList if mfilter.match(f)]
        filelist.sort(key=attrgetter('day', 'time'), reverse=True)
        filename = filelist[0].filename
        #print(filename)
        #
        with open(os.path.join(settings.storeHome, filename), 'rb') as f:
            return pickle.load(f)

if __name__ == "__main__":
    pass
