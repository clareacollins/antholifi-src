import re
from bs4 import BeautifulSoup
from utils import classobj

'''The Utils Package String Module
This module contains functions that deal with strings and text.
'''

### Passed String
### Returns String

## Simple Re Functions
# Fixes '&' Before Displaying Text
def fix(string):
    string = re.sub('&amp;', '&', string)
    return string
# Returns string as valid filename (no forbidden characters)
def filename(string):
    string = re.sub(':|\?|\/|\*', '', string)
    return string
# Returns string with only alphanumeric characters
def alphanumString(raw_string):
    string = ''
    for character in raw_string.lower():
        if character not in '"˜¦…‘.!?,:;@#$%^&*-+=()[]{}<>/\\‘’“”|â€™œã¡':
            if character not in "' ":
                string = string + character
    return string
# Returns string without 'A', 'An', and 'The' at the start
def removeArticles(string):
    if (string[:4].lower() == 'the ') or (string[:3].lower() == 'an ') or (string[:2].lower() == 'a '):
        return string[string.find(' ') + 1:]
    else:
        return string
# Returns Image file name without anthology suffix
def removeSuffix(string):
    if string[0].isupper():
        string = string[string.find('_')+1:]
    return string

## Compound Functions
def getAnthTitle(string):
    fandom = string
    title_suffix = ''
    if '_' in string:
        fandom = string.partition('_')[0]
        title_suffix = ' ' + string.partition('_')[-1]
    return abbreviation(fandom), abbreviation(fandom) + title_suffix

## Compound Functions
# Passed a Fandom name or abbreviation string, returns the other corresponding string
def abbreviation(title):
    fandom_abbr_tuples = REDACTED
    additional_abbr = REDACTED
    fandom_abbreviation = ''
    # Abbreviation to long form
    if len(title) <= 4:
        for i in fandom_abbr_tuples:
            if title == i[1]:
                return i[0]
    # Long form to Abbreviation
    else:
        for i in fandom_abbr_tuples:
            if i[0] in title:
                fandom_abbreviation = i[1]
        # Adds for Anthologies
        for i in additional_abbr:
            if i[0] in title:
                fandom_abbreviation = fandom_abbreviation + i[1]
    # If the fandom isn't in fandom_abbreviations_list
    if fandom_abbreviation == "":
        #print(title + " not in abbreviations list.")
        return "UNK"
    # Return the correct string
    return fandom_abbreviation
# Returns number string that's been formatted based on the passed type
def formatNum(num, type):
# If we're giving all the works their own unique ID codes to reference later
    # GuideID Numbers (000)
    if type == 'GuideID':
        if len(str(num)) == 1:
            return '00' + str(num)
        elif len(str(num)) == 2:
            return '0' + str(num)
        else:
            return str(num)
    # Adds commas to word count (up to 999,999 words)
    elif type == 'Word':
        if int(num) >= 1000:
            return str(num)[:-3] + "," + str(num)[-3:]
        else:
            return str(num)
    # Treats number like a folder path
    elif type == 'Path':
        return str(num) + '/'
    # Entry Number (00)
    elif type == 'Entry':
        if len(str(num)) == 1:
            return '0' + str(num)
        elif len(str(num)) == 2:
            return str(num)
    # Only in Segmented Anthologies, possibly still relevant
    elif type == 'Group':
        if num > 0:
            if len(str(num)) == 1:
                return '0' + str(num)
            elif len(str(num)) == 2:
                return str(num)
        else:
            return '00'
    # Manifest Work ID (w000)
    elif type == 'manifest_work_numbering':
        if len(str(num)) == 1:
            return 'w00' + str(num)
        elif len(str(num)) == 2:
            return 'w0' + str(num)
        else:
            return 'w' + str(num)
    # Manifest Chapter ID (c000)
    elif type == 'manifest_chapter_numbering':
        if len(str(num)) == 1:
            return 'c00' + str(num)
        elif len(str(num)) == 2:
            return 'c0' + str(num)
        else:
            return 'c' + str(num)
    # Manifest Chapter ID (e00)
    elif type == 'manifest_entry_numbering':
        if len(str(num)) == 1:
            return 'e0' + str(num)
        elif len(str(num)) == 2:
            return 'e' + str(num)
    # Manifest Group ID (g00)
    elif type == 'manifest_group_numbering':
        if num > 0:
            if len(str(num)) == 1:
                return 'g0' + str(num)
            elif len(str(num)) == 2:
                return 'g' + str(num)
        else:
            return 'g00'
    # Used to replicate FFF file names (file_00001.xhtml)
    elif type == 'FFF_file_toc.ncx':
        if len(str(num)) == 1:
            return '00' + str(num)
        elif len(str(num)) == 2:
            return '0' + str(num)
    elif type == 'Image':
        if len(str(num)) == 1:
            return '0' + str(num)
        elif len(str(num)) == 2:
            return str(num)
    else:
        return ''
# Returns alphanumeric string for sorting based off of the passed title and author strings
def getSortString(title, author):
    title_str = removeArticles(title)
    title_str = alphanumString(title_str)
    author_str = alphanumString(author)
    return title_str.lower() + ' ' + author_str.lower()

### Passed an Object
### Returns String
def getID(title_text, author_text):
    raw_string = ''
    title_text = removeArticles(title_text)
    author_text = removeArticles(author_text)
    raw_string = title_text[:10] + ' ' + author_text[:10]
    if raw_string != '':
        string = alphanumString(raw_string)
        string = re.sub('\s*','', string)
    return string
# Passed a work object, returns alphanumeric name for epub file
def getStorageName(object):
    raw_string = ''
    title_text = object.getTitle()
    author_text = object.getAuthor()
    raw_string = title_text[:25] + ' ' + author_text[:25]
    if raw_string != '':
        string = re.sub('\s+',' ', raw_string.lower())
        string = removeArticles(string)
        string = re.sub(' ','_', string)
        string = alphanumString(string)
        sorting_target = string[:50].strip()
        sortstring = filename(sorting_target)
    return sortstring
# Generate subIDs from work object for work contents
def getSubID(object):
    # Establish proper chapter numbering
    if object.getType() == 'Preface':
        chapter_subID = 'c000'
    elif object.getType() == 'TOC':
        chapter_subID = 'c000toc'
        if object.getName() == 'series_page.xhtml':
            chapter_subID = 'c000series'
    else:
        chapter_subID = formatNum(object.getNumber(), 'manifest_chapter_numbering')
    return chapter_subID
# Passed an image, returns the file type
def getImageType(image):
    file_type = 'jpeg'
    if '.png' in image:
        file_type = "png"
    elif '.gif' in image:
        file_type = "gif"
    return file_type
# Generates Name string from work object
def generateNameString(object):
    name_string = alphanumString(object.getTitle()[:25] + "_" + object.getAuthor()[:10])
    return name_string
# Generates an old name/new name tuple for each image in the passed object
def generateNameTuples(object, name_string):
    name_tuples = []
    object.images = sorted(object.images) # Sort by the numbers at the end of the file name
    for image in object.images:
        if name_string not in image:
            num = formatNum(object.images.index(image), 'Image')
            new_name = name_string + num + f'.{getImageType(image)}'
            if image != new_name:
                name_tuples.append((image, new_name))
        else:
            name_tuples.append(None)
    # if name_tuples != []:
    #     print(name_tuples)
    return name_tuples
# Returns old name/new name tuples for each image in the passed object
def nameImages(object):
    object.images = list(set(object.images))
    tuple_list = []
    if object.getType() == 'Anthology':
        for work in object.contents:
            if work.image_bool:
                name_tuples = generateNameTuples(work, f'{object.getAbbr()}_{generateNameString(work)}')
                for name_tup in name_tuples:
                    if name_tup != None:
                        tuple_list.append(name_tup)
    else:
        name_tuples = generateNameTuples(object, generateNameString(object))
        for name_tup in name_tuples:
            if name_tup != None:
                tuple_list.append(name_tup)
    return tuple_list

## Passed Ao3 HTML Text, returns string(s)
# Grab Update Value from AO3 HTML
def grabUpdateValue(text):
    update_value = False
    if ('Chapters: ' in text) and ('Completed: ' not in text):
        update_value = True
    return update_value
# Grab AO3 Tags string from text
def grabTags(text):
    tags_text = []
    tags = text[text.find('<dl class="tags">')+ 18:text.find('</dl>')].split('</dd>')[:-1]
    for i in tags:
        fix_tags = re.sub('<a [^>]*?>', '', i)
        fix_tags = re.sub('\s*</a>\s*', '', fix_tags)
        fix_tags = re.sub('\s*</dt>\s*', '\n\t</dt>', fix_tags)
        fix_tags = re.sub('<dt [^>]*>', '\t<dt>', fix_tags)
        fix_tags = re.sub('<dd [^>]*>', '\n\t<dd>', fix_tags)
        tags_text.append(fix_tags.strip())
    tags_text = '\n\t</dd>'.join(tags_text)
    tags_text = re.sub('>\n\s*<dt>','>\n\t<dt>', tags_text)
    return tags_text
# Grab Title string from text
def grabTitle(text):
    return text.partition('<h1 class="calibre6" id="calibre_pb_1">')[2].partition('</h1>')[0].strip()
# Grab Author string from text
def grabAuthor(text):
    # By Default, the author is Anonymous
    author = 'Anonymous'
    author_text = text.partition('<h1 class="calibre6" id="calibre_pb_1">')[2].partition('</div>')[0]
    if re.search('rel="author">', author_text):
        author_list = re.findall('<a [^>]*?>(.*?)</a>', author_text)
        # author_list = list(set(author_list))
        author = ", ".join(author_list)
    author = re.sub('<[^>]+>', '', author)
    author = re.sub(' \([^\)]+\)', '', author)
    return author
# Grab Summary string from text
def grabSummary(text):
    summary = text.partition('Summary</p>')[2].partition('<blockquote class="userstuff">')[2].partition('</blockquote>\n')[0].strip()
    summary = re.sub('<(?P<cap>(p|i|b|e)) [^>]*?>', '<\g<cap>>', summary)
    summary = re.sub('</?a[^>]*?>', '', summary)
    summary = re.sub('\s*?</?(blockquote|div)[^>]*?>\s*?', '', summary).strip()
    summary = re.sub('</p>[\n|\t|\s]*?<p>', '</p>\n\t<p>', summary)
    if summary.startswith('<p>'):
        summary = summary[3:]
    if summary.endswith('</p>'):
        summary = summary[:-4]
    # print(summary)
    return summary
# Grab Link string from text
def grabLink(text):
    return text.partition('Archive of Our Own</a> at <a href="')[2].partition('">http://')[0].strip()
# Grab Fandom string from text
def grabFandom(text):
    return text.partition('</title>')[0].partition('<title>')[2].split(' - ')[2].strip()
# Grab Chapter Header string from text
def grabHeader(text):
    header = text.partition('</h2>')[0].split('">')[-1].strip()
    return header
# Grab Chapter Text string from text
def grabChapter(text):
    soup = BeautifulSoup(text, 'html.parser')
    chapter = soup.find('div', {'class': 'userstuff2'})
    chapter = str(chapter)
    return chapter
def grabAuthorNotes(text):
    soup = BeautifulSoup(text, 'html.parser')
    notes = soup.find('div', id=re.compile('endnotes\d+'))
    notes = str(notes)
    if notes == 'None':
        notes = ''
    return notes

def getSeriesTitle(text):
    series_title = text.partition('<title>')[2].partition(' Series Page</title>')[0].strip()
    return series_title
def getSeriesSummary(text):
    summary = re.findall('<br/>\[Words\: [\d|,]+\]\n\t<br/>(?P<SUMM>.*?)\n\t</p><p>\n\t<u>', text, flags=re.S)[0]
    return summary
def getSeriesLink(text):
    series_link = text.partition("LINK: '")[2].partition("'")[0].strip()
    return series_link

# Grab Series Number from text
def grabSeriesNumber(text, series_title):
    series_num = ''
    # Grab the Series Tags
    series_str = re.findall('<dt[^>]*>Series:\s*</dt>\s*<dd>\s*?(?P<SERI>.+?)\s*</dd>', text, flags=re.S)[0]
    series_str = re.sub('\n', ' ', series_str)
    series_str = re.sub('&amp;', '&', series_str)
    series_str = re.sub(', Part (?P<CAP>\d+) of ', '\nPart \g<CAP> of ', series_str)
    series_strs = series_str.split('\n')
    # Match with the Series Title
    for str in series_strs:
        series_data = re.findall('Part (?P<NUM>\d+) of (?P<SERI>.*)', str)[0]
        if series_data[1] == re.sub('&amp;', '&', series_title):
            series_num = series_data[0]
    # Automatic Error Handling
    if series_num == '':
        print('ERROR: Series Number Not Found')
        print(f"Series Title: {series_title}")
        print(f"Series String: {series_str}")
        print(f"Series Data: {series_data}")
    return series_num

### Passed File Name and Text Tuples
### Returns string
# Returns the finished preface text
def processRawPreface(tuples):
# Grab values from raw preface files
    for file in tuples:
        filename = file[0]
        text = file[1]
        if '_split_000' in filename:
            update_value = grabUpdateValue(text)
            link = grabLink(text)
            fandom = grabFandom(text)
            tags_text = grabTags(text)
            series = ''
            series_num = ''
        elif '_split_001' in filename:
            title = grabTitle(text)
            author = grabAuthor(text)
            summary = grabSummary(text)
# Create the Preface
    preface_text = classobj.Preface.assemble(update_value, link, title, author, fandom, series, series_num, tags_text, summary)
    return preface_text
# Returns the finished chapter text and filename tuples
def processRawChapters(tuples):
    new_tuples = []
    # Sort the raw chapter tuples
    # For each tuple, rename the file and format the text
    for file in tuples:
        text = file[1]
        num = tuples.index(file) + 1
        new_filename = 'chapter' +  str(num) + '_1.xhtml'
        chapter_text = grabChapter(text)
        header = grabHeader(text)
        notes = grabAuthorNotes(text)
# here is where to make corrections in the text itself
        # chapter_text = basic_editing(chapter_text)
        chapter_text = classobj.Chapter.assemble(header, chapter_text, notes)
        new_tuples.append([new_filename, chapter_text])
    return new_tuples


### Make HTML for Files
def tag(tag, type='open', contents=''):
    closure = ''
    if type == 'close':
        closure = '/'
    return '<' + closure + tag + contents + '>'
# Make the HTML text for the entire file
def makeHTMLText(head, title, body):
    return '\n\t'.join([
        tag('?xml', 'open', ' version="1.0" encoding="UTF-8"?'), 
        tag('html', 'open', ' xmlns="http://www.w3.org/1999/xhtml"'),
        head, title, body,
        tag('html', 'close')])
def makeHeadHTML(title, type, style, data=""):
    return '\n\t'.join([
            tag('head') + data,
            '\t' + tag('title') + title + type + tag('title', 'close'),
            '\t' + tag('link', 'open', ' href="../stylesheet_' + style + '.css" type="text/css" charset="UTF-8" rel="stylesheet"/'),
            tag('head', 'close')])
def makeDataHTML(update, link, tags):
    return '\n\t\t'.join([
            f"\n\t<!--UPDATE: '{update}'",
            f"LINK: '{link}'",
            f"SPECIAL: '{tags}'-->"])
def makeTitleHTML(title, type):
    return '\n\t'.join([
            tag('h1') + title + type + tag('h1', 'close')])
def makeBodyHTML(text, type=None):
    if type == None:
        return '\n\t'.join([
                tag('body'),
                '\t' + text,
                tag('body', 'close')])
    elif type == 'TOC':
        return '\n\t'.join([
            tag('body'),
            tag('div', 'open', ' class="meta"'),
            '\t' + text,
            tag('div', 'close'),
            tag('body', 'close')])

# Make the HTML fragments for the Descriptions
# Link [Title by Author]
def makeStoryLinkHTML(ID, link, title, author):
    return '\n\t'.join([
            tag('u'),
                tag('a', 'open', 
                    ' id="' + ID + \
                    '" href="' + link + '"') + \
                        title + ' by ' + author,
                tag('a', 'close'), 
            tag('u', 'close')])
# Wordcount
def makeWordcountHTML(wordcount):
    return '\n\t'.join([
            tag('br', 'open', '/') + \
                '[Words: ' + formatNum(str(wordcount), 'Word') + ']'])
# Works Count
def makeWorksCountHTML(works_count):
    return '\n\t'.join([
            tag('br', 'open', '/') + \
                '[Works: ' + str(works_count) + ']'])
# Summary
def makeSummaryHTML(summary):
    return '\n\t'.join([
            tag('br', 'open', '/') + \
                re.sub('\s*\n+\s*','\n\t<br/>', summary)])
# Link [Part x of series]
def makePartLinkHTML(link, ID,  number, title):
    return '\n\t'.join([
        tag('br', 'open', '/'), 
            tag('i'),
                tag('a', 'open', ' href="' + link + '#' + ID + '"') + \
                    'Part ' + str(number) + \
                    ' of ' + title,
                tag('a', 'close'),
            tag('i', 'close')])

# Make the TOC HTML Text
def makeTOCText(title, body):
    text = ''
    for chapter in body:
        indent_level = '4'
        if chapter.getNumber() == 1:
            indent_level = '3'
        # Make the TOC Entry
        text += '\n\t' + tag('p', 'open', ' class="calibre_' + indent_level + '"') + '\n\t' + \
                tag('a', 'open', ' href="' + chapter.getName() + '"') + \
                    str(chapter.getNumber()) + '. ' + \
                    chapter.getHeader() + \
                tag('a', 'close') + tag('p', 'close')
    return makeHTMLText(
        makeHeadHTML(title, ' TOC', 'Gen'),
        makeTitleHTML(title, ' TOC'),
        makeBodyHTML(text, 'TOC'))
# Make the Series Page HTML Text
def makeSeriesPageText(series):
    series_link = '../1/series_page.xhtml'
    mainID = getID(series.title, series.author) + '00'
    guide_link = series_link + '#' + mainID
    # Make the Main Series Entry
    text = '\n\t'.join([
        tag('p'),
            makeStoryLinkHTML(mainID, guide_link, series.title, series.author),
            makeWorksCountHTML(len(series.contents)),
            makeWordcountHTML(series.wordcount),
            makeSummaryHTML(series.summary),
        tag('p', 'close')])
    # Make the Series Page Entry Entries
    for entry in series.contents:
        storyID = getID(series.title, series.author) + formatNum(str(entry.number), 'Entry')
        story_link = '../' + str(entry.number) + '/'+ entry.preface.getName()
        # Add Preface Link to Series Page
        # If No Link, add marker
        if '</blockquote>\n\t</div>' in entry.preface.text:
            entry.setPreface(re.sub('</blockquote>\n\t</div>','</blockquote>\n\t<p>\t</p><a href="\n\t</div>', entry.preface.getText()))
        # Update Link
        entry.setPreface(
            re.sub('<p>\t</p>.*<a href=".*',
            '<p>\t</p><a href="' + series_link + '#' + storyID + '">Back to Series Page\n\t</a>\n\t</div>\n\t</body>\n\t</html>',
            entry.preface.getText(), flags = re.S))
        # Make Entry
        text += '\n\t'.join([
            tag('p'),
                makeStoryLinkHTML(storyID, story_link, entry.title, entry.author),
                makeWordcountHTML(entry.wordcount),
                makeSummaryHTML(entry.summary),
                makePartLinkHTML(series_link, mainID, entry.number, series.title),
            tag('p', 'close')])
    return makeHTMLText(
        makeHeadHTML(series.title, ' Series Page', 'Gen', makeDataHTML(series.UPDATE, series.LINK, series.SPEC)),
        makeTitleHTML(series.title, ' Series Page'), 
        makeBodyHTML(text))

# Make Formatting Text from work object
def makeDescription(object):
    return '\n' + object.title + ' by ' + object.author
def makeManifest(object, work, group):
    file_path = ''
    work_ID = ''
    if group != None:
        file_path = formatNum(group, 'Path') + formatNum(work, 'Path')
        work_ID = formatNum(group, 'manifest_group_numbering') + formatNum(work, 'manifest_work_numbering')
    mani = ''
    if object.getType() == 'Singleton':
        for i in object.contents:
            mani = mani + '\n\t\t<item href="' + file_path + i.getName() + '" id="' + \
            work_ID + getSubID(i) + '" media-type="application/xhtml+xml"/>'
    elif object.getType() == 'Series':
        for entry in object.contents:
            for i in entry.contents:
                mani = mani + '\n\t\t<item href="' + file_path + \
                formatNum(entry.number, 'Path') + i.getName() + '" id="' + \
                work_ID + formatNum(entry.number, 'manifest_entry_numbering') + \
                getSubID(i) + '" media-type="application/xhtml+xml"/>'
    return mani
def makeSpine(object, work, group):
    work_ID = ''
    if group != None:
        work_ID = formatNum(group, 'manifest_group_numbering') + formatNum(work, 'manifest_work_numbering')
    spine = ''
    if object.getType() == 'Singleton':
        for i in object.contents:
            spine += '\n\t\t<itemref idref="' + work_ID + getSubID(i) + '"/>'
    elif object.getType() == 'Series':
        for entry in object.contents:
            for i in entry.contents:
                spine += '\n\t\t<itemref idref="' + work_ID + \
                formatNum(entry.number, 'manifest_entry_numbering') + getSubID(i) + '"/>'
    return spine
def makeTOCNCX(object, work, group):
    file_path = ''
    work_ID = '0'
    if group != None:
        file_path = formatNum(group, 'Path') + formatNum(work, 'Path')
        work_ID = str(group) + '_' + str(work)
    if object.getType() == 'Series':
        file_name = '1/series_page.xhtml'
    else:
        file_name = object.preface.getName()
    return '\n\t\t'.join(['',
        tag('navPoint', 'open', ' id="num_' + work_ID + '" playOrder="' + work_ID + '"'),
        '\t' + tag('navLabel'),
            '\t\t' + tag('text') + \
                object.title + \
            tag('text', 'close'),
        '\t' + tag('navLabel', 'close'),
        '\t' + tag('content', 'open', ' src="' + file_path + file_name + '"/'),
        tag('navPoint', 'close')])
def makeGuide(object, work, group, abbr_fandom):
    work_ID = ''
    file_path = ''
    if group != None:
        work_ID = formatNum(group, 'Group') + formatNum(work, 'GuideID')
        file_path = formatNum(group, 'Path') + formatNum(work, 'Path')
    # Make Guide Entry for Singleton
    if object.getType() == 'Singleton':
        # Check if guide links exist
        if '</blockquote>\n\t</div>' in object.preface.text:
                object.setPreface(re.sub('</blockquote>\n\t</div>','</blockquote>\n\t<p>\t</p><a href="\n\t</div>', object.preface.getText()))
        # Recreate the Preface with updated links
        object.setPreface(re.sub('<p>\t</p>.*<a href=".*', '<p>\t</p><a href="../../guide.html#' + \
            abbr_fandom + work_ID + '">Back to Guide\n\t</a>\n\t</div>\n\t</body>\n\t</html>', object.preface.getText(), flags = re.S))
        return '\n\t'.join(['',
                tag('p'),
                    makeStoryLinkHTML(abbr_fandom + work_ID, file_path + object.preface.getName(), object.title, object.author),
                    makeWordcountHTML(object.wordcount),
                    makeSummaryHTML(object.guide_summary),
                tag('p', 'close')])
    elif object.getType() == 'Series':
        return '\n\t'.join(['',
                tag('p'),
                    makeStoryLinkHTML(abbr_fandom + work_ID, file_path + '1/series_page.xhtml', object.title, object.author),
                    makeWorksCountHTML(len(object.contents)),
                    makeWordcountHTML(object.wordcount),
                    makeSummaryHTML(object.guide_summary),
                tag('p', 'close')])

def makeSingletonGuide(object_list):
    text = ''
    for object in object_list:
        if object.getType() == 'Singleton':
            text += '\n\t'.join(['',
                    tag('p'),
                    tag('u'),
                        object.title + ' by ' + object.author,
                    tag('a', 'close'), 
                    tag('u', 'close'),
                    makeWordcountHTML(object.wordcount),
                    makeSummaryHTML(object.guide_summary),
                    tag('p', 'close')])
        elif object.getType() == 'Series':
            text += '\n\t'.join(['',
                    tag('p'),
                    tag('u'),
                        object.title + ' by ' + object.author,
                    tag('a', 'close'), 
                    tag('u', 'close'),
                        makeWorksCountHTML(len(object.contents)),
                        makeWordcountHTML(object.wordcount),
                        makeSummaryHTML(object.guide_summary),
                    tag('p', 'close')])
    guide_file = open('guide.html', 'w')
    guide_file.write(classobj.Guide.assemble('guide.html', text))
