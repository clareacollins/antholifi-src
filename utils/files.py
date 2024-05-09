import dir

import os
import pickle
import shutil
import zipfile

from utils import classobj, string, other

'''The Utils Package Files Module
This module contains all the functions that perform file and directory operations.
'''

### Passed File Names/Directories as Strings
### Performs File/Directories Operations

### Returns Nothing
def writeFile(text, fileName='csv', ext="txt"):
    os.chdir(dir.downloads)
    file = open(f'{fileName}.{ext}', 'w', errors="ignore")
    file.write(text)
    file.close()

# Makes Directory if it doesn't exist
def makeDir(location):
    if not os.path.exists(location):
        os.mkdir(location)
# Deletes a File if it exists
def makeWay(location, file):
    if os.path.exists(os.path.join(location, file)):
        os.remove(os.path.join(location, file))
# Returns full File Paths for listdir
def getFilePaths(location):
    file_path_list = []
    for file in os.listdir(location):
        if not os.path.isdir(os.path.join(location, file)):
            file_path_list.append(os.path.join(location, file))
    return file_path_list

def getFolderPaths(location):
    folder_path_list = []
    for file in os.listdir(location):
        if os.path.isdir(os.path.join(location, file)):
            folder_path_list.append(os.path.join(location, file))
    return folder_path_list

### ### Specific File Operations ### ###
# Renames a Specific File at a Location
def renameFile(old_name, new_name, location):
    if old_name != new_name:
        makeWay(location, new_name)
        os.rename(os.path.join(location, old_name), os.path.join(location, new_name))
# Renames a List of Specific Files at a Location
def renameFiles(name_tuples, location):
    for tuple in name_tuples:
        old_name, new_name = tuple[0], tuple[1]
        renameFile(old_name, new_name, location)

# Copies a Specific File to a Destination (Can Rename)
def copyFile(file_path, destination, newName=None):
    makeDir(destination)
    # If applicable, rename the file
    file_name = os.path.basename(file_path)
    if newName != None:
        file_name = newName
    # Copy the file
    makeWay(destination, file_name)
    shutil.copy(file_path, os.path.join(destination, file_name))
# Copies a List of Specific Files to a Destination (Doesn't Rename)
def copyFiles(file_list, location, destination):
    for file in file_list:
        copyFile(os.path.join(location, file), destination)

# Moves a File to a Destination (Can Rename)
def moveFile(file_path, destination, newName=None):
    if os.path.exists(file_path):
        makeDir(destination)
        # If applicable, rename the file
        file_name = os.path.basename(file_path)
        if newName != None:
            file_name = newName
        # Move the file
        makeWay(destination, file_name)
        try:
            shutil.move(file_path, os.path.join(destination, file_name))
        except PermissionError:
            pass
    else:
        print('File not found for Move: ' + file_path)
# Moves a List of Specific Files to a Destination (Doesn't Rename)
def moveFiles(file_list, location, destination):
    for file in file_list:
        moveFile(os.path.join(location, file), destination)

# Removes a File, or throws an error if it doesn't exist
def removeFile(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        print('File not found for Deletion: ' + file_path)
# Removes specific files from a location
def removeFiles(file_list, location):
    for file in file_list:
        removeFile(os.path.join(location, file))




# Renames images in temp and moves them to the appropriate directory
def handleImages(object):
    # Generate Image Name Tuples
    name_tuples = string.nameImages(object)
    # print(name_tuples)
    renameFiles(name_tuples, dir.temp_img)
    object.setImages(name_tuples)
    destination = dir.misc_img
    if object.getType() == 'Anthology':
        destination = dir.anth_img
        # Make Cover
        cover_img = str(object.images[0])
        if not os.path.exists(os.path.join(dir.temp_img, cover_img)):
            if os.path.exists(os.path.join(dir.cover, cover_img)):
                copyFile(os.path.join(dir.cover, cover_img), dir.temp_img)
            else:
                copyFile(os.path.join(dir.img_root, 'placeholder.jpg'), dir.temp_img, cover_img)
    moveFiles(object.images, dir.temp_img, destination)


### ### Directory File Operations ### ###
# Removes all Files a folder and a subfolder
def emptyDir(location, subfolder=None):
    try:
        os.chdir(location)
        if subfolder != None:
            if os.path.exists(os.path.join(location, subfolder)):
                shutil.rmtree(subfolder)
        for file in os.listdir():
            os.remove(file)
    except PermissionError:
        pass

def clearExt():
    emptyDir(dir.pos, 'Ext')


### Returns List of Strings
# Opens, reads, and returns the text of a file
def readText(file, location=dir.ext):                
    readable_file = open(os.path.join(location, file), 'r', encoding="utf-8", errors = 'ignore')
    text = readable_file.read()
    # text = string.fixHtmlErrors(text)
    readable_file.close()
    return text
# Given the file location of an epub, extracts epub to ext, moves images to temp, and returns a list of the zip's contents.
def extractEpub(location, epub=None):
    # If no epub is passed, location includes file name and they need to be separated
    if epub == None:
        epub = os.path.basename(location)
        location = os.path.dirname(location)
    # Empty the ext folder
    clearExt()
    # Copy epub to the recieving Location, turn into zip
    zip = epub[:-5] + '.zip'
    copyFile(os.path.join(location, epub), dir.pos, zip)
    # open the zip, extract
    zip_file = zipfile.ZipFile(os.path.join(dir.pos, zip), 'r')
    zip_file.extractall(dir.ext)
    # Grab contents, close file, turn back into epub
    zip_contents_list = zip_file.namelist()
    zip_file.close()
    renameFile(zip, epub, dir.pos)
    contents = other.noFormatting(zip_contents_list)
    # Move images from Ext to Temp
    moveFiles(other.onlyImages(contents), dir.ext, dir.temp_img)
    return contents



### Passed Object or List of Objects
### Performs File/Directories Operations
### Returns Nothing
# Passed an Object, makes a pickle file of it
def makePickle(object, anth_title = None):
    if object.getType() == 'Anthology':
        os.chdir(dir.anth)
        pickle.dump(object, open(anth_title + '.anth', "wb+"))
    else:
        os.chdir(dir.misc)
        pickle.dump(object, open(string.filename(object.getSort()) + '.work', "wb+"))
# Passed a list of Objects, removes their pickles
def removePickles(object_list, location):
    for pickle_file in os.listdir(location):
        for work in object_list:
            if pickle_file[:-5] == work.getSort():
                os.remove(os.path.join(location, pickle_file))
# Write Works Files
def writeSingleton(object, new_epub, suffix=''):
    for file in object.getContents():
        new_epub.writestr(suffix + file.getName(), file.getText())
# Write Series Files
def writeSeries(object, new_epub, suffix=''):
    for entry in object.contents:
        for file in entry.getContents():
            new_epub.writestr(suffix + str(entry.getNumber()) + '/' + file.getName(), file.getText())    
# Passed Object and Destination, makes Epub file at Destination
def makeEpub(object, destination, anthBool=False):
    os.chdir(destination)
# Start making up the epub
    file_name = str(object)
    if not anthBool:
        file_name = string.getStorageName(object)
    new_epub = zipfile.ZipFile(file_name + '.zip', 'w')
    # Write all the generic contents
    new_epub.writestr('mimetype', classobj.GenericContents.mimetype)
    new_epub.writestr('META-INF/container.xml', classobj.GenericContents.meta)
    new_epub.writestr('stylesheet_Gen.css', classobj.GenericContents.gen)
    cover_manifest, opfFinal = '', ''
    guide_text, description_text, manifest_text, spine_text, toc_ncx_text = '', '', '', '', ''
# Anthology
    if anthBool:
    # Generate Strings for Formatting Files
        cover_manifest = '<item href="stylesheet_Cover.css" id="style_Cover" media-type="text/css"/>\n\t\t'
        opfTitle = file_name
        opfAuthor = 'various'
        opfFinal = '\n\t\t<reference href="cover.xhtml" type="cover"/>\n\t'
        tocDescription = opfTitle + ' by ' + opfAuthor
        unique_id = object.getAbbr()
    # Complex Strings for Formatting Files
        manifest_text = '\n\t\t'.join(['', '<item href="cover.xhtml" id="cover" media-type="application/xhtml+xml"/>', '<item href="guide.html" id="guide" media-type="application/xhtml+xml"/>'])
        spine_text = '\n\t\t'.join(['', '<itemref idref="cover"/>', '<itemref idref="guide"/>'])
        toc_ncx_text = '\n\t\t'.join(['<navPoint id="num_0" playOrder="0">', '\t<navLabel>', '\t\t<text>Guide</text>', '\t</navLabel>', '\t<content src="guide.html"/>', '</navPoint>'])
        for fandom_group in object.anth:
            # Open fandom group
            if len(object.anth) > 1:
                guide_text += '\n\t<p>' + fandom_group[0].getFandom() + '</p>\n\t<hr/>'
                description_text += '\n<hr>' + fandom_group[0].getFandom() + '</hr>\n'
            # Grab Formatting Strings
            group_index = object.anth.index(fandom_group)+1
            for work in fandom_group:
                work_index = fandom_group.index(work)+1
                # Add to content.opf
                description_text += string.makeDescription(work)
                manifest_text += string.makeManifest(work, work_index, group_index)
                spine_text += string.makeSpine(work, work_index, group_index)
                # Add to guide.html
                guide_text += string.makeGuide(work, work_index, group_index, object.getAbbr())
                # Add to toc.ncx
                toc_ncx_text += string.makeTOCNCX(work, work_index, group_index)
            # Write Works to Epub
                if work.getType() == 'Singleton':
                    writeSingleton(work, new_epub, str(group_index) + '/' + str(work_index) + '/')
                elif work.getType() == 'Series':
                    writeSeries(work, new_epub, str(group_index) + '/' + str(work_index) + '/')
            # Close fandom group
            if len(object.anth) > 1:
                guide_text = guide_text + '\n\t<hr/>'   
    # Write Exclusive Anthology Formatting Files
        new_epub.writestr('stylesheet_Cover.css', classobj.GenericContents.cover)
        new_epub.writestr('guide.html', classobj.Guide.assemble(file_name, guide_text))
        new_epub.writestr('cover.xhtml', classobj.Cover.assemble(file_name, object.images[0]))
        # Images
        os.chdir(dir.anth_img)
        for i in object.images:
            try:
                new_epub.write(i, 'Images/' + i)
            except:
                print('Error writing ' + i + ' to anthology')
                FileNotFoundError
# Singleton or Series
    else:
        #
        opfTitle = object.getTitle()
        opfAuthor = object.getAuthor()
        tocDescription = opfTitle + ' by ' + opfAuthor
        unique_id = 'A225'
        #
        manifest_text = string.makeManifest(object, None, None)
        spine_text = string.makeSpine(object, None, None)
        toc_ncx_text = string.makeTOCNCX(object, None, None)
        if object.getType() == 'Singleton':
            writeSingleton(object, new_epub)
        elif object.getType() == 'Series':
            writeSeries(object, new_epub)
        # Images
        os.chdir(dir.misc_img)
        for i in object.images:
            print(i)
            if i in os.listdir(dir.misc_img):
                new_epub.write(os.path.join(dir.misc_img, i), 'Images/' + i)
            elif i in os.listdir(dir.temp_img):
                new_epub.write(os.path.join(dir.temp_img, i), 'Images/' + i)
            else:
                print(f'Error writing {i} to {file_name}, {i} not in dir.misc_img or dir.temp_img')
# Content.opf
    # images for the manifest
    image_man = ''
    for i in object.images:
        image_man += '\n\t\t<item href="Images/' + str(i) + '" id="image' + str(object.images.index(i) + 1) + '" media-type="image/' + string.getImageType(i) + '"/>'
    manifest_text += '\n\t\t' + \
        '<item href="toc.ncx" id="ncx" media-type="application/x-dtbncx+xml"/>\n\t\t' + \
        cover_manifest + \
        '<item href="stylesheet_Gen.css" id="style_Gen" media-type="text/css"/>\n\t\t' + \
        image_man
    # Write the content.opf and toc.ncx
    new_epub.writestr('content.opf', classobj.OPF.assemble(unique_id, opfTitle, opfAuthor, description_text, manifest_text, spine_text, opfFinal))
    new_epub.writestr('toc.ncx', classobj.TOCncx.assemble(unique_id, tocDescription, toc_ncx_text))
# Files
    # Move the pictures?
    # makeDir(os.path.join(destination, 'Temp'))    
    # Close the zip file
    # os.chdir(destination)
    new_epub.close()
    # Remove potential duplicates in destination
    if os.path.isfile(os.path.join(destination, file_name + '.epub')):
        os.remove(os.path.join(destination, file_name + '.epub'))
    renameFile(file_name + '.zip', file_name + '.epub', destination)
    # os.chdir(destination)
    # shutil.rmtree('Temp')
