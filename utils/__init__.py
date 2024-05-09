from utils import classobj
from utils import string
from utils import files
from utils import obj
from utils import other

import os
'''
Isolated:
    - anthclass
    - dir
'''

def createAnthology(directory, fandom=None, anth_title=None):
    if fandom == None and anth_title == None:
        fandom, anth_title = string.getAnthTitle(os.path.basename(directory))
    object_list = []
    folderPaths = files.getFolderPaths(directory)
    if folderPaths != []:
        for file in files.getFilePaths(directory):
            work_object = makeObject(file)
            object_list.append(work_object)
        for folder in folderPaths:
            sub_fandom = os.path.basename(folder)
            for file in files.getFilePaths(folder):
                work_object = makeObject(file)
                work_object.setFandom(sub_fandom)
                object_list.append(work_object)
    else:
        for file in files.getFilePaths(directory):
            work_object = makeObject(file)
            if fandom != None:
                work_object.setFandom(fandom)
            object_list.append(work_object)
    object = obj.createAnthologyObject(object_list, anth_title)
    # Images, which are in temp with unique names, are sent to their final destination
    files.handleImages(object)
    return object                


# # Function is passed a directory, returns object made from the files in the directory
# def createObject(directory, type, fandom=None):
#     # Get All Files in Directory
#     # For every file in the directory
#     object_list = []
#     for file in files.getFilePaths(directory):
#         work_object = makeObject(file)
#         if fandom != None:
#             work_object.setFandom(fandom)
#         object_list.append(work_object)
#     # Extract the contents of the epub file
#     if type == 'Series':
#         object = obj.createSeriesObject(object_list)
#     # Images, which are in temp with unique names, are sent to their final destination
#     files.handleImages(object)
#     return object

# Passed an Epub File Path, Returns a Work Object
def makeObject(file_path, title=None):
    # Extract the contents of the epub file
    contents = files.extractEpub(file_path)
    work_contents = other.onlyWorks(contents)
    type = other.getType(work_contents)
# Work
    if type == 'Work':
        object = obj.makeWorkObject(work_contents)
# Series
    if type == 'Series':
        object = obj.makeSeriesObject(work_contents)
# Anthology
    if type == 'Anthology':
        object = obj.makeAnthologyObject(work_contents, title)
    files.clearExt()
    return object