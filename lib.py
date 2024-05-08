import dir

import copy
import os
import pickle

anth = []
book = []
misc = []
edit = []
fan = []
cont = []

# Loads the anthology library from the anthology storage folder
def load_anthology_library():
    global anth
    anth = []
    # Go to where the pickles are kept
    os.chdir(dir.anth)
    for i in os.listdir(dir.anth):
        # Don't select Folders
        if os.path.isdir(dir.anth + '//' + i) == False:
            # Pickles created when antholifi module existed
            anth.append(pickle.load(open(i,'rb')))
    anth = sorted(anth, key = lambda x:x.name)

# Loads the book library from the book storage folder
def load_book_library():
    global book
    book = []
    # Go to where the pickles are kept
    os.chdir(dir.book)
    for i in os.listdir(dir.book):
        # Don't select Folders
        if os.path.isdir(dir.book + '//' + i) == False:
            book.append(pickle.load(open(i,'rb')))

# Loads the misc library from the misc storage folder
def load_misc_library():
    global misc
    misc = []
    # Go to where the pickles are kept
    os.chdir(dir.misc)
    for i in os.listdir(dir.misc):
        # Don't select Folders
        if os.path.isdir(dir.misc + '//' + i) == False:
            misc.append(pickle.load(open(i,'rb')))
    misc = sorted(misc, key = lambda x:x.getSort())

def load_edit_misc_library():
    global misc
    global edit
    edit = copy.deepcopy(misc)

def load_fan_misc_library():
    global edit
    global fan
    fan = copy.deepcopy(edit)

def load_cont_misc_library():
    global misc
    global cont
    cont = copy.deepcopy(misc)

load_anthology_library()
load_book_library()
load_misc_library()
load_edit_misc_library()
load_fan_misc_library()
