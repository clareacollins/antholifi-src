import re
import itertools


def detectAuthor(all_authors):
    unique_authors = set(all_authors)
    # If there's only one author, return it
    if len(unique_authors) == 1:
        return list(unique_authors)[0]
    # If there's more than one author, return the most common
    else:
        author_counts = []
        for author in unique_authors:
            author_counts.append((author, all_authors.count(author)))
        max_count = max(author_counts, key=lambda x: x[1])[1]
        final_authors = []
        for inst in author_counts:
            author, count = inst
            if count == max_count:
                final_authors.append(author)
        final_authors = sorted(final_authors)
        return ", ".join(final_authors)

### Passed Lists
### Returns Overlapping Objects
def getWorks(selected_list, library):
    objects_list = []
    if selected_list != None:
        for work in selected_list:
            for object in library:
                if work == str(object):
                    objects_list.append(object)
    return objects_list

def getSeriesPage(series_contents):
    for file in series_contents:
        if 'series_page' in file:
            return file

### Passed Data
### Returns Bool
#
def getType(contents):
    counts = []
    for file in contents:
        counts.append(file.count('/'))
    if min(counts) == 0:
        return 'Work'
    if min(counts) == 1:
        return 'Series'
    if min(counts) >= 2:
        return 'Anthology'

# Passed a list of contents, returns a bool if it's a series
def isSeries(contents):
    isSeriesBool = False
    for file in contents:
        if 'title_page' in file:
            isSeriesBool = True
    return isSeriesBool
# Passed a list of contents, returns a bool if it's a raw AO3 file
def isRaw(contents):
    isRawBool = False
    for file in contents:
        if '_split_' in file and 'index_' not in file:
            isRawBool = True
    return isRawBool

### Passed Data
### Returns Filtered List
# Passed list of file name strings, returns list of non-formatting file name strings
def noFormatting(zip_contents_list):
    forbidden = ['.css', '.opf', 'mimetype', 'META-INF', '.ncx']
    contents = []
    for y in zip_contents_list:
        if not any(x in y for x in forbidden):
            if 'cover.xhtml' != y and 'guide.html' != y:
                contents.append(y)
    return contents
# Passed a list of file name strings, returns list of image file names
def onlyImages(contents):
    images = []
    for file in contents:
        if '.xhtml' not in file and '.html' not in file:
            if file != 'cover.jpg':
                images.append(file)
    return images
# Passed a list of file name strings, returns list of work file names
def onlyWorks(contents):
    works = []
    for file in contents:
        if '.xhtml' in file or '.html' in file:
            works.append(file)
    return works

### Passed Data
### Returns Grouped List
# Groups Series Contents
def groupEntries(series_contents):
    entry_contents = []
    for key, group in itertools.groupby(series_contents, lambda x: x.split('/')[-2]):
        entry_contents.append(list(group))
    return entry_contents
# Groups Anthology Contents
def groupWorks(contents):
    group_list = []
    for key, group in itertools.groupby(contents, lambda x: x[:x.find('/', 2)]): # ignores anth groups (e.g. 1/)
        group_list.append(list(group))
    return group_list
