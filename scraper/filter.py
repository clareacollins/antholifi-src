import re

from scraper import taglib


def relationship(tag):
    ValidTagBool = False
    if '&' in tag or '/' in tag:
        ValidTagBool = True
    for string in taglib.relationship_forbidden:
        if string.lower() in tag.lower():
            ValidTagBool = False
    tag = re.sub(' - Relationship', '', tag)
    tag = re.sub(' Friendship', '', tag)
    return [ValidTagBool, tag]

def character(tag):
    ValidTagBool = True
    for string in taglib.character_forbidden:
        if string.lower() in tag.lower():
            ValidTagBool = False
    tag = re.sub(' - Character', '', tag)
    return [ValidTagBool, tag]

def freeform(tag):
    ValidTagBool = True
    for string in taglib.freeform_forbidden:
        if string.lower() in tag.lower():
            ValidTagBool = False
    tag = re.sub(' - Freeform', '', tag)
    return [ValidTagBool, tag]
