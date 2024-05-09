import dir
import lib, appclass, active

from button import marginals

from guizero import Box, PushButton, CheckBox

from app import main

'''Exclusive Functionality'''
# View/Sort/Filter Works in Misc Library
# Upload/Write/Scrape/Remove Works from Misc Lib
# Make Series from Objects in Misc Lib
# Download Works/Get CSV Info from Ao3 Links
# Download Works from Misc Lib

# + Selecting Works shows info (like workEd)
# + Edit Works button that opens WorkEd for Misc Lib (if no work selected, opens with first selected)

screen = Box(main.app, visible=False, align="top", border=0, width="fill", height="fill")

tab = PushButton(main.header, command=main.update, args=['Misc Library', screen], text="Misc Library", align="left", width="fill", height="fill")

'''Footer'''
footer = appclass.MarginalElement(screen, buttons=[
                                ['upload', marginals.uploadWorks, [], 'Upload Works', True],
                                
                                ['series', marginals.makeSeries, [], 'Make Series', False],
                                ['download', marginals.downloadWorks, [], 'Download Works', False],
                                ['remove', marginals.removeWorks, [], 'Remove Works', False],
                                ['edit', marginals.editWork, [], 'Edit Work', False],

                                ['write', marginals.makeWorks, ['write'], 'Write Works', True],
                                ['save', marginals.makeWorks, ['save'], 'Save', False],
                                
                                ['scrape', marginals.makeWorks, ['scrape'], 'Scrape Works', True],
                                ['check', marginals.checkUpdates, [], 'Check for Updates', False],
                                ['grab', marginals.grabLinks, [], 'Grab Links', False],
                                ['start', marginals.scrapeLinks, [], 'Scrape Links', False],

                                ['cancel', marginals.makeWorks, [None], 'Cancel', False],
                                ['back', marginals.back_button_pressed, [], 'Back', False]
                                ])
footer.save.disable()
footer.start.disable()

'''List Box'''
misc_library_box = Box(screen, align="left", border=0, width=250, height="fill")
sort = appclass.SortList(misc_library_box, selected="Alphabetical", options=['Alphabetical', 'Author', 'Fandom', 'Word Count', 'Series', 'Singletons'], lib=lib.misc)
# Listbox
listbox = appclass.ListElement(misc_library_box, active.work, items=lib.misc, width=250, multiselect=True)
sort.list = listbox

details = Box(screen, align="right", width="fill", height="fill", visible=False)

stats = appclass.TextDisplay(details, lines=[
    ("work_title", 20, 500),
    ("author", 15, 500),
    ("fandom", 15, 500),
    ("words", 15, False),
    ("summary", 12, 500)
    ])
stats.summary.bg = "white"

'''Write'''
write_master = Box(screen, visible=False, align="right", border=0, width=500, height="fill")
work_box = Box(write_master, align="top", width="fill", height="fill")
# Title & Author
title_author_box = Box(work_box, align="top", width="fill", height=40)
title = appclass.InputElement(title_author_box, "Title:")
author = appclass.InputElement(title_author_box, "Author:", align="right")
# Fandom & Url
fandom_url_box = Box(work_box, align="top", width="fill", height=40)
fandom = appclass.InputElement(fandom_url_box, "Fandom:")
url = appclass.InputElement(fandom_url_box, "URL:", align="right")
# Summary & Content
summary = appclass.InputElement(work_box, "Summary:", align="top", label="top", height=80, multiline=True, scrollbar=True)
contents = appclass.InputElement(work_box, "Contents (include HTML):", align="top", label="top", height="fill", multiline=True, scrollbar=True)

'''Scraper'''
scraper_master = Box(screen, align="right", border=0, width=500, height="fill", visible=False)

scraper_footer = Box(scraper_master, align="bottom", width="fill", height=40)

links = appclass.InputElement(scraper_master, "Paste AO3 Links Here", align="top", label="top", height="fill", multiline=True, scrollbar=True)

clear_button = PushButton(scraper_footer, command=links.clear, align="left", text="Clear Links", width="fill", height="fill")
csv_check_box = CheckBox(scraper_footer, align="left", text="CSV", width="fill", height="fill")
download_check_box = CheckBox(scraper_footer, align="left", text="Download", width="fill", height="fill")
upload_check_box = CheckBox(scraper_footer, align="left", text="Upload", width="fill", height="fill")

def clear():
    # Clear all textboxes
    title.clear()
    author.clear()
    fandom.clear()
    url.clear()
    summary.clear()
    contents.clear()
    links.clear()
    # Clear all checkboxes
    csv_check_box.value = False
    download_check_box.value = False
    upload_check_box.value = False

def reload():
    listbox.clear()
    lib.load_misc_library()
    for i in sorted(lib.misc, key = lambda x:x.getSort()):
        listbox.append(i)

def updateButtons():
    test_buttons = [
        (bool(contents.textbox.value != '\n'), [footer.save]),
        (bool(links.getValue() != '\n' and any([csv_check_box.value, download_check_box.value, upload_check_box.value])), [footer.start]),
    ]
    for test, elements in test_buttons:
        if test:
            for element in elements:
                element.enable()
        else:
            for element in elements:
                element.disable()

def update(type=None):
    element_visibility = [
        # If type == None
        (bool(type == None and active.work.obj == ""), [footer.upload, footer.write, footer.scrape]),
        # If Misc Mode
        (bool(active.work.obj != ""), [details, footer.series, footer.download, footer.remove, footer.edit, footer.back]),
        # If type is write
        (bool(type == "write"), [write_master, footer.save, footer.cancel]),
        # If type is scrape
        (bool(type == "scrape"), [scraper_master, footer.grab, footer.start, footer.check]),
        # Override
        (bool(type == "write" or type == "scrape"), [footer.cancel])]
    for test, elements in element_visibility:
        for element in elements:
            element.visible = test

    if type == "write" or type == "scrape":
        misc_library_box.disable()
    else:
        misc_library_box.enable()

    updateButtons()

# Add Button Update Commands
contents.textbox.update_command(updateButtons)
links.textbox.update_command(updateButtons)
csv_check_box.update_command(updateButtons)
download_check_box.update_command(updateButtons)
upload_check_box.update_command(updateButtons)

listbox.gui = appclass.GUIConnector(update=[stats],
                                    method=[update])
