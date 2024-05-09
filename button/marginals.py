import lib

import active, app

import data
import fun
import gui

import copy

'''Anthology Library Footer'''
def createAnthology():
    fun.anth.create()
    lib.load_anthology_library()
    app.anth.library.refill(lib.anth)
    app.anth.library.gui.refresh(active.anth.obj)
def uploadAnthology():
    fun.anth.upload()
    lib.load_anthology_library()
    app.anth.library.refill(lib.anth)
    app.anth.library.gui.refresh(active.anth.obj)
def downloadAnthology():
    fun.anth.download()
def removeAnthology():
    fun.anth.remove()
    lib.load_anthology_library()
    app.anth.library.refill(lib.anth)
    app.anth.update()
def editAnthology():
    lib.load_edit_misc_library()
    app.edit.listbox_misc.refill(lib.edit)
    active.edit.update(copy.deepcopy(active.anth).obj)
    app.edit.update()
    app.edit.fandom_scroll.gui.refresh(active.edit.obj)

'''Edit Anthology Footer'''
def addToAnthology():
    fun.anth.addWork()
    app.edit.listbox_misc.refill(lib.edit)
    app.edit.fandom_scroll.gui.refresh(active.edit.obj)
    app.edit.update()
def removeFromAnthology():
    fun.anth.removeWork()
    app.edit.listbox_misc.refill(lib.edit)
    app.edit.fandom_scroll.gui.refresh(active.edit.obj)
    app.edit.update()
def saveAnthology():
    fun.anth.save()
    app.edit.update()
    app.anth.library.gui.refresh(active.anth.obj)
def cancelAnthology():
    fun.anth.cancel()
    app.edit.update()
    app.anth.library.gui.refresh(active.anth.obj)

'''Fandom Editing Footer'''
def saveFandom():
    app.fan.window.hide()
    active.edit.update(copy.deepcopy(active.fan).obj)
    lib.edit = copy.deepcopy(lib.fan)
    active.fan.reset()
    lib.fan = []
    app.edit.screen.enable()
    app.edit.update()
def cancelFandom():
    app.fan.window.hide()
    active.fan.reset()
    active.index.reset()
    app.edit.screen.enable()
    app.edit.update()


'''Contents Editing Footer'''
def saveWork():
    gui.cont.save()
    # gui.edit.enable()
    gui.cont.update()
    data.edit.grab()
def cancelWork():
    # gui.edit.enable()
    active.copy.reset('cont')
    active.index.reset()
    gui.cont.update()


'''Misc Footer'''
def uploadWorks():
    fun.misc.upload()
    app.misc.reload()
def makeSeries():
    fun.misc.series()
    app.misc.reload()
    app.misc.listbox.gui.refresh(active.work.obj)
    # print(app.misc.listbox.listbox.value)
    # app.misc.listbox.setValue(str(active.work.obj))
    # print(app.misc.listbox.listbox.value)
def downloadWorks():
    fun.misc.downloadWorks()
def removeWorks():
    fun.misc.remove()
    app.misc.reload()
    app.misc.update()

def editWork():
    pass

# Write/Scrape
def makeWorks(type):
    if type == 'save':
        fun.misc.saveWork()
        app.misc.misc_library_box.enable()
        app.misc.reload()
        type = None
    app.misc.update(type)
    app.misc.clear()

def scrapeLinks():
    fun.misc.scrape()

def checkUpdates():
    fun.misc.checkUpdates()

def grabLinks():
    fun.misc.compareData()

'''Back Button'''
def back_button_pressed():
    if app.main.tab == "Anthology Library":
        # If we're in a work
        if active.work.obj != '':
            # If in series, back out
            if active.index.entry.int != 0:
                active.index.entry.int = 0
                app.anth.contents.gui.refresh(active.work.obj)
            else:
                # Back out of work
                active.work.reset()
                active.index.work.int = 0
                # Update the GUI
                app.anth.library.gui.refresh(active.anth.obj)
        # If we're not looking at a work
        else:
            # if in fandom, back out
            if active.index.page.int != 0:
                active.index.page.int = 0
                # Update the GUI
                app.anth.library.gui.refresh(active.anth.obj)
            else:
                # Back out of Anthology
                active.anth.reset()
                active.index.work.int = 0
                # Update the GUI
                app.anth.update()
    elif app.main.tab == "Book Library":
        active.book.obj = ''
        app.book.update()
    elif app.main.tab == "Misc Library":
        active.work.reset()
        app.misc.update()