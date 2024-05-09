import re

nt = '\n\t'
ntt = '\n\t\t'

# Master Class for all HTML files
class HTML_File(object):
    def __init__(self):
        nt = '\n\t'
        ntt = '\n\t\t'
        self.Open = "<?xml version='1.0' encoding='utf-8'?>" + nt + '<html xmlns="http://www.w3.org/1999/xhtml">' + nt
        self.headOpen = '<head>' + ntt
        self.titleOpen = '<title>'
        self.titleClose = '</title>' + ntt
        self.headClose = '</head>' + nt
        self.h1Open = '<h1>'
        self.h1Close = '</h1>' + nt
        self.bodyOpen = '<body>' + nt + '<div>' + nt
        self.bodyClose = nt + '</div>' + nt + '</body>' + nt
        self.Close = '</html>'
        self.Create()
    def Create(self):
        return 

class TOCncx_html(HTML_File):
    def Create(self):
        self.Open = "<?xml version='1.0' encoding='utf-8'?>\n" + '<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1" xml:lang="en">\n\t'
        self.metaOpen = '<meta content="'
        self.metaClose = '" name="dtb:uid"/>\n\t\t'
        self.docTitleOpen = '<docTitle>\n\t\t<text>'
        self.docTitleClose = '</text>\n\t</docTitle>\n\t'
        self.navMapOpen = '<navMap>\n\t\t'
        self.navMapClose = '\n\t</navMap>\n'
        self.Close = '</ncx>'
    def assemble(self, unique_id, title, TOC_ncx_body):
        return self.Open + self.headOpen + \
            self.metaOpen + unique_id + self.metaClose + \
            self.headClose + \
            self.docTitleOpen + title + self.docTitleClose + \
            self.navMapOpen + TOC_ncx_body + self.navMapClose + self.Close

class OPF_html(HTML_File):
    def Create(self):
        self.Open = "<?xml version='1.0' encoding='utf-8'?>\n"
        self.packageUIDOpen = '<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="'
        self.packageUIDClose = '" version="2.0">\n\t'
        self.metadataOpen = '<metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">\n\t'
        self.dcTitleOpen = '<dc:title>'
        self.dcTitleClose = '</dc:title>\n\t'
        self.dcCreatorOpen = '<dc:creator opf:role="aut" opf:file-as="'
        self.dcCreatorClose = '</dc:creator>\n\t'
        self.dcDescriptionOpen = '<dc:description>'
        self.dcDescriptionClose = '</dc:description>\n\t'
        self.dcIdentifierOpen = '<dc:identifier id="'
        self.dcIdentifierClose = '</dc:identifier>\n\t'
        self.metadataClose = '</metadata>\n\t'
        self.manifestOpen = '<manifest>'
        self.manifestClose = '\n\t</manifest>\n\t'
        self.spineOpen = '<spine toc="ncx">'
        self.spineClose = '\n\t</spine>\n\t'
        self.guideOpen = '<guide>'
        self.guideClose = '</guide>\n\t'
        self.Close = '</package>'
    def assemble(self, unique_id, title, author, description, manifest, spine, guide):
        return self.Open + \
        self.packageUIDOpen + unique_id + self.packageUIDClose + \
        self.metadataOpen + \
        self.dcTitleOpen + title + self.dcTitleClose + \
        self.dcCreatorOpen + author + '">' +  author + self.dcCreatorClose + \
        self.dcDescriptionOpen + description + self.dcDescriptionClose + \
        self.dcIdentifierOpen + unique_id + '" opf:scheme="uuid">' + unique_id + self.dcIdentifierClose + \
        self.metadataClose + \
        self.manifestOpen + manifest + self.manifestClose + \
        self.spineOpen + spine + self.spineClose + \
        self.guideOpen + guide + self.guideClose + self.Close

class Cover_html(HTML_File):
    def Create(self):
        self.Open = '<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">\n\t'
        self.styleTags = '<link href="stylesheet_Cover.css" type="text/css" charset="UTF-8" rel="stylesheet"/>\n\t'
        self.linkOpen = '<img src="Images/'
        self.linkClose = '" alt="cover"/>'
    def assemble(self, title, link, prefix=''):
        return self.Open + self.headOpen + \
            self.titleOpen + title + self.titleClose + \
            self.styleTags + self.headClose + \
            self.bodyOpen + \
            self.linkOpen + link + self.linkClose + \
            self.bodyClose + self.Close

class Guide_html(HTML_File):
    def Create(self):
        self.styleTags = '<link href="stylesheet_Gen.css" type="text/css" charset="UTF-8" rel="stylesheet"/>\n\t'
        self.bodyOpen = '<body>\n\t'
        self.bodyClose = '\n</body>\n\t'
    def assemble(self, title, Guide_body, prefix=''):
        return self.Open + self.headOpen + \
            self.titleOpen + title + ' Guide\n\t' + self.titleClose + \
            self.styleTags + self.headClose + \
            self.h1Open + title + ' Guide\n\t' +  self.h1Close + \
            self.bodyOpen + Guide_body + self.bodyClose + self.Close

class Generic(object):
    def __init__(self):
        self.filenames = ['mimetype', 'META-INF/container.xml', 'stylesheet_Gen.css', 'stylesheet_Cover.css']
        self.mimetype = 'application/epub+zip'
        self.meta = '<?xml version="1.0" encoding="utf-8"?>\n<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">\n\t<rootfiles>\n\t\t<rootfile full-path="content.opf" media-type="application/oebps-package+xml"/>\n\t</rootfiles>\n</container>'
        self.gen = 'p.message {\n\t  text-align: center;\n\t}\n\th1 {\n\tfont-size: 1.5em;\n\ttext-align: center;\n\t}\n\th2 {\n\tfont-size: 1.25em;\n\ttext-align: center;\n\tpage-break-before: always;\n\t}\n\t.meta .byline {\n\ttext-align: center;\n\t}\n\t.meta dl.tags {\n\tborder: 1px solid;\n\tpadding: 1em;\n\t}\n\t.meta dd {\n\tmargin: -1em 0 0 10em;\n\t}\n\t.meta .endnote-link {\n\tfont-size: 0.8em;\n\t}\n\t#chapters {\n\tfont-family: "Nimbus Roman No9 L", "Times New Roman", serif;\n\tpadding: 1em;\n\t}\n\t.userstuff {\n\tfont-family: "Nimbus Roman No9 L", "Times New Roman", serif;\n\tpadding: 1em;\n\t}\n\t.bold {\n\tfont-weight: bold;\n\t}\n\t.calibre {\n\tdisplay: block;\n\tfont-size: 1em;\n\tline-height: 1.2;\n\tpadding-left: 0;\n\tpadding-right: 0;\n\ttext-align: justify;\n\tmargin: 0 5pt;\n\t}\n\t.calibre_ {\n\tdisplay: block;\n\ttext-align: center;\n\ttext-indent: 0;\n\tmargin: 1em 0 0;\n\t}\n\t.calibre_1 {\n\tdisplay: block;\n\ttext-align: justify;\n\ttext-indent: 0;\n\tmargin: 1em 0 0;\n\t}\n\t.calibre_2 {\n\tdisplay: block;\n\ttext-align: justify;\n\ttext-indent: 0;\n\tmargin: 1em 0 0 2em;\n\t}\n\t.calibre_3 {\n\tdisplay: block;\n\ttext-indent: -19pt;\n\tmargin: 1em 0 0 19pt;\n\t}\n\t.calibre_4 {\n\tdisplay: block;\n\ttext-indent: -19pt;\n\tmargin: 0 0 0 19pt;\n\t}\n\t.calibre_5 {\n\tdisplay: block;\n\ttext-indent: 0;\n\tmargin: 0 0 0 2em;\n\t}\n\t.calibre1 {\n\tfont-size: 1.125em;\n\tline-height: 1.2;\n\t}\n\t.calibre3 {\n\tfont-size: 1.5em;\n\tline-height: 1.2;\n\t}\n\t.italic {\n\tfont-style: italic;\n\t}\n\t.mbp_pagebreak {\n\tdisplay: block;\n\tmargin: 0;\n}'
        self.cover = '@page {\n\tpadding: 0;\n\tmargin: 0;\n\t}\n\tbody {\n\ttext-align: center;\n\tpadding: 0;\n\tmargin: 0;\n\t}\n\tdiv {\n\tmargin: 0;\n\tpadding: 0;\n\t}'

class Preface_Obj(object):
    def __init__(self):
        self.Open = "<?xml version='1.0' encoding='utf-8'?>\n\t" + '<html xmlns="http://www.w3.org/1999/xhtml">\n\t'
        self.headOpen = '<head>\n\t'
        self.updateOpen = "<!--UPDATE: '"
        self.updateClose = "SPECIAL: 'NONE'-->\n\t"
        self.titleTagsOpen = '<title>'
        self.titleTagsClose = '</title>\n\t'
        self.style = '<link href="../stylesheet_Gen.css" type="text/css" charset="UTF-8" rel="stylesheet"/>\n\t'
        self.headClose = '</head>\n\t'
        self.tagsOpen = '<body>\n\t<div class="meta">\n\t<dl class="tags">\n\t'
        self.tagsClose = '</dd>\n\t</dl>\n\t'
        self.titleOpen = '<h1>'
        self.titleClose = '</h1>\n\t'
        self.authorOpen = '<div class="byline">by '
        self.authorClose = '</div>\n\t'
        self.summaryOpen = '<p>Summary</p>\n\t<blockquote class="userstuff">\n\t<p>'
        self.summaryClose = '</p></blockquote>\n\t'
        self.Close = '</div>\n\t</body>\n\t</html>'
    def assemble(self, update_value, link, title, author, fandom, series, series_num, tags, summary):
        series_text = ''
        if series != '':
            series_text = '\t' + series + '\n\t\t' + str(series_num) + '\n\t'
        return self.Open + self.headOpen + \
        self.updateOpen + str(update_value) + "'\n\t\tLINK: '" + link + "'\n\t\t" + self.updateClose + \
        self.titleTagsOpen + title + '\n\t\t' + author + '\n\t\t' + fandom + '\n\t' + series_text + self.titleTagsClose + \
        self.style + self.headClose + \
        self.tagsOpen + tags + '\n\t' + self.tagsClose + \
        self.titleOpen + title + '\n\t' + self.titleClose + \
        self.authorOpen + author + '\n\t' + self.authorClose + \
        self.summaryOpen + summary + self.summaryClose + \
        self.Close

class Chapter_Obj(object):
    def __init__(self):
        self.Open = "<?xml version='1.0' encoding='utf-8'?>" + '\n<html xmlns="http://www.w3.org/1999/xhtml">\n\t'
        self.head = '<head>\n\t\t<title></title>\n\t\t<link href="../stylesheet_Gen.css" type="text/css" charset="UTF-8" rel="stylesheet"/>\n\t</head>\n\t'
        self.bodyOpen = '<body>\n\t<div class="meta group">\n\t'
        self.headerOpen = '<h2>'
        self.headerClose = '</h2>\n\t'
        self.chapterOpen = '</div>\n\t<!--chapter content-->\n\t<div class="userstuff">\n\t'
        self.chapterClose = '</div>\n\t<!--/chapter content-->\n\t'
        self.bodyClose = '</body>\n\t'
        self.Close = '</html>'
    def assemble(self, header, text, notes):
        return self.Open + self.head + self.bodyOpen + \
        self.headerOpen + header + '\n\t' + self.headerClose + \
        self.chapterOpen + text + '\n\t' + self.chapterClose + notes + \
        self.bodyClose + self.Close

TOCncx = TOCncx_html()
OPF = OPF_html()
Cover = Cover_html()
Guide = Guide_html()
GenericContents = Generic()
Preface = Preface_Obj()
Chapter = Chapter_Obj()
