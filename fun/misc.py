import dir
import lib
import anthclass
import utils
import scraper

import app, active

import os, re
import tkinter as tk
import pickle
import time

# Uploads epub file(s) to the misc library
def upload():
# Open a dialog to select file(s) from chdir
    os.chdir(dir.lib_root)
    epub_file_list = tk.filedialog.askopenfilenames(initialdir = dir.dest, title = "Select Epub File(s)", filetypes = (("epub files","*.epub"),("all files","*.*")))
    # for every file selected, returns the full file path
    for work in epub_file_list:
        # Create object from file path and save to misc library
        object = utils.makeObject(work)
        utils.files.handleImages(object)
        utils.files.makePickle(object)
    # Reload misc library from pickles to load new object(s) to app
    lib.load_misc_library()

# Removes selected objects from the misc library
def remove():
    # Make a list of objects to remove
    objects_list = utils.other.getWorks(app.misc.listbox.getValue(), lib.misc)
    # remove active object
    if objects_list == [] and active.work.obj != '':
        objects_list.append(active.work.obj)
    # removes any associated image file(s) from misc img storage
    utils.files.removeFiles([image for object in objects_list for image in object.images], dir.misc_img)
    # remove object pickles from storage
    utils.files.removePickles(objects_list, dir.misc)
    active.work.reset()

# Creates a series object from selected objects in the misc library
def series():
    # ask for series title
    series_title = app.main.app.question('Create Series', 'Name the new Series:')
    if series_title == None or series_title == '':
        return
    # Make a list of selected objects (if there are any)
    objects_list = utils.other.getWorks(app.misc.listbox.getValue(), lib.misc)
    # remove entry pickles from storage here so series pickles are removed properly
    utils.files.removePickles(objects_list, dir.misc)
    # if there is a series in the objects, separate it
    if any([isinstance(object, anthclass.Series) for object in objects_list]):
        works_list = []
        for object in objects_list:
            if isinstance(object, anthclass.Series):
                works_list.extend(object.contents)
            else:
                works_list.append(object)
        objects_list = works_list
    # Make a series object
    series_object = anthclass.Series(objects_list, series_title, detectOrder=False)
    # add series pickle to storage
    utils.files.makePickle(series_object)
    active.work.update(series_object)
 
# Currently removes all pickles from storage and replaces all of them (should pass work_object to be deleted/saved)
def save():
# remove pickles from storage
    os.chdir(dir.misc)
    for f in os.listdir():
        os.remove(f)
    for work_object in lib.cont:
        utils.files.makePickle(work_object)

# Write
def saveWork():
    new_story_files = []
    update_value = 'False'
    # tags_fin = ''
    title = 'Untitled' if app.misc.title.isEmpty() else app.misc.title.getValue()
    author = 'Anonymous' if app.misc.author.isEmpty() else app.misc.author.getValue()
    fandom = 'Other' if app.misc.fandom.isEmpty() else app.misc.fandom.getValue()
    link = 'NONE' if app.misc.url.isEmpty() else app.misc.url.getValue()
    summary = '' if app.misc.summary.isEmpty() else app.misc.summary.getValue()
    summary = ''
    chapter_text = app.misc.contents.getValue()
    wordcount = str(len(chapter_text.split()))
# Create the Preface
    preface_text_final = "<?xml version='1.0' encoding='utf-8'?>\n\t" + '<html xmlns="http://www.w3.org/1999/xhtml">' + \
    "\n\t<head>\n\t<!--UPDATE: '" + str(update_value) + "'\n\t\tLINK: '" + link + "'\n\t\tSPECIAL: 'DIY'-->" + \
    '\n\t<title>' + title + '\n\t\t' + author + '\n\t\t' + fandom + '\n\t</title>' + \
    '\n\t<link href="stylesheet_Gen.css" type="text/css" charset="UTF-8" rel="stylesheet"/>' + \
    '\n\t</head>\n\t<body>\n\t<div class="meta">\n\t<h1>' + title + '\n\t</h1>\n\t<div class="byline">by ' + \
    author + '\n\t</div>\n\t<p>\n\tWords: ' + wordcount + '\n\t</p>\n\t<p>Summary</p>\n\t<blockquote class="userstuff">\n\t<p>' + \
    summary + '</p></blockquote>\n\t</div>\n\t</body>\n\t</html>'
    preface_obj = anthclass.Preface('preface.xhtml', preface_text_final)
    new_story_files.append(preface_obj)
    # write chapter object
    final_text = "<?xml version='1.0' encoding='utf-8'?>" + '\n<html xmlns="http://www.w3.org/1999/xhtml">' + \
    '\n\t<head>\n\t\t<title></title>\n\t\t<link href="stylesheet_Gen.css" type="text/css" charset="UTF-8" rel="stylesheet"/>' + \
    '\n\t</head>\n\t<body>\n\t<div class="meta group">\n\t<h2>\n\t</h2>\n\t</div>\n\t<!--chapter content-->\n\t<div class="userstuff">' + \
    '\n\t' + chapter_text + '\n\t</div>\n\t<!--/chapter content-->\n\t</body>\n\t</html>'
    chapter = anthclass.Chapter('chapter1_1.xhtml', final_text)
    new_story_files.append(chapter)
    object = anthclass.Singleton(new_story_files)
    # Add a pickle to storage
    os.chdir(dir.misc)
    pickle.dump(object, open(utils.string.filename(object.getSort()) + '.work', "wb+"))

def downloadWorks():
    objects_list = utils.other.getWorks(app.misc.listbox.getValue(), lib.misc)
    for object in objects_list:
        utils.files.makeEpub(object, dir.pos)


# Scrape
def scrape(links_list=None, type=None):
    # Test Data
    csvBool = app.misc.csv_check_box.value
    downloadBool = app.misc.download_check_box.value
    uploadBool = app.misc.upload_check_box.value
    if type == 'Download':
        downloadBool = 1
    # get links
    if links_list == None:
        links_list = app.misc.links.getValue().split('\n')[:-1]
    # Open Browser
    scraper.browser.login()
    # For each Link
    csv_text = ''
    print("Scraping...")
    for link in links_list:
        time.sleep(10)
        print(link)
        try:
            html = scraper.browser.scrape(link)
            utils.files.writeFile(html, fileName='htmlfic', ext='html')
            if csvBool:
                csv_text += scraper.extract.csvextract(html, link) + '\n'
        except: 
            print('Error with link: ' + link)
            continue
        # download for either
        if downloadBool or uploadBool:
            try:
                scraper.browser.download(link)
            except:
                print('Error with link: ' + link)
                continue
            # Make Work Object
            if '/works/' in link:
                file_name = os.listdir(dir.epub_temp)[0]
                object = utils.makeObject(os.path.join(dir.epub_temp, file_name))
                if downloadBool:
                    # Move file to dest
                    utils.files.moveFile(os.path.join(dir.epub_temp, file_name), dir.dest, utils.string.getStorageName(object) + '.epub')
            # Make Series Object
            elif '/series/' in link:
                # Pass Series Title and Summary
                series_title = scraper.utils.getTitle(html)
                series_summary = scraper.utils.getSeriesSummary(html)
                object_list = []
                for f in os.listdir(dir.epub_temp):
                    object_list.append(utils.makeObject(os.path.join(dir.epub_temp, f)))
                object = anthclass.Series(object_list, series_title, link, series_summary)
                if downloadBool:
                    # Add file to dest
                    utils.files.makeEpub(object, dir.dest)
            time.sleep(2.5)
            utils.files.emptyDir(dir.epub_temp)
            if uploadBool:
                utils.files.handleImages(object)
                # Add a pickle to storage
                utils.files.makePickle(object)
    utils.files.writeFile(csv_text)
    scraper.browser.close()
    app.misc.clear()
    print("Scrape Complete")

def checkForUpdates(fileName):
    # Grab the Rows from the TSV
    fileText = utils.files.readText(fileName, location=dir.storage).split('\n')[1:]

    story_obj = []
    update_links = []
    for line in fileText:
        data = line.split('\t')
        # if data[6] != "Completed":
        if data[6] != "Completed" and data[6] != "LOST":
        # if data[-4] == "Series":
            story_obj.append((data[-3], data[3]))
        
    print("Checking for Updates")
    for obj in story_obj:
        time.sleep(10)
        try:
            # Grab html
            html = scraper.browser.scrape(obj[0])
            # Grab wordcount
            if not 'series' in obj[0]:
                words = scraper.format.words(re.search('<dd class="words">\s*(?P<WORDS>[^<]+)</dd>', html).group('WORDS'))
            else:
                words = scraper.format.words(re.search('<dt>Words:</dt>\s*<dd>(?P<WORDS>[^<]+)</dd>', html).group('WORDS'))
        except AttributeError:
            print('Error with link: ' + obj[0])
        # Check by wordcount
        if int(obj[1]) != int(words):
            update_links.append(obj[0])
    utils.files.writeFile("\n".join(update_links), fileName="update_links")
    print('Finished Checking for Updates')

def updateSeries(files):
    print("Checking for Series Updates")
    for file in files:
        remakeBool = False
        print(f'Opening {os.path.basename(file)}...')
        object = utils.makeObject(os.path.join(dir.storage, "Red", "Series", file))
        html = scraper.browser.scrape(object.LINK)
        print('Grabbing Data...')
        # Grab Series Strings
        series_title = scraper.utils.getTitle(html)
        series_link = object.LINK
        series_summary = scraper.utils.getSeriesSummary(html)
        # series_words = scraper.format.words(re.search('<dt>Words:</dt>\s*<dd>(?P<WORDS>[^<]+)</dd>', html).group('WORDS'))
        series_works = re.search('<dt>Works:</dt>\s*<dd>(?P<WORKS>[^<]+)</dd>', html).group('WORKS')
        # Grab Entry Strings
        entry_list = []
        for entry_str in html.split('role="article">')[1:]:
            entry_num = scraper.utils.getEntryNum(entry_str, object.title)
            # Get Entry Basics
            entry_title = re.search('<h4 class="heading">\s*<a href="/works/(\d)+">(?P<TIT>[^<]+)</a>', entry_str).group('TIT')
            entry_words = re.search('<dd class="words">(?P<WOR>[^<]+)</dd>', entry_str).group('WOR')
            entry_words = re.sub(",", "", entry_words)
            entry_link = 'http://archiveofourown.org/works/' + re.search('<h4 class="heading">\s*<a href="/works/(?P<LINK>\d+)">(?P<TIT>[^<]+)</a>', entry_str).group('LINK')
            # Get Entry Summary
            entry_summary = scraper.utils.getEntrySummary(entry_str)
            # By Default, Assume this is a new work with no matching entry object
            entry = None
            for entry_obj in object.contents:
                if entry_obj.LINK == entry_link:
                    entry = entry_obj
                    # Remove series page if present
                    entry.contents = [file for file in entry.contents if 'series_page' not in file.getName()]
                    # print(f"Checking [{entry.number}/{series_works}] ({entry.title})...")
                    # Treat Updated Entry like New Entry
                    if int(entry_words) != entry.wordcount:
                        print(f"{entry.wordcount} -> {entry_words}")
                        entry = None
        # New Entry
            if entry == None:
                remakeBool = True
                print(f"Downloading Entry [{entry_num}/{series_works}] ({entry_title})...]")
                # Download Entry
                try:    
                    work_html = scraper.browser.scrape(entry_link)
                    time.sleep(10)
                    scraper.browser.download(entry_link)
                except:
                    print('Error with link: ' + entry_link)
                    continue
                # Make Work Object
                file_name = os.listdir(dir.epub_temp)[0]
                work_object = utils.makeObject(os.path.join(dir.epub_temp, file_name))
                # Delete File
                utils.files.removeFile(os.path.join(dir.epub_temp, file_name))
                entry_list.append(work_object)
        # Existing Entry
            else:
                if entry_title != entry.title:
                    remakeBool = True
                    print(F"Entry Title Change: {entry.title} -> {entry_title}")
                    entry.updatePreface(newTitle=entry_title)
                if series_title != entry.series or entry_num != entry.number:
                    remakeBool = True
                    # Unless Entry Number is duplicate
                    if series_title == entry.series:
                        for entry_obj in object.contents:
                            if entry_obj != entry:
                                if entry_obj.number == entry_num:
                                    # print('Cannot Change Entry Number: Duplicate Number')
                                    # Cancel Change
                                    remakeBool = False
                    if remakeBool:
                        # Has to change the text in the tags a well
                        print(F"Entry Series Change: {object.title} [{entry.number}] -> {series_title} [{entry_num}]")
                        entry.updatePreface(newSeries=series_title, newNumber=entry_num)
                if re.sub("\W|\s", "", entry_summary) != re.sub('\W|\s', '', scraper.utils.format.text(entry.summary)):
                    remakeBool = True
                    print(f"Entry Summary Change")
                    print("###")
                    print(re.sub('\n', ' ', scraper.utils.format.text(entry.summary)))
                    print("### -> ###")
                    print(entry_summary)
                    print("###")
                    entry.updatePreface(newSummary=entry_summary)
                entry_list.append(entry)
        if remakeBool:
            print("Updating Epub File")
            newObject = anthclass.Series(entry_list, series_title, series_link, series_summary)
            utils.files.makeEpub(newObject, dir.dest)
        else:
            print("No Changes Detected")
            time.sleep(10)
    print("Check Complete")

def checkUpdates():
    fileNames = tk.filedialog.askopenfilenames(initialdir = dir.storage, 
                                             title = "Select TSV File or Series Epub(s)", 
                                             filetypes = (("all files","*.*"), ("tsv file","*.tsv"),("epub file", "*.epub")))
    if fileNames == []:
        return
    scraper.browser.login()
    if fileNames[0].endswith(".tsv"):
        checkForUpdates(fileNames[0])
    else:
        updateSeries(fileNames)
    scraper.browser.close()
        

def compareData():
    # Grab the Rows from the TSV
    data_list = []
    fileText = utils.files.readText('Witcher - Red.tsv', location=dir.storage).split('\n')[1:]
    for line in fileText:
        data = line.split('\t')
        if data[6] != "LOST":
            data_list.append(line.split('\t'))
    # Grab the Work Objects
    folder_list = ["A-C", "D-H", "I-L", "M-R", "S-V", "W-Z"]

    for folder in folder_list:
        print(f"Comparing {folder} Singletons...")
        object_list = []
        for file in os.listdir(os.path.join(dir.storage, "Singletons", folder)):
            object_list.append(utils.makeObject(os.path.join(dir.storage, "Singletons", folder, file)))
        print('Objects Loaded')
        # Compare the Data
        for object in object_list:
            object_link = re.sub("http", "https", object.LINK)
            match_data = None
            for data in data_list:
                if data[-2] == object_link:
                    match_data = data
        # Compare Title
            if match_data == None:
                print(f"New Work: {object.title}")
            if object.getTitle() != match_data[0]:
                print(f"Title Change: {match_data[0]} -> {object.title}")
        # Compare Author
            if object.getAuthor() != re.sub('\s*\([^\)]+\)\s*', '', match_data[2]):
                # print(match_data[0])
                print(f"Author Change: {match_data[2]} -> {object.getAuthor()}")
        # Compare Wordcount
            if object.wordcount != int(match_data[3]):
                print(match_data[0])
                print(f"Wordcount Change: {match_data[3]} -> {object.wordcount}")
        # # Compare Summaries
            if re.sub("\W|\s", "", object.summary) != re.sub("\W|\s", "", match_data[7]):
                print(match_data[0])
                print(f"Summary Change: {match_data[7]} -> {object.summary}")
        
    print('Finished Comparing All Data')

