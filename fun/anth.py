import dir
import lib
import active
import utils

import app

import copy
import guizero
import os
import tkinter as tk


'''Anthology Footer Functionality'''
# Create Anthology Object from directory contents
def create(file_location=None, fandom=None, anth_title=None):
# Open a dialog to name the anthology
    # if anth_title == None:
    #     anth_title = app.main.app.question('Create Anthology','Name the New Anthology:')
    #     if anth_title == None:
    #         return
# # Open a dialog to confirm single/multi fandom
#     if fandom == None:
#         fandom = app.main.app.question('Single Fandom?','Name the Fandom if so:')
# Open a dialog to select folder from computer
    if file_location == None:
        os.chdir(dir.anth_cont)
        file_location = guizero.select_folder()
        if file_location == '':
            return
# Make the Anthology Object from the Title and Contents
    anth_object = utils.createAnthology(file_location, fandom, anth_title)
# Write Pickle, clear Ext folder, update the Active Object
    utils.files.makePickle(anth_object, anth_object.name)
    utils.files.clearExt()
    active.anth.update(anth_object)

# Get Anthology Object from Epub File
def upload(anth_list=None):
# Select the Epub(s) to extract
    if anth_list == None:
        anth_list = tk.filedialog.askopenfilenames(initialdir = dir.anth_epub, title = "Select Anthology Epub(s)", filetypes = (("epub files","*.epub"),("all files","*.*")))
        if anth_list == []:
            return
# For every selected Anthology file
    for anth_file in anth_list:
    # Make the Anthology Object from the Title and Contents
        anth_title = os.path.basename(anth_file).partition(' Anthology.epub')[0]
        print(anth_title)
        anth_object = utils.makeObject(anth_file, anth_title)
        # anth_object.printLinks()
        utils.files.handleImages(anth_object)
    # Store obj and update active
        utils.files.makePickle(anth_object, anth_title)
        utils.files.clearExt()
        active.anth.update(anth_object)

# Download Anthology Object as Epub File
def download():
    utils.files.makeEpub(active.anth.obj, dir.pos, anthBool=True)

# Remove Anthology Object from Storage
def remove():
    # Throw a warning popup
    if app.main.app.yesno('Removing an Anthology',  str(active.anth.obj) + ' will be removed from storage permanently! Are you sure you want to do this?'):
    # remove pickle from storage
        os.chdir(dir.anth)
        for f in os.listdir():
            if f == active.anth.obj.name + '.anth':
                os.remove(f)
    # remove the images from storage
        utils.files.removeFiles(active.anth.obj.images, dir.anth_img)
    # Reset active anthology object
        active.anth.reset()

'''Handle Changes to the Anthology Object'''
# Save changes to Anthology Object
def save():
# remove old and write the new pickle into the library folder
    utils.files.removeFiles([active.anth.obj.name + '.anth'], dir.anth)
    utils.files.makePickle(active.edit.obj, active.edit.obj.name)
# Update data objects
    active.anth.update(copy.deepcopy(active.edit.obj))
    active.edit.reset()
    lib.misc = copy.deepcopy(lib.edit)
# Update Anth Image Storage
    utils.files.moveFiles([image for image in active.anth.obj.images if image not in os.listdir(dir.anth_img)], dir.misc_img, dir.anth_img)
    name_tuples = utils.string.nameImages(active.anth.obj)
    utils.files.renameFiles(name_tuples, dir.anth_img)
    active.anth.obj.setImages(name_tuples)
    # Move Temp Images to Anth Image Storage
    utils.files.moveFiles([image for image in os.listdir(dir.temp_img) if image in active.anth.obj.images], dir.temp_img, dir.anth_img)
# Update Misc Storage
    # Remove pickles for objects no longer in the misc library
    for file in os.listdir(dir.misc):
        if file[:-5] not in [utils.string.filename(object.getSort()) for object in lib.misc]:
            os.remove(os.path.join(dir.misc, file))
    # Add pickles for objects added to the misc library
    for object in lib.misc:
        if utils.string.filename(object.getSort()) + '.work' not in os.listdir(dir.misc):
            # Add the pickle to storage
            utils.files.makePickle(object)
            # Deal with Images
            utils.files.moveFiles([image for image in object.images if image not in os.listdir(dir.misc_img)], dir.anth_img, dir.misc_img)
            name_tuples = utils.string.nameImages(object)
            utils.files.renameFiles(name_tuples, dir.misc_img)
            object.setImages(name_tuples)
# Empty Temp Image Storage?
    utils.files.emptyDir(dir.temp_img)
    
# Cancel changes to Anthology Object (delete temp images)
def cancel():
    # Reset active edit object
    active.edit.reset()
    active.index.reset()
    # Remove Temp Images
    utils.files.emptyDir(dir.temp_img)
    # Reset library?

'''Edit Anthology Work Contents'''
# Add Work(s) to Anthology Object
def addWork():
    # Make list of objects to add
    object_list = utils.other.getWorks(app.edit.listbox_misc.getValue(), lib.edit)
    # Add images to the anthology (files don't move until anthology is saved)
    active.edit.obj.images.extend([image for object in object_list for image in object.images])
# Set the Objects Fandom to match the Anthology or the current active Fandom page
    if len(active.edit.getAnth()) == 1:
        for object in object_list:
            object.setFandom(active.edit.getAnth()[0][0].getFandom())
    else:
        if active.index.page.int > 0:
            for object in object_list:
                object.setFandom(active.edit.getAnth()[active.index.page.int-1][0].getFandom())
# Add the works to the object
    active.edit.obj.addWorks(object_list)
# Remove works from misc library list
    for object in object_list:
        if object in lib.edit:
            lib.edit.remove(object)
# Remove Work(s) from Anthology Object
def removeWork():
# Make list of work objects to remove
    object_list = utils.other.getWorks(app.edit.listbox_cont.getValue(), active.edit.getContents())
    for image in [image for object in object_list for image in object.images]:
        active.edit.obj.images.remove(image)
# Remove works from Anthology object
    active.edit.obj.removeWorks(object_list)
# add objects to misc library list
    for object in object_list:
        object.fixLinks()
        if object not in lib.edit:
            lib.edit.append(object)

