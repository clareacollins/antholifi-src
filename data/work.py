import lib
import active
import utils

import app

def grab(type=None):
    if active.work.obj != '':
        grabAnthData()
    # if type == 'Anthology':
    #     grabAnthData()
    # else:
    #     if active.header.tab == "Anthology Library":
    #         grabAnthContData()
    #     else:
    #         grabMiscContData()

def grabAnthData():
    # title character cutoff number single vs multifandom
    if len(active.anth.obj.anth) == 1:
        cuttof_number = 67
    else:
        cuttof_number = 58
    # Assign stats
    app.anth.stats.work_title.value = utils.string.fix(active.work.obj.getTitle()[:cuttof_number])
    #app.anth.author.value = utils.string.processString(active.work.obj.getAuthor(), 200, 12)
    app.anth.stats.author.value = active.work.obj.getAuthor()
    app.anth.stats.wordcount.value = "Words: " + utils.string.formatNum(active.work.obj.getWordcount(), 'Word')
    app.anth.stats.fandom.value = active.work.obj.getFandom()
    app.anth.stats.summary.value = active.work.obj.getGuideSummary()
# If there's more than one title, it's a series
    if active.work.obj.getType() == 'Series':
        app.anth.entry_scroll_box.visible = True
    # For Page 0 of Series
        if active.index.entry == 0:
            app.anth.stats.listbox.visible = True
            app.anth.stats.summary.visible = False
            app.anth.stats.author.visible = True
            app.anth.stats.fandom.visible = True
            app.anth.stats.entry_title.visible = False
            # Text size page 0
            app.anth.stats.author.size = 15
            app.anth.stats.wordcount.size = 15
            app.anth.stats.fandom.size = 15
            # Fill a new listbox with entries
            app.anth.stats.listbox.clear()
            app.anth.stats.listbox.append(active.work.obj)
            for entry in active.work.obj.getContents():
                app.anth.stats.listbox.append(entry)
        else:
    # For other Pages of Series
            app.anth.stats.listbox.visible = False
            app.anth.stats.author.visible = False
            app.anth.stats.fandom.visible = False
            app.anth.stats.summary.visible = True
            app.anth.stats.entry_title.visible = True
            # Text size
            app.anth.stats.entry_title.size = 12
            app.anth.stats.wordcount.size = 12
            # Assign values
            app.anth.stats.entry_title.value = active.work.obj.contents[active.index.entry-1].getTitle()
            app.anth.stats.wordcount.value = "Words: " + utils.string.formatNum(active.work.obj.contents[active.index.entry-1].getWordcount(), 'Word')
            app.anth.stats.summary.value = active.work.obj.contents[active.index.entry-1].getGuideSummary()
    else:
    # If it's not a series
        app.anth.stats.summary.visible = True
        app.anth.entry_scroll_box.visible = False
        app.anth.stats.entry_title.visible = False
        app.anth.stats.listbox.visible = False

def grabAnthContData():
    # Update active work object
    active.work.obj = active.copy.cont_obj.anth[active.index.page][active.index.work]
    # Assign stats
    app.cont.title.value = utils.string.fix(active.work.obj.getTitle())#[:cuttof_number]
    app.cont.author.value = utils.string.processString(active.work.obj.getAuthor(), 200, 12)
    app.cont.wordcount.value = "Words: " + utils.string.formatNum(active.work.obj.getWordcount(), 'Word')
    app.cont.fandom.value = utils.string.processString(active.work.obj.getFandom(), 200, 12)
    app.cont.main_summary.value = active.work.obj.getSummary()
    app.cont.guide_summary.value = active.work.obj.getGuideSummary()

# If there's more than one title, it's a series
    if active.work.obj.getType() == 'Series':
        app.cont.entry_scroll_box.visible = True
    # For Page 0 of Series
        if active.index.entry == 0:
            # Button Bar
            app.cont.button_bar.visible = False
            app.cont.button_foot.align = "top"
            app.cont.view_tags_button.visible = False
            app.cont.edit_images_button.visible = False
            # Details Master
            app.cont.main_summary_box.visible = False
            app.cont.guide_summary_box.visible = False
            app.cont.change_guide_summary_button_box.visible = False
            app.cont.toggle_summary_button_box.visible = False
            app.cont.listbox_entries_box.visible = True
            # Text size page 0
            app.cont.author.size = 15
            app.cont.wordcount.size = 15
            app.cont.fandom.size = 15
            # Fill a new listbox with entries
            app.cont.listbox_entries.clear()
            app.cont.listbox_entries.append(active.work.obj)
            for entry in active.work.obj.getContents():
                app.cont.listbox_entries.append(entry)
        else:
    # For other Pages of Series
            # Stats
            app.cont.change_work_title_button.visible = False
            app.cont.change_entry_title_button.visible = True
            app.cont.author_box.visible = False
            app.cont.change_author_button_box.visible = False
            app.cont.fandom_box.visible = False
            app.cont.change_fandom_button_box.visible = False
            app.cont.order_box.visible = True
            app.cont.change_order_button_box.visible = True
            app.cont.series_back_button_box.visible = True
            app.cont.remove_entry_button.visible = True
            app.cont.button_foot.visible = False
            # Text size
            app.cont.wordcount.size = 15
            # Assign values
            app.cont.title.value = utils.string.processString(active.work.obj.contents[active.index.entry-1].getTitle(), 200, 12)
            app.cont.order.value = 'Part ' + str(active.work.obj.contents[active.index.entry-1].getNumber()) + ' of ' + active.work.obj.contents[active.index.entry-1].getSeries()
            app.cont.wordcount.value = "Words: " + utils.string.formatNum(active.work.obj.contents[active.index.entry-1].getWordcount(), 'Word')
            app.cont.main_summary.value = active.work.obj.contents[active.index.entry-1].getSummary()
            app.cont.guide_summary.value = active.work.obj.contents[active.index.entry-1].getGuideSummary()

def grabMiscContData():
    # Update active work object
    active.work.obj = lib.cont[active.index.work]
    # Assign stats
    app.cont.title.value = utils.string.fix(active.work.obj.title)#[:cuttof_number]
    app.cont.author.value = utils.string.processString(active.work.obj.author, 200, 12)
    app.cont.wordcount.value = "Words: " + utils.string.formatNum(active.work.obj.wordcount, 'Word')
    app.cont.fandom.value = utils.string.processString(active.work.obj.fandom, 200, 12)
    if not active.work.obj.getType() == 'Series':
        app.cont.main_summary.value = active.work.obj.summary
        app.cont.guide_summary.value = active.work.obj.guide_summary
    app.cont.fandom_combo_box.visible = False
# If there's more than one title, it's a series
    if active.work.obj.getType() == 'Series':
        app.cont.entry_scroll_box.visible = True
    # For Page 0 of Series
        if active.index.entry == 0:
            # Button Bar
            app.cont.button_bar.visible = False
            app.cont.button_foot.align = "top"
            app.cont.view_tags_button.visible = False
            app.cont.edit_images_button.visible = False
            # Details Master
            app.cont.main_summary_box.visible = False
            app.cont.guide_summary_box.visible = False
            app.cont.change_guide_summary_button_box.visible = False
            app.cont.toggle_summary_button_box.visible = False
            app.cont.listbox_entries_box.visible = True
            # Text size page 0
            app.cont.author.size = 15
            app.cont.wordcount.size = 15
            app.cont.fandom.size = 15
            # Fill a new listbox with entries
            app.cont.listbox_entries.clear()
            app.cont.listbox_entries.append(active.work.obj)
            for entry in active.work.obj.getContents():
                app.cont.listbox_entries.append(entry)
        else:
    # For other Pages of Series
            # Stats
            app.cont.change_work_title_button.visible = False
            app.cont.change_entry_title_button.visible = True
            app.cont.author_box.visible = False
            app.cont.change_author_button_box.visible = False
            app.cont.fandom_box.visible = False
            app.cont.change_fandom_button_box.visible = False
            app.cont.order_box.visible = True
            app.cont.change_order_button_box.visible = True
            app.cont.series_back_button_box.visible = True
            app.cont.remove_entry_button.visible = True
            app.cont.button_foot.visible = False
            # Text size
            app.cont.wordcount.size = 15
            # Assign values
            app.cont.title.value = utils.string.processString(active.work.obj.contents[active.index.entry-1].title, 200, 12)
            app.cont.order.value = 'Part ' + str(active.work.obj.contents[active.index.entry-1].number) + ' of ' + active.work.obj.contents[active.index.entry-1].series
            app.cont.wordcount.value = "Words: " + utils.string.formatNum(active.work.obj.contents[active.index.entry-1].wordcount, 'Word')
            app.cont.main_summary.value = active.work.obj.contents[active.index.entry-1].summary
            app.cont.guide_summary.value = active.work.obj.contents[active.index.entry-1].guide_summary

def clear():
    app.anth.stats.work_title.clear()
    app.anth.author.clear()
    app.anth.wordcount.clear()
    app.anth.fandom.clear()
    app.anth.summary.clear()
    app.anth.listbox_entries.clear()
    app.anth.entry_title.clear()
    app.cont.title.clear()
    app.cont.author.clear()
    app.cont.wordcount.clear()
    app.cont.fandom.clear()
    app.cont.order.clear()
    app.cont.main_summary.clear()
    app.cont.guide_summary.clear()
    app.cont.listbox_entries.clear()
def selected():
    if active.copy.cont_obj != '' or lib.cont != []:
        return app.cont.listbox_contents.value
    elif active.header.tab == "Anthology Library":
        return app.anth.listbox_contents.value
    elif active.header.tab == "Misc Library":
        return app.misc.listbox_main.value
def listbox():
    if active.copy.cont_obj != '':
        return app.cont.listbox_contents.items
    elif active.header.tab == "Anthology Library":
        return app.anth.listbox_contents.items
    elif active.header.tab == "Misc Library":
        return app.misc.listbox_main.items
