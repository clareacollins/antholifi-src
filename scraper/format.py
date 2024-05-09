import re

from scraper import taglib
from scraper import filter

def text(string):
    string = re.sub('</p><p>', '\n', string)
    string = re.sub('<br>', '\n', string)
    string = re.sub('\t', '', string)
    string = re.sub('"', "'", string)
    string = re.sub('”|“', "'", string)
    string = re.sub('’', "'", string)
    string = re.sub('@', 'at', string)
    string = re.sub('<[^>]*?>', '', string)
    string = re.sub('&nbsp;', '', string)
    string = re.sub(' \s+', ' ', string)
    string = re.sub('\s+\n\s+', '\n', string)
    string = re.sub('\n\n+', '\n', string)
    string = string.strip()
    #print(string)
    return string

def tags_list(list, type=None):
    new_list = []
    for string in list:
        string = re.sub('&#39;', "'", string)
        string = re.sub('&quot;', "'", string)
        string = re.sub('&amp;', '&', string)
        string = re.sub('@', 'at', string)
        string = re.sub(' \s+', ' ', string)
        string = re.sub('\s+/', '/', string)
        string = re.sub('/\s+', '/', string)
        string = re.sub('\(s\)', 's', string)
        for tuple in taglib.double_names:
            string = re.sub(tuple[0], tuple[1], string)
        for tuple in taglib.tag_abbr:
            string = re.sub(tuple[0], tuple[1], string)
        string = string.strip()
        if type == 'relationship':
            tag_tuple = filter.relationship(string)
            if tag_tuple[0]:
                new_list.append(tag_tuple[1])
        elif type == 'character':
            tag_tuple = filter.character(string)
            if tag_tuple[0]:
                new_list.append(tag_tuple[1])
        elif type == 'freeform':
            tag_tuple = filter.freeform(string)
            if tag_tuple[0]:
                new_list.append(tag_tuple[1])
        else:
            new_list.append(string)
    return new_list

def tags(string):
    string = re.sub('</li><li>', ', ', string)
    string = re.sub('<[^>]+>', '', string)
    string = re.sub(' \([^\)]+\)', '', string)
    string = re.sub('&#39;', "'", string)
    string = re.sub('&amp;', '&', string)
    string = re.sub('@', ' ', string)
    # Remove double names
    for tuple in taglib.double_names:
        string = re.sub(tuple[0], tuple[1], string)
    return string

def words(string):
    return re.sub(',', '', string)
    # if ',' not in string:
    #     if int(string) >= 1000:
    #         return str(string)[:-3] + "," + str(string)[-3:]
    # else:
    #     return string

def tuples(tuple_list):
    if tuple_list == []:
        return ''
    else:
        series = []
        for tuple in tuple_list:
            series.append(tuple[1] + ' [' + tuple[0] + ']')
        string = '-) ' + ', '.join(series)
        string = re.sub('&amp;', '&', string)
        return string