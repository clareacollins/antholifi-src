import re

from scraper import format

# Various
def sortingTitle(obj):
    if obj.title.lower()[:2] == 'a ':
        sorting_title = obj.title[2:]
    elif obj.title.lower()[:3] == 'an ':
        sorting_title = obj.title[3:]
    elif obj.title.lower()[:4] == 'the ':
        sorting_title = obj.title[4:]
    else:
        sorting_title = obj.title
    obj.sorting_title = re.sub('\(|\)|\.|,|\?|-|\/|\!|’', '', sorting_title)
    obj.sorting_title = re.sub("'", '', obj.sorting_title)
    return obj

def pickRating(obj):
# Choose Series Rating
    if len(obj.rating) == 1:
        obj.rating = obj.rating[0]
    else:
        if 'NR' in obj.rating:
            obj.rating = 'NR'
        elif 'E' in obj.rating:
            obj.rating = 'E'
        elif 'M' in obj.rating:
            obj.rating = 'M'
        elif 'T' in obj.rating:
            obj.rating = 'T'
    return obj

def fixWarning(obj):
    if obj.warning == []:
        obj.warning = ''
    else:
        temp_warning = []
        for w in obj.warning:
            if w != '':
                temp_warning.append(w)
        obj.warning = ', '.join(temp_warning)
    return obj

def objPrint(obj):
    # Printers
    print(obj.title)
    print(', '.join(obj.author))
    print(obj.words)
    print(obj.chapters)
    print(obj.status)
    print(obj.summary)
    print(obj.series)
    print(obj.rating)
    print(obj.warning)
    print(', '.join(obj.relationship))
    print(', '.join(obj.character))
    print(', '.join(obj.freeform))


def getAbbreviation(text, type):
    rating_Abbr_list = [('Explicit', 'E'), ('Mature', 'M'), ('Teen And Up Audiences', 'T'), ('General Audiences', 'G'), ('Not Rated', 'NR')]
    warning_Abbr_list = [('No Archive Warnings Apply', ''), ('Creator Chose Not To Use Archive Warnings', 'Not Used'), ('Rape/Non-Con', 'Rape'), ('Graphic Depictions Of Violence', 'Violence'), ('Major Character Death', 'MCD'), ('Underage', 'Underage'), ('Choose Not To Use Archive Warnings', 'Not Used')]
    if type == 'rating':
        tuple_list = rating_Abbr_list
    elif type == 'warning':
        tuple_list = warning_Abbr_list
    for tuple in tuple_list:
        if text == tuple[0]:
            return tuple[1]

def grabElement(text, start, end):
    return text.partition(start)[-1].split(end, 1)[0]

def getMatch(html_text, search_text, type=None, default_value=''):
    match = re.search(search_text, html_text)
    if type == 'summary':
        match = re.search(search_text, html_text, re.S)
    if match != None:
        if type == 'list':
            return re.findall(search_text, html_text)
        return match.group('CAP')
    return default_value
    
def getElementMatch(extTag, html_text, search_text, type, default_value, closingTag='</dd>'):
    extText = grabElement(html_text, extTag, closingTag)
    return getMatch(extText, search_text, type, default_value)

'''Multipurpose Extraction Functions'''
# Get Work or Series Title (Throws Error if No Title Found)
def getTitle(html_text):
    searchText = '<h2 class="(title )?heading">\s*(<[^>]+>\s*)?(?P<CAP>.*)\s*(<[^>]+>\s*)?</h2>'
    title = getMatch(html_text, searchText)
    title = re.sub('&amp;', '&', title)
    if title == '':
        print('Error: No Title Found')
    return title

'''Work Extracts'''
# Get Work Author (Default Value: ['Anonymous'])
def getWorkAuthor(html_text):
    extTag = '<h3 class="byline heading">'
    searchText = '<a rel="author"[^>]+>\s*(?P<CAP>[^<]*?)</a>'
    author = getElementMatch(extTag, html_text, searchText, 'list', ['Anonymous'], '</h3>')
    author = format.tags_list(author)
    return author
# Get Work Summary
def getWorkSummary(html_text):
    summaryText = '<div class="summary module"( role="complementary")?>\s*<h3 class="heading">Summary:</h3>\s*<blockquote class="userstuff">\s*(?P<CAP>.*?)\s*</blockquote>\s*</div>'
    summary = getMatch(html_text, summaryText, 'summary')
    if summary == '':
        notesText = '<div class="notes module"( role="complementary")?>\s*<h3 class="heading">Notes:</h3>\s*(<ul.*?</ul>\s*)?<blockquote class="userstuff">\s*(?P<CAP>.*?)\s*</blockquote>\s*(<p class="jump">|</div>)'
        summary = getMatch(html_text, notesText, 'summary')
    summary = format.text(summary)
    summary = re.sub('�', '...', summary)
    return summary
# Get Work Rating
def getWorkRating(html_text):
    searchText = '<dd class="rating tags">\s*<ul class="commas">\s*<[^>]+><a class="tag"[^>]+>(?P<CAP>.*)</a></li>'
    rating = getMatch(html_text, searchText, None, 'Not Rated')
    rating = getAbbreviation(rating, 'rating')
    return rating
# Get Work Warning Tags
def getWorkWarning(html_text):
    searchText = '<a class="tag"[^>]+>(?P<CAP>.*?)\s*</a>'
    extTag = '<dd class="warning tags">'
    warning = getElementMatch(extTag, html_text, searchText, 'list', [])
    warning = format.tags_list(warning)
# Abbreviate Warnings
    warning_list = []
    for w in warning:
        w = getAbbreviation(w, 'warning')
        if w != '' and w not in warning_list:
            warning_list.append(w)
# Handle No Warnings
    if warning_list == []:
        warning = ''
    else:
        warning = ', '.join(warning_list)
    return warning
# Get Work Tags
def getWorkTags(html_text, type):
    extTag = '<dd class="' + type + ' tags">'
    searchText = '<l[^>]+><a class="tag"[^>]+>(?P<CAP>[^<]*?)\s*</a>'
    tags = getElementMatch(extTag, html_text, searchText, 'list', [])
    tags = format.tags_list(tags, type)
    return tags
# Get Work Series Tuple
def getWorkSeries(html_text):
    extTag = '<dd class="series">'
    searchText = '<span class="position">Part (?P<SERIESNUM>\d\d?) of <a href[^>]*?>(?P<WORKSERIES>[^<]*?)</a>'
    series = getElementMatch(extTag, html_text, searchText, 'list', [])
    series = format.tuples(series)
    return series
# Get Work Status
def getWorkStatus(html_text):
    if '<dt class="status">Completed:</dt>' in html_text or '<dd class="chapters">1/1</dd>' in html_text:
        status = 'Completed'
    else:
        status = re.search('<dt class="status">Updated:</dt><dd class="status">(?P<UPDATE>[^<]+)</dd>', html_text).group('UPDATE')
    return status    

'''Series Extracts'''
def getSeriesAuthor(html_text):
    searchText = '<a rel="author"[^>]+>\s*(?P<CAP>[^<]*?)</a>'
    author = getMatch(html_text, searchText, 'list', ['Anonymous'])
    author = format.tags_list(author)
    return list(set(author))
# Get Series Summary
def getSeriesSummary(html_text):
    summaryText = '<dt>Description:</dt>\s*<dd><blockquote class="userstuff">(?P<CAP>.*?)</blockquote></dd>'
    summary = getMatch(html_text, summaryText, 'summary')
    summary = format.text(summary)
    summary = re.sub('�', '...', summary)
    return summary
# Get Series Status
def getSeriesStatus(html_text):
    if re.search('<dt>Complete:</dt>\s*<dd>Yes</dd>', html_text):
        status = 'Completed'
    else:
        status = re.search('<dt>Series Updated:</dt>\s*<dd>(?P<UPDATE>[^<]+)</dd>', html_text).group('UPDATE')
    return status

# Get Entry Number
def getEntryNum(entry_text, title):
    searchText = 'Part <strong>(?P<NUM>[^<]+)</strong> of <a[^>]+>(?P<SERI>[^<]+)</a>'
# Get Series Tuple for Entry
    entry_tuple = re.findall(searchText, entry_text)
    entry_num = 0
    for tuple in entry_tuple:
        if title == re.sub('&amp;', '&', tuple[1]):
            entry_num = tuple[0]
    return str(entry_num)

def getEntrySummary(entry_text):
    searchText = '<h6 class="landmark heading">Summary</h6>\s*<blockquote class="userstuff summary">\s*(?P<CAP>.*?)\s*</blockquote>'
    summary = getMatch(entry_text, searchText, 'summary', '')
    summary = format.text(summary)
    summary = re.sub('\n', ' ', summary)
    summary = re.sub('�', '...', summary)
    return summary

def getEntryChapters(entry_text):
    searchTect = '<dd class="chapters">(<a href=[^>]*?>)?(?P<CAP>[^<]+(</a>)?[^<]+)</dd>'
    entry_chap = getMatch(entry_text, searchTect)
    entry_chap = re.sub('<[^>]*?>', '', entry_chap)
    return entry_chap

def getEntryRating(entry_text):
    searchText = '<span class="rating[^>]*?><span class="text">(?P<CAP>[^<]+)</span>'
    rating = getMatch(entry_text, searchText, None, 'Not Rated')
    rating = getAbbreviation(rating, 'rating')
    return rating

def getEntryWarning(entry_text, obj):
    extTags = ['<li class="warnings">', "<li class='warnings'>"]
    for extTag in extTags:
        if extTag in entry_text:
            searchText = extTag + '<strong><a class[^>]*?>(?P<CAP>[^<]*?)</a>'
            entry_warning = re.findall(searchText, entry_text)
            entry_warning = format.tags_list(entry_warning)
            for warning in entry_warning:
                warning = getAbbreviation(warning, 'warning')
                if warning not in obj.warning:
                    obj.warning.append(warning)

def getEntryTags(entry_text, type, obj):
    extTags = ['<li class="' + type + 's">', "<li class='" + type + "s'>"]
    for extTag in extTags:
        if extTag in entry_text:
            searchText = extTag + "<a class[^>]*?>(?P<CAP>[^<]*?)</a>"
            entry_tags = re.findall(searchText, entry_text)
            entry_tags = format.tags_list(entry_tags, type)
            for tag in entry_tags:
                if tag not in getattr(obj, type):
                    getattr(obj, type).append(tag)