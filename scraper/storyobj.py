
class Story(object):
    def __init__(self, link):
        self.title = ''
        self.sorting_title = ''
        self.author = ''
        self.words = ''
        self.chapters = ''
        self.status = ''
        self.summary = ''
        self.series = ''
        self.rating = ''
        self.warning = ''
        self.relationship = ''
        self.character = ''
        self.freeform = ''
        self.link = link
        self.string = ''
    def makeStr(self):
        self.string = self.title + '@' + self.sorting_title + '@' + \
        ', '.join(self.author) + '@' + self.words + '@' + self.chapters + '@@' + \
        self.status + '@"' + self.summary + '"@"' + self.series + '"@' + self.warning + \
        '@' + self.rating + '@' + ', '.join(self.relationship) + '@' + \
        ', '.join(self.character) + '@' + ', '.join(self.freeform) + '@@@@' + self.link
