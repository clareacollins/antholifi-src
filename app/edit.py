import dir, lib
import appclass, active

from button import edit, marginals

from guizero import Box, CheckBox, Picture

from app import main, anth

import copy

screen =  Box(main.app, visible=False, align="top", border=0, width="fill", height="fill")

'''Footer'''
footer = appclass.MarginalElement(screen, [
                                ['add', marginals.addToAnthology, [], 'Add to Anthology', False],
                                ['remove', marginals.removeFromAnthology, [], 'Remove from Anthology', False],
                                ['save', marginals.saveAnthology, [], 'Save', True],
                                ['cancel', marginals.cancelAnthology, [], 'Cancel', True]
                                ])

'''Edit Anthology Screen'''
# Contents Master
contents_master = Box(screen, align="left", width=250, height="fill")
    # Fandom Scroll
fandom_scroll = appclass.ScrollElement(contents_master, active.edit, active.index.page, align="top", visible=False, height=30, text=True)
    # Contents List Box
listbox_cont = appclass.ListElement(contents_master, None, None, align="bottom", multiselect=True)
# Anth Master
anth_master = Box(screen, align="right", width="fill", height="fill")

### Stats Master
stats_master = Box(anth_master, align="top", width="fill", height=220)
# Box for the cover boxes
cover_main = Box(stats_master, align="left", width=120, height="fill")
change_cover = appclass.BoxedButton(cover_main, "Change Cover", edit.change_cover, align="bottom", height=30)
cover_box = Box(cover_main, align="top", width="fill", height="fill")
cover_image = Picture(cover_box, align="top", width=120, height=190)

text_master = Box(stats_master, align="left", width=300, height="fill")
button_master = Box(stats_master, align="right", width=80, height="fill")
# Box for the Multifandom checkbox
multifandom_checkbox_box = Box(button_master, align="bottom", height=40)
multifandom_checkbox = CheckBox(multifandom_checkbox_box, command=edit.multifandom_checkbox_pressed, align="right", width="fill", height="fill", text="Multi-\nfandom?")

# text
title = appclass.EditableValue(text_master, button_master, screen, active.edit, "Title", suffix=" Anthology", cutoff=10)
single_fandom = appclass.EditableValue(text_master, button_master, screen, active.edit, "Fandom", size=15, prefix="Fandom: ")
multi_fandom = appclass.BoxedText(text_master, align="top", height=0, wraplength=300)
wordcount = appclass.BoxedText(text_master, align="top", height=0)
worksnumber = appclass.BoxedText(text_master, align="top", height=0)
# other buttons
edit_fandoms = appclass.BoxedButton(button_master, "Edit Fandoms", edit.edit_fandoms)
edit_works = appclass.BoxedButton(button_master, "Edit Works", edit.edit_works)
edit_images = appclass.BoxedButton(button_master, "Edit Images", edit.edit_images)

# Misc master box
listbox_misc_box = Box(anth_master, align="bottom", width="fill", height="fill")
listbox_misc = appclass.ListElement(listbox_misc_box, None, None, items=lib.edit, align="bottom", multiselect=True)

def update():
    anth.screen.visible = bool(active.edit.obj == "")
    screen.visible = not anth.screen.visible
    if screen.visible == True:
        # Objects
        object_visibility = [
            (bool(len(active.edit.getAnth()) != 1), [fandom_scroll]),
            (bool(len(active.edit.getAnth())==1), [single_fandom]),
            (bool(len(active.edit.getAnth())!=1), [multi_fandom, edit_fandoms]),
            (bool(len(active.edit.obj.images) > 1), [edit_images])]
        for test, elements in object_visibility:
            for element in elements:
                element.visible(test)
        # Elements
        element_visibility = [
            (bool(listbox_cont.getValue() != None), [footer.remove]),
            (bool(listbox_misc.getValue() != None), [footer.add]),]
        for test, elements in element_visibility:
            for element in elements:
                element.visible = test
        # Update Text Values
        title.update(active.edit.obj.name, suffix=" Anthology")
        wordcount.setValue(active.edit.obj.getWordsString())
        worksnumber.setValue(active.edit.obj.getWorksString())
        # Fandom
        single_fandom.update(active.edit.obj.contents[0].fandom, prefix="Fandom: ")
        multi_fandom.setValue(active.edit.obj.getFandomString())
        multifandom_checkbox.value = bool(len(active.edit.getAnth())!=1)
        # Images
        cover_image.image = copy.copy(dir.anth_img + '\\' + str(active.edit.obj.images[0]))



fandom_scroll.gui = appclass.GUIConnector(fill=[(listbox_cont, active.edit.getContents)],
                                          scroll=[(fandom_scroll, active.edit.getAnth)],
                                          method=[update])
listbox_cont.gui = appclass.GUIConnector(method=[update])
listbox_misc.gui = appclass.GUIConnector(method=[update])
