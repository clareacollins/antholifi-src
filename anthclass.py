import utils, active

import itertools
import re

# File Class and Derivatives
class File(object):
    '''
    The File Class is the Base Class for all file objects.
    It has only two attributes: Name and Text.
    Its behaviors are Getters, Setters, and Printing.
    '''
    def __init__(self, file_name, file_contents):
        self.name = file_name
        self.text = file_contents
        # Means all derivative classes call their own getStats(self)
        self.getStats()
# This empty getStats() is a placeholder for other classes' getStats()
    def getStats(self):
        return
# Getters
    def getName(self):
        return self.name
    def getText(self):
        return self.text
# Setters
    def setName(self, new_name):
        self.name = new_name
    def setText(self, new_text):
        self.text = new_text
# Utilities
    def makeChapter(self, chapter_name, chapter_text):
        return Chapter(chapter_name, chapter_text)
# Printing
    def __str__(self):
        return utils.string.fix(self.name + " File")
    def getType(self):
        return "File"
    
class Preface(File):
    '''
    The Preface Class is a derivative of the File Class.
    Attributes are Title, Author, Fandom, Wordcount, Summary, GuideSummary, Series, Number, 
    UPDATE, LINK, and SPEC.
        UPDATE is a bool that decides whether Get_Updates checks the work.
        LINK is the url where the story can be found, or 'none' if the story isn't online anymore
        SPEC values include:
                        LJ (the work is taken from livejournal, dreamwidth, or tumblr)
                        CHAP (the work is a chapter taken from a longer work)
                        ART (The series is compiled artificially)
                        LOST (The work can no longer be found online)
        Specific to the 'FFF' format are the attributes Series and Number.
    Behaviors are the full range of Getters, a Format Setter, and Printing.
    '''
    def getStats(self):
        # Basic Story Stats are stored in preface title tags
        title_tag_stats = []
        for tag in self.text.partition('<title>')[2].partition('</title>')[0].split('\n')[:-1]:
            title_tag_stats.append(tag.strip())
        # Assign update stats if there
        update_stats_boolean = False
        if '<!--UPDATE: ' in self.text:
            update_stats_boolean = True
            self.UPDATE = self.text.partition("<!--UPDATE: '")[2].partition("'")[0].strip()
            self.LINK = self.text.partition("LINK: '")[2].partition("'")[0].strip()
            self.SPEC = self.text.partition("SPECIAL: '")[2].partition("'")[0].strip()
        # If everything was there
        if len(title_tag_stats) == 3 or len(title_tag_stats) == 5:
            self.title = title_tag_stats[0]
            self.author = title_tag_stats[1]
            self.fandom = title_tag_stats[2]
            self.series = ''
            self.number = ''
            # Ao3 (and DIY) (Works from Archive of our Own or works created by this program)
            if 'preface' in self.name:
                # Assign other attributes
                self.wordcount = int(re.sub(',', '', self.text.partition('Words: ')[2].partition('\n')[0].strip()))
                self.summary = re.sub('</p>\s*<p>', '\n', self.text.partition('<blockquote class="userstuff">\n\t<p>')[2].partition('</p></blockquote>')[0].strip())
                if len(title_tag_stats) == 5:
                    self.series = title_tag_stats[3]
                    self.number = int(title_tag_stats[4])
            # FFN (Works from Fanfic.net)
            elif 'Cover' in self.name:
                # Assign other attributes
                self.wordcount = int(self.text.partition('Words: ')[2].partition('Reviews: ')[0][:-3].strip().replace(',', ''))
                self.summary = re.sub('</p>\s*<p>', '\n', self.text.partition('</div>\n\t<p>')[2].partition('</p>\n\t<p>Rated:')[0].strip())
            # FFF (This is for files from the calibre app 'FanFicFare')
            elif 'title_page' in self.name:
                # Deal with fandoms
                if ',' in self.fandom:
                    self.fandom = self.fandom.partition(',')[0].strip()
                if ' - ' in self.fandom:
                    self.fandom = self.fandom.partition(' - ')[0].strip()
                # Get Wordcount and Summary
                self.wordcount = int(self.text.partition('<b>Words:</b>')[2].partition('<br')[0].strip().replace(',',''))
                self.summary = re.sub('</p>\s*<p>', '\n', self.text.partition('<p>')[2].partition('</p></blockquote>')[0].strip())
                if len(title_tag_stats) == 5:
                    self.series = title_tag_stats[3]
                    self.number = int(title_tag_stats[4])
            # DIY
            elif 'index_split_' in self.name:
                # Assign other attributes
                self.wordcount = int(self.text.partition('<b>Words:</b> ')[2].partition('<br/>')[0].strip().replace(',', ''))
                self.summary = re.sub('</p>\s*<p>', '\n', self.text.partition('<blockquote class="userstuff">\n\t<p>')[2].partition('</p></blockquote>')[0].strip())

            self.guide_summary = self.summary

# Getters
    def getTitle(self):
        return self.title
    def getAuthor(self):
        return self.author
    def getFandom(self):
        return self.fandom
    def getSeries(self):
        return self.series
    def getNumber(self):
        return self.number
    def getWordcount(self):
        return int(self.wordcount)
    def getSummary(self):
        return re.sub('<[^>]*>', '', self.summary)
    def getGuideSummary(self):
        return re.sub('<[^>]*>', '', self.guide_summary)
    def getUPDATE(self):
        return self.UPDATE
    def getLINK(self):
        return self.LINK
    def getSPEC(self):
        return self.SPEC
# Printable Object
    def __str__(self):
        return utils.string.fix(self.title + " Preface by " + self.author)
    def getType(self):
        return "Preface"

class TOC(File):
    '''
    The TOC Class is a derivative of the File Class.
    It has only two attributes: Name and Text.
    Its only behavior is Printing.
    '''
# Printable Object
    def __str__(self):
        return "TOC file"
    def getType(self):
        return "TOC"

class Chapter(File):
    '''
    The Chapter Class is a derivative of the File Class.
    It has four Attributes: Name, Header, Text, and Number.
        Number is derived from Name.
    Its behaviors are Getters, Setters, and Printing.
    '''
    def getStats(self):
    # Get Number based on Name
        if '_split_' in self.name and 'index_split_' not in self.name:
            self.number = int(self.name[-9:-6]) - 1
        elif 'chap_ffn_' in self.name:
            self.number = int(self.name[9:self.name[9:].find('_')+9])
        elif 'file' in self.name:
            self.number = int(self.name[4:-6])
        elif 'chapter' in self.name:
            if "OEBPS" in self.name:
                self.number = int(self.name[13:self.name.find('_')])
            else:
                self.number = int(self.name[7:self.name.find('_')])
        elif 'index' in self.name:
            self.number = int(self.name[12:self.name.find('.')])
    # get header based on text
        if '</h2>' in self.text:
            if '<h2>' in self.text:
                self.header = self.text.partition('</h2>')[0].partition('<h2>')[2].strip()
            else:
                self.header = self.text.partition('</h2>')[0].split('">')[-1].strip()
            # Remove Numbers from the beggining of headers
            if str(self.number) + '. ' in self.header:
                self.header = re.sub(str(self.number) + '. ', '', self.header)
            if 'Chapter ' + str(self.number) in self.header:
                if 'Chapter ' + str(self.number) == self.header:
                    self.header = 'Chapter ' + str(self.number)
                else:
                    self.header = re.sub('Chapter [\d]+[:]*', '', self.header)
        else:
            self.header = 'Chapter ' + str(self.number)
# Getters & Setters
    def getHeader(self):
        return self.header
    def getNumber(self):
        return self.number
    def setHeader(self, new_header):
        self.header = new_header
    def setNumber(self, new_number):
        self.number = new_number
# Printable Object
    def __str__(self):
        return utils.string.fix(self.name + ", Chapter " + str(self.number))
    def getType(self):
        return "Chapter"

# Story Classes
class Singleton(object):
    '''
    A Singleton object represents a work which may or may not be in a series.
    Attributes:
        Preface, TOC (TOC object or 0), Body (list of Chapter objects), Contents (Preface, TOC and Chapter objects),
        Images, Image Bool
        Title, Author, Fandom, Series, Number
        Wordcount, Summary, Guide Summary, Sort
        UPDATE, LINK, and SPEC
    '''
    def __init__(self, contents_list):
    # Get data from all the files in contents_list
        for file in contents_list:
            # Assign Preface attribute
            if isinstance(file, Preface):
                # Assign Singleton attributes from the preface object
                self.preface = file
                # Story stats
                self.title = self.preface.getTitle()
                self.author = self.preface.getAuthor()
                self.fandom = self.preface.getFandom()
                self.series = self.preface.getSeries()
                self.number = self.preface.getNumber()
                self.wordcount = self.preface.getWordcount()
                self.summary = self.preface.getSummary()
                self.guide_summary = self.preface.getGuideSummary()
                self.sort = utils.string.getSortString(self.title, self.author)
                # Updating stats
                self.UPDATE = self.preface.getUPDATE()
                self.LINK = self.preface.getLINK()
                self.SPEC = self.preface.getSPEC()
            # Assign TOC (if there's one present)
            elif isinstance(file, TOC):
                self.TOC = file
    # Order Body and Contents
        self.body = sorted([file for file in contents_list if isinstance(file, Chapter)], key = lambda x:x.getNumber())
        # Keep Appropriate TOC files
        self.TOC = 0
        if len(self.body) > 3:
            # Make TOC
            self.TOC = TOC('TOC.xhtml', utils.string.makeTOCText(self.title, self.body))
        self.contents = utils.obj.orderContents(self.preface, self.TOC, self.body)
    # Go through the body text looking for Image links
        self.image_bool = False
        self.images = []
        for chapter in self.body:
            # Does not catch pics in the author's note
            for match in re.findall('src="([^"]+)"', chapter.getText()):
                if not match.startswith('http'):
                    image_name = str(match).split('/')[-1]
                    # Determine if the link is valid
                    if image_name.endswith('.jpg') or image_name.endswith('.png') or image_name.endswith('.gif') or image_name.endswith('.jpeg'):
                        self.image_bool = True
                        chapter.setText(re.sub(match,'Images/' + image_name, chapter.getText()))
                        self.images.append(image_name)
                    else:
                        print('Invalid Image Link: ' + match)
        self.fixLinks()
# Getters
    # Get lists of the files
    def getPreface(self):
        return self.preface
    def getTOC(self):
        return self.TOC
    def getBody(self):
        return self.body
    def getContents(self):
        return self.contents
    def getImages(self):
        return self.images
    def getImageBool(self):
        return self.image_bool
    # Get story stats
    def getTitle(self):
        return re.sub("&amp;", "&", self.title)
    def getAuthor(self):
        return self.author
    def getFandom(self):
        return self.fandom
    def getSeries(self):
        return self.series
    def getNumber(self):
        return self.number
    def getWordcount(self):
        return int(self.wordcount)
    def getSummary(self):
        return re.sub('<[^>]*>', '', self.summary)
    def getGuideSummary(self):
        return re.sub('<[^>]*>', '', self.guide_summary)
    def getSort(self):
        return self.sort
    # Get Update Stats
    def getUPDATE(self):
        return self.UPDATE
    def getLINK(self):
        return self.LINK
    def getSPEC(self):
        return self.SPEC
# Setters
    # Automatically Updates Contents
    def updatePreface(self, 
                      newUPDATE=None, newLINK=None, 
                      newTitle=None, newAuthor=None, newFandom=None, 
                      newSeries=None, newNumber=None, newSummary=None):
        if not (newSeries == None and newNumber == None):
            oldSeries = self.series
            oldNumber = self.number
        tuples = [(newUPDATE, 'UPDATE'),
                  (newLINK, 'LINK'),
                  (newTitle, 'title'),
                  (newAuthor, 'author'),
                  (newFandom, 'fandom'),
                  (newSeries, 'series'),
                  (newNumber, 'number'),
                  (newSummary, 'summary')]
        for tuple in tuples:
            if tuple[0] != None:
                setattr(self, tuple[1], tuple[0])
        tags_text = self.preface.text.partition('<dl class="tags">\n\t')[2].partition('</dd>\n\t</dl>\n\t')[0]
        # Change Series Values in tags
        if not (newSeries == None and newNumber == None):
            tags_text = re.sub(f'Part {oldNumber} of\s*{oldSeries}', f'Part {self.number} of\n{self.series}', tags_text)
        # Update the Preface File
        new_preface_text = utils.classobj.Preface.assemble(self.UPDATE, self.LINK, self.title, self.author, self.fandom, self.series, self.number, tags_text, self.summary)
        self.preface = Preface(self.preface.getName(), new_preface_text)
        series_page = 0
        for file in self.contents:
            if file.getName() == 'series_page.xhtml':
                series_page = file
        self.contents = utils.obj.orderContents(self.preface, self.TOC, self.body, series_page)

    def setPreface(self, new_preface_text):
        self.preface = Preface(self.preface.getName(), new_preface_text)
        series_page = 0
        for file in self.contents:
            if file.getName() == 'series_page.xhtml':
                series_page = file
        self.contents = utils.obj.orderContents(self.preface, self.TOC, self.body, series_page)
    def setFandom(self, new_fandom):
        self.fandom = new_fandom
        if self.fandom != "Other":
            self.setPreface(re.sub('<title>(?P<TITLE>[^\n]+)\n\t\t(?P<AUTHOR>[^\n]+)\n\t\t(?P<FANDOM>[^\n]+)\n\t</title>', '<title>\g<TITLE>\n\t\t\g<AUTHOR>\n\t\t' + self.fandom + '\n\t</title>', self.preface.getText()))
    def setNumber(self, new_number):
        self.number = new_number
        self.setPreface(re.sub('<title>(?P<TITLE>[^\n]+)\n\t\t(?P<AUTHOR>[^\n]+)\n\t\t(?P<FANDOM>[^\n]+)\n\t\t(?P<SERI>[^\n]+)\n\t\t(?P<NUM>[^\n]+)\n\t</title>', '<title>\g<TITLE>\n\t\t\g<AUTHOR>\n\t\t\g<FANDOM>\n\t\t\g<SERI>\n\t\t' + str(new_number) + '\n\t</title>', self.preface.getText()))
    def setSeries(self, new_series):
        self.series = new_series
        self.setPreface(re.sub('<title>(?P<TITLE>[^\n]+)\n\t\t(?P<AUTHOR>[^\n]+)\n\t\t(?P<FANDOM>[^\n]+)\n\t\t(?P<SERI>[^\n]+)\n\t\t(?P<NUM>[^\n]+)\n\t</title>', '<title>\g<TITLE>\n\t\t\g<AUTHOR>\n\t\t\g<FANDOM>\n\t\t' + new_series + '\n\t\t\g<NUM>\n\t</title>', self.preface.getText()))


    def setImages(self, name_tuples):
        new_images = []
        for name_tuple in name_tuples:
            old_name, new_name = name_tuple[0], name_tuple[1]
            for i in self.contents:
                i.setText(re.sub('Images/[^>]*?' + old_name + '"', 'Images/' + new_name + '"', i.getText()))
            for image in self.images:
                if image == old_name:
                    self.images.remove(image)
                    new_images.append(new_name)
        self.images.extend(new_images)
    def getWordsString(self):
        return "Words: " + utils.string.formatNum(self.getWordcount(), 'Word')
    def getWorksString(self):
        return ""
    def getFandomString(self):
        return "Fandom: " + utils.string.fix(self.getFandom())
# Printing
    def __str__(self):
        return utils.string.fix(self.title + " by " + self.author)
    def getType(self):
        return "Singleton"
    def updateSort(self):
        self.sort = utils.string.getSortString(self.title, self.author)
    def fixLinks(self):
        for file in self.contents:
            file.setText(re.sub('<link href="[/|\.]*?stylesheet_Gen.css"[^>]*>','<link href="stylesheet_Gen.css" type="text/css" charset="UTF-8" rel="stylesheet"/>', file.getText()))
            file.setText(re.sub('src="[/|\.]*?Images/','src="Images/', file.getText()))
        # Fix the Preface Guide Link
        for file in self.contents:
            if file.getType() == 'Preface':
                file.setText(re.sub('<a href="[/|\.]*?guide.html#[^"]+">Back to Guide\n\t</a>','<a>\n\t</a>', file.getText()))

class Series(object):
    '''
    A Series object represents multiple Entry objects. (Series metadata?)
    Attributes:
        Contents (ordered list of Entries), TOC Guide, Images
        Title, Author, Fandom, Wordcount, Summary, Sort, UPDATE, LINK, SPEC,
    '''
    def __init__(self, contents_list, series_title, series_link="None", series_summary='', detectOrder=True):
    # Assign Contents to contents_list sorted by entry number
        eint = 1
        for entry in contents_list:
            if detectOrder:
                entry.updatePreface(newSeries=series_title, newNumber=utils.string.grabSeriesNumber(entry.preface.text, series_title))
            else:
                entry.updatePreface(newSeries=series_title, newNumber=eint)
                eint += 1
        for entry in sorted(contents_list, key = lambda x:int(x.getNumber())):
            entNum = entry.getNumber()
            if entNum in [ent.getNumber() for ent in contents_list if ent != entry]:
                entry.updatePreface(newSeries=series_title, newNumber=str(int(entNum)+1))
        self.contents = sorted(contents_list, key = lambda x:int(x.getNumber()))

    # Assign stats based on the first entry
        self.title = self.contents[0].getSeries()
        if series_title != None:
            self.title = series_title
            self.setSeries(series_title)
        # Author listed is the main (most common) author of the series. Can be multiple if there's a tie.
        self.author = utils.other.detectAuthor([i.getAuthor() for i in self.contents])
        self.fandom = self.contents[0].getFandom()
        self.wordcount = sum([i.getWordcount() for i in self.contents])
        self.summary = series_summary
        self.guide_summary = series_summary
        self.sort = utils.string.getSortString(self.title, self.author)
        self.UPDATE = self.contents[0].getUPDATE() # Doesn't show UPDATE status for series itself
        self.LINK = series_link
        self.SPEC = self.contents[0].getSPEC()
    # Make Series Page
        self.TOC = TOC('series_page.xhtml', utils.string.makeSeriesPageText(self))
        self.contents[0].contents.insert(0, self.TOC)
    # Go through the body text looking for Image links
        self.image_bool = False
        self.images = []
        for entry in self.contents:
            if entry.image_bool:
                self.image_bool = True
                for image in entry.images:
                    self.images.append(image)
        self.fixLinks()
# Getters
    def getContents(self):
        return self.contents
    def getImages(self):
        return self.images
    def getImageBool(self):
        return self.image_bool
    # Story Stats
    def getTitle(self):
        return self.title
    def getAuthor(self):
        return self.author
    def getFandom(self):
        return self.fandom
    def getWordcount(self):
        return self.wordcount
    def getSort(self):
        return self.sort
# Currently Empty
    def getSummary(self):
        return self.summary
    def getGuideSummary(self):
        return self.guide_summary
    # Update Stats
    def getUPDATE(self):
        return self.UPDATE
    def getLINK(self):
        return self.LINK
    def getSPEC(self):
        return self.SPEC
# Setters
    # Automatically Updates Contents
    def setFandom(self, new_fandom):
        self.fandom = new_fandom
        if self.fandom != "Other":
            for entry in self.contents:
                entry.setFandom(new_fandom)
    def setSeries(self, new_series):
        self.title = new_series
        for entry in self.contents:
            entry.setSeries(new_series)
    def setImages(self, name_tuples):
        new_images = []
        for name_tuple in name_tuples:
            old_name, new_name = name_tuple[0], name_tuple[1]
            for entry in self.contents:
                entry.setImages(name_tuples)
            for image in self.images:
                if image == old_name:
                    self.images.remove(image)
                    new_images.append(new_name)
        self.images.extend(new_images) 
    def getWordsString(self):
        if active.index.entry.int == 0:
            return "Words: " + utils.string.formatNum(self.getWordcount(), 'Word')
        else:
            return "Words: " + utils.string.formatNum(self.contents[active.index.entry.int-1].getWordcount(), 'Word')
    def getFandomString(self):
        return "Fandom: " + utils.string.fix(self.getFandom())
# Utilities
    def sortSeries(self):
        self.contents = sorted(self.contents, key = lambda x:int(x.getNumber()))
    def __str__(self):
        return utils.string.fix(self.title + " series by " + self.author)
    def getType(self):
        return "Series"
    def updateSort(self):
        self.sort = utils.string.getSortString(self.title, self.author)
    def fixLinks(self):
        for entry in self.contents:
            for file in entry.contents:
                file.setText(re.sub('<link href="[/|\.]*?stylesheet_Gen.css"[^>]*?>','<link href="../stylesheet_Gen.css" type="text/css" charset="UTF-8" rel="stylesheet"/>', file.getText()))
                file.setText(re.sub('src="[/|\.]*?Images/','src="../Images/', file.getText()))
        # Fix the Series Page Guide Link
                if file.getName() == 'series_page.xhtml':
                    file.setText(re.sub('<a id="(?P<ID>[^"]+)" href="[/|\.]*guide.html#[^"]+">','<a id="\g<ID>" href="../1/series_page.xhtml#\g<ID>">', file.getText()))

# Anth Class
class Anthology(object):
    '''
    An Anthology object contains multiple Series and/or Singleton objects.
    Grouped by fandom, most to least works, then alphabetically.
    Attributes are Name, Contents (a flat list of all works), Anth (list of groups), and Images.
    Derived Attributes are Abbr (Abbreviation), Total Wordcount, Works Number, Fandom Count, Fandom List, Fandom Group Pages
    Behaviors are basic Getters, derived Getters, setFandom, setImage, Printer,
    sortContents, removeWorks, and addWorks.
    '''
    def __init__(self, contents_list, name):
        self.name = name.partition(" Anthology")[0]
        # Assign attributes to default values
        self.images = [self.getAbbr() + '_AAA_Cover.png']
        # Assign contents (should be a flat list)
        self.contents = []
        for work in contents_list:
            self.contents.append(work)
            for image in work.getImages():
                self.images.append(image)
        self.anth = self.sortContents()
        self.fixLinks()

# Getters
    def getName(self):
        return self.name
    def getContents(self):
        return self.contents
    def getAnth(self):
        return self.anth
    def getImages(self):
        return self.images
    # Derived Attributes
    def getAbbr(self):
        return utils.string.abbreviation(self.name)
    def getWordsString(self):
        if active.index.page.int == 0:
            wordcount = sum([work.getWordcount() for work in self.contents])
        else:
            wordcount = sum([work.getWordcount() for work in self.anth[active.index.page.int-1]])
        return "Words: " +  utils.string.formatNum(wordcount, 'Word')
    def getWorksString(self):
        if active.index.page.int == 0:
            worksnum = len(self.contents)
        else:
            worksnum = len(self.anth[active.index.page.int-1])
        return "Works: " + str(worksnum)
    def getFandomString(self):
        if len(self.anth) == 1:
            return "Fandom: " + utils.string.fix(self.contents[0].getFandom())
        elif active.index.page.int == 0:
            return "Fandoms: " + utils.string.fix(', '.join([group[0].getFandom() for group in self.anth]))
        else:
            return "Fandom: " + utils.string.fix(self.anth[active.index.page.int-1][0].getFandom())
# Setters
    def setFandom(self, old_fandom, new_fandom):
        if old_fandom != new_fandom:
            for group in self.anth:
                for work in group:
                    if work.getFandom() == old_fandom:
                        work.setFandom(new_fandom)
    def setImages(self, name_tuples):
        new_images = []
        for name_tuple in name_tuples:
            old_name, new_name = name_tuple[0], name_tuple[1]
            for work in self.contents:
                work.setImages(name_tuples)
            for image in self.images:
                if image == old_name:
                    self.images.remove(image)
                    new_images.append(new_name)
        self.images.extend(new_images)
        self.images = sorted(self.images)
# Utilities
    def fixLinks(self):
        # For every group in anthology
        for group in self.anth:
            group_index = self.anth.index(group) + 1
            # For every work in the group
            for work in group:
                work_index = group.index(work) + 1
                if work.getType() == 'Singleton':
                    for file in work.contents:
                        file.setText(re.sub('<link href="[/|\.]*stylesheet_Gen.css"[^>]*>','<link href="../../stylesheet_Gen.css" type="text/css" charset="UTF-8" rel="stylesheet"/>', file.getText()))
                        file.setText(re.sub('src="[/|\.]*Images/','src="../../Images/', file.getText()))
                elif work.getType() == 'Series':
                    # Fix series page Link
                    id = utils.string.getID(work.title, work.author) + '00'
                    storyID = self.getAbbr() + utils.string.formatNum(group_index, 'Group') + utils.string.formatNum(work_index, 'GuideID')
                    work.contents[0].contents[0].setText(re.sub(f'<a id="{id}" href="[^"]+">', f'<a id="{id}" href="../../../guide.html#{storyID}">', work.contents[0].contents[0].getText()))
                    for entry in work.contents:
                        for file in entry.contents:
                            file.setText(re.sub('<link href="[/|\.]*stylesheet_Gen.css"[^>]*>','<link href="../../../stylesheet_Gen.css" type="text/css" charset="UTF-8" rel="stylesheet"/>', file.getText()))
                            file.setText(re.sub('src="[/|\.]*Images/','src="../../../Images/', file.getText()))
    def sortContents(self):
        # Sort the (flat) contents by fandom. Needed because of how groupby works
        fandom_sort_list = sorted(self.contents, key = lambda x: x.getFandom())
        # Group by Fandoms
        grouped_by_fandom_list = []
        for key, group in itertools.groupby(fandom_sort_list, key = lambda x: x.getFandom()):
            grouped_by_fandom_list.append(list(group))
        # If there's only one fandom
        if len(grouped_by_fandom_list) == 1:
            # Return the list with only one fandom group in it (a singlefandom anthology)
            return [sorted(grouped_by_fandom_list[0], key = lambda x:x.getSort())]
        else:
            # Separate the groups from the misc/assorted works
            fandom_group_list = []
            misc_fandoms_list = []
            for group in grouped_by_fandom_list:
                if len(group) > 2 and group[0].getFandom() != 'Other':
                    fandom_group_list.append(sorted(group, key = lambda x:x.getSort()))
                else:
                    misc_fandoms_list.append(group)
            # Put misc works into one group
            misc_group = []
            for fandom in misc_fandoms_list:
                for work in fandom:
                    work.setFandom('Other')
                    misc_group.append(work)
            # Sort the lists
            # sort misc alphabetically
            misc_group = sorted(misc_group, key = lambda x:x.getSort())
            # sort fandoms by most works
            fandom_group_list = sorted(fandom_group_list, reverse=True, key = lambda x:len(x))
            # combine the lists
            if misc_group != []:
                fandom_group_list.append(misc_group)
            return fandom_group_list
    def removeWorks(self, work_list):
        group_contents = []
        # for every group in the anthology
        for group in self.anth:
            for work in group:
                matchBool = False
                for work_obj in work_list:
                    if str(work) == str(work_obj):
                        matchBool = True
                if matchBool == False:
                    group_contents.append(work)
        self.contents = group_contents
        self.anth = self.sortContents()
    def addWorks(self, work_list):
        for work in work_list:
            self.contents.append(work)
        self.anth = self.sortContents()
        self.fixLinks()
    # Printing
    def __str__(self):
        return utils.string.fix(self.name + " Anthology")
    def getType(self):
        return "Anthology"
    def printLinks(self):
        for group in self.anth:
            for work in group:
                print(work.LINK)
