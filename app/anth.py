import lib
import active, appclass, anthclass

from button import marginals

from guizero import Box, PushButton

from app import main

'''Exclusive Functionality'''
# View Anthologies (from Anth Library) and their Works
# Add/Remove Anthologies from Anth Library
# Create Anthologies from folder
# Download Anthologies from Anth Library

screen = Box(main.app, align="top", border=0, width="fill", height="fill")

tab = PushButton(main.header, command=main.update, args=['Anthology Library', screen], text="Anthology Library", align="left", width="fill", height="fill")
tab.bg = "white" # Anth, the default button, should start out highlighted

'''Footer'''
footer = appclass.MarginalElement(screen, buttons=[
                                ['create', marginals.createAnthology, [], 'Create Anthology', True],
                                ['upload', marginals.uploadAnthology, [], 'Upload Anthology', True],
                                ['download', marginals.downloadAnthology, [], 'Download Anthology', False],
                                ['remove', marginals.removeAnthology, [], 'Remove Anthology', False],
                                ['edit', marginals.editAnthology, [], 'Edit Anthology', False],
                                ['back', marginals.back_button_pressed, [], 'Back', False]
                                ])

'''Screen'''
# Anthology Library List 
library = appclass.ListElement(screen, active.anth, items=lib.anth, width=250)
# Display Master
anth_master = Box(screen, visible=False, width="fill", height="fill")
    # Anthology Contents Display Master
contents_master = Box(anth_master, align="bottom", width="fill", height="fill")
        # Contents Scroll
contents_scroll = appclass.ScrollElement(contents_master, active.work, active.index.work, visible=True, align="right", width=35)
        # Contents List
contents = appclass.ListElement(contents_master, active.work, active_index=active.index.work, align="left")
    # Work Master
work_master = Box(anth_master, align="top", width="fill", height=220)
        # Scrollbars
fandom_scroll = appclass.ScrollElement(work_master, active.anth, active.index.page, height=30)
entry_scroll = appclass.ScrollElement(work_master, active.work, active.index.entry, height=30)
        # Work Display Master
main_box = Box(work_master, width="fill", height="fill")
            # Work Display
anth_stats = appclass.TextDisplay(main_box, lines=[
    ("title", 20, False),
    ("fandom", 15, 500),
    ("words", 15 , False),
    ("works", 15, False)
    ])
work_stats = appclass.TextDisplay(main_box, align="left", height=175, lines=[
    ("work_title", 15, 250),
    ("entry_title", 12, 250),
    ("author", 12, 250),
    ("fandom", 12, 250),
    ("words", 12, False)
])
summary = appclass.SummaryBox(main_box, width=250)

def update():
    element_visibility = [
        # Visible depending on active.anth.obj
        (bool(active.anth.obj != ""), [anth_master, footer.download, footer.remove, footer.edit, footer.back]),
        (bool(active.anth.obj == ""), [footer.create, footer.upload]),
        # Visible depending on active.work.obj
        (bool(active.work.obj == ""), [anth_stats.words, anth_stats.works, anth_stats.fandom]),
        (bool(active.work.obj != ""), [work_stats.master, summary.master]),
        # Other
        (bool(active.index.entry.int != 0), [work_stats.entry_title])]
    for test, elements in element_visibility:
        for element in elements:
            element.visible = test

    # Fandom Scroll [can't go into element visibility because their hide command is different]
    fandom_scroll.visible(bool(len(active.anth.getAnth()) != 1))
    # Entry Scroll
    entry_scroll.visible(bool(isinstance(active.work.obj, anthclass.Series)))
    # Summary [Can't go in element visibility because the second bool depends on the first]
    summary.listbox.visible = bool(isinstance(active.work.obj, anthclass.Series) and active.index.entry.int == 0)
    summary.summary.visible = not summary.listbox.visible


'''GUI Connections'''
library.gui = appclass.GUIConnector(reset=[active.work, active.index],
                                    fill=[(contents, library.active_obj.getContents)],
                                    scroll=[(contents_scroll, library.active_obj.getContents), (fandom_scroll, library.active_obj.getAnth)],
                                    update=[anth_stats],
                                    method=[update])
fandom_scroll.gui = appclass.GUIConnector(reset=[active.work],
                                          zero=[active.index.work, active.index.entry, active.index.summary],
                                          fill=[(contents, library.active_obj.getContents)],
                                          scroll=[(contents_scroll, library.active_obj.getContents), (fandom_scroll, library.active_obj.getAnth)],
                                          update=[anth_stats],
                                          method=[update])
contents.gui = appclass.GUIConnector(zero=[active.index.entry, active.index.summary],
                                          scroll=[(contents_scroll, library.active_obj.getContents), (entry_scroll, contents.active_obj.getContents)], 
                                          update=[work_stats, summary],
                                          method=[update])
contents_scroll.gui = appclass.GUIConnector(zero=[active.index.entry, active.index.summary],
                                          scroll=[(contents_scroll, library.active_obj.getContents), (entry_scroll, contents.active_obj.getContents)],
                                          update=[work_stats, summary],
                                          method=[update])
entry_scroll.gui = appclass.GUIConnector(scroll=[(entry_scroll, contents.active_obj.getContents)],
                                          update=[work_stats, summary],
                                          method=[update])
summary.gui = appclass.GUIConnector(scroll=[(entry_scroll, contents.active_obj.getContents)],
                                          update=[work_stats, summary],
                                          method=[update])

