import anthclass, dir

from utils import files, string, other

import os

'''Top Level Functions'''
def makeSingletonObject(work_contents):
    # Detect Raw Ao3 Files
    if other.isRaw(work_contents):
        object = processRawFiles(work_contents)
    else:
        object = processFiles(work_contents)
    # Rename Images in Temp Folder (avoids same name conflicts)
    name_tuples = string.nameImages(object)
    object.setImages(name_tuples)
    files.renameFiles(name_tuples, dir.temp_img)
    # Return the Singleton Object
    
    return object

# Passed the contents for a series, returns a Series Object (Series Epub must have a series page)
def makeSeriesObject(series_contents):
# Preserve the series title, summary and link
    series_page_text = files.readText(other.getSeriesPage(series_contents))
    series_title = string.getSeriesTitle(series_page_text)
    series_summary = string.getSeriesSummary(series_page_text)
    series_link = string.getSeriesLink(series_page_text)
# Make an object for each entry
    entry_objects = []
    for entry in other.groupEntries(series_contents):
        obj = makeSingletonObject(entry)
        entry_objects.append(obj)
# Make the series object
    series_obj = anthclass.Series(entry_objects, series_title, series_link, series_summary)
    return series_obj

# For use in makeAnthologyObject, detects if work is Singleton or Series
def makeWorkObject(work_contents):
    # Detect Series
    if other.isSeries(work_contents):
        object = makeSeriesObject(work_contents)
    else:
        object = makeSingletonObject(work_contents)
    return object

# Passed the Anthology Title and Work Object List, Returns an Anthology Object
def makeAnthologyObject(anth_contents, anth_title):
    work_list = []
    for work in other.groupWorks(anth_contents):
        work_list.append(makeWorkObject(work))
    anth_object = anthclass.Anthology(work_list, anth_title)
    return anth_object



# Processes the files in the contents list and returns a Singleton or Entry Object
def processFiles(contents):
    # Establish empty body and TOC
    Body = []
    TOC_obj = 0
    # For every file in the contents list
    for file in contents:
        # open the file
        text = files.readText(file)
        # Get the name of the file (don't let paths interfere with grabbing numbers from chapter file names)
        file = os.path.basename(file)
        # Assign Preface (Ao3 singleton, series, fanfic.net and manually assembled singletons)
        if 'preface' in file or 'title_page' in file or 'Cover_ffn.html' in file or 'index_split_000' in file:
            preface = anthclass.Preface(file, text)
        # Assign TOC
        elif 'TOC' in file:
            TOC_obj = anthclass.TOC(file, text)
        # Add chapters to the body
        elif 'series_page' not in file:
            Body.append(anthclass.Chapter(file, text))
    # Order the contents
    new_contents = orderContents(preface, TOC_obj, Body)
# Make the object
    object = anthclass.Singleton(new_contents)
    return object
# Processes the raw Ao3 files in the contents list and returns a Singleton or Entry Object
def processRawFiles(contents):
    Body = []
    TOC_obj = 0
    raw_preface = []
    raw_chapters = []
    # Trim the last file, which is the afterword
    contents = sorted(contents)[:-1]
    for file in contents:
        text = files.readText(file)
        filename = os.path.basename(file)
        if '_split_000' in filename or '_split_001' in filename:
            raw_preface.append([filename, text])
        else:
            raw_chapters.append([filename, text])
    # Process the raw preface and chapters
    preface = anthclass.Preface('preface.xhtml', string.processRawPreface(raw_preface))
    raw_chapters = sorted(raw_chapters, key=lambda x:x[0])
    for chapter in string.processRawChapters(raw_chapters):
        Body.append(anthclass.Chapter(chapter[0], chapter[1]))
    new_contents = orderContents(preface, TOC_obj, Body)
    object = anthclass.Singleton(new_contents)
    return object
# Passed the content objects for a work, assembles them to be turned into an object
def orderContents(preface, TOC_obj, Body, series_page=0):
    contents = []
    if series_page != 0:
        contents.append(series_page)
    contents.append(preface)
    if TOC_obj != 0:
        contents.append(TOC_obj)
    for chapter in Body:
        contents.append(chapter)
    return contents


# def createSeriesObject(series_contents):
#     return anthclass.Series(series_contents)
def createAnthologyObject(anth_contents, anth_title):
    return anthclass.Anthology(anth_contents, anth_title)



def arrowVisibility(arrowA, arrowB, startTest, endTest):
    if startTest:
        arrowA.visible = False
        arrowB.visible = True
    # At last page, you can only go backwards
    elif endTest:
        arrowB.visible = False
        arrowA.visible = True
    # Between those two, you can do both
    else:
        arrowB.visible = True
        arrowA.visible = True

def convertSingleFandom(new_fandom, edit_anthology_object):
    new_contents = []
    for group in edit_anthology_object.anth:
        for work in group:
            work.setFandom(new_fandom)
            new_contents.append(work)
    new_anth = anthclass.Anthology(new_contents, edit_anthology_object.name)
    return new_anth


'''NOT CONFIRMED'''
def fandomSort(anth):
    contents = []
    for i in anth:
        for y in sorted(i, key=lambda x:x.getSort()):
            contents.append(y)
    return contents
