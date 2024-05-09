import re

from scraper import format, storyobj, utils

def links(html_text):
    # rfind the entry links from the html text
    list = []
    for match in re.findall('<a href="/works/(?P<CAP>\d+)">', html_text):
        list.append('https://archiveofourown.org/works/' + match)
    return list

def csvextract(html_text, link):
    object = storyobj.Story(link)
    if '/works/' in link:
        object = work(object, html_text)
    elif '/series/' in link:
        object = series(object, html_text)
    object.makeStr()
    return object.string

def work(obj, html_text):
# Basics
    obj.title = utils.getTitle(html_text)
    obj.author = utils.getWorkAuthor(html_text)
    obj.summary = utils.getWorkSummary(html_text)
# Stats
    obj.words = format.words(re.search('<dd class="words">\s*(?P<WORDS>[^<]+)</dd>', html_text).group('WORDS'))
    obj.chapters = re.search('<dd class="chapters">\s*(?P<CHAPTERS>[^<]+)</dd>', html_text).group('CHAPTERS')
# Tags
    obj.rating = utils.getWorkRating(html_text)
    obj.warning = utils.getWorkWarning(html_text)
    obj.relationship = utils.getWorkTags(html_text, 'relationship')
    obj.character = utils.getWorkTags(html_text, 'character')
    obj.freeform = utils.getWorkTags(html_text, 'freeform')
# Other
    obj.series = utils.getWorkSeries(html_text)
    obj.status = utils.getWorkStatus(html_text)
    
    obj = utils.sortingTitle(obj)
    # obj = utils.fixWarning(obj)
    obj = utils.pickRating(obj)
    # utils.objPrint(obj)
    return obj

def series(obj, html_text):
# Basics
    obj.title = utils.getTitle(html_text)
    obj.author = utils.getSeriesAuthor(html_text)
    obj.summary =  utils.getSeriesSummary(html_text)
# Words/Chaps
    obj.words = format.words(re.search('<dt>Words:</dt>\s*<dd>(?P<WORDS>[^<]+)</dd>', html_text).group('WORDS'))
    obj.chapters = re.search('<dt>Works:</dt>\s*<dd>(?P<CHAPTERS>[^<]+)</dd>', html_text).group('CHAPTERS')
# Status
    obj.status = utils.getSeriesStatus(html_text)
    # Entries
    obj.warning = []
    obj.rating = []
    obj.relationship = []
    obj.character = []
    obj.freeform = []
    # split the html
    series_text = html_text.split('role="article">')[1:]
    for entry in series_text:
        entry_num = utils.getEntryNum(entry, obj.title)
        # Get Entry Basics
        entry_title = re.search('<h4 class="heading">\s*<a href="/works/(\d)+">(?P<TIT>[^<]+)</a>', entry).group('TIT')
        entry_words = re.search('<dd class="words">(?P<WOR>[^<]+)</dd>', entry).group('WOR')
        # Get Entry Summary
        entry_summary = utils.getEntrySummary(entry)
        entry_chap = utils.getEntryChapters(entry)
        # Grab rating (For series is highest)?
        entry_rating = utils.getEntryRating(entry)
        if entry_rating not in obj.rating:
            obj.rating.append(entry_rating)
        
        obj.series = obj.series + entry_num + ') ' + \
        entry_title + ' [' + entry_words + '; ' + entry_chap + ' ' + entry_rating + '] ' + \
        entry_summary + '\n'
    # Warnings
        utils.getEntryWarning(entry, obj)
    # Tags
        utils.getEntryTags(entry, 'relationship', obj)
        utils.getEntryTags(entry, 'character', obj)
        utils.getEntryTags(entry, 'freeform', obj)

    if obj.series != '':
        obj.series =  format.text(obj.series)
    obj = utils.sortingTitle(obj)
    obj = utils.fixWarning(obj)
    obj = utils.pickRating(obj)
    #objPrint()
    return obj





