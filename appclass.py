from guizero import Box, ListBox, PushButton, Text, TextBox, Combo
import dir, active, utils, anthclass

# # # Empty Classes # # #
class Master(object):
    def __init__(self, parent, align="left", width="fill", height="fill", border=0):
        self.parent = parent
        self.master = Box(self.parent, align=align, width=width, height=height)
    
    def visible(self, bool):
        self.master.visible = bool
    def hide(self):
        self.master.visible = False
    def show(self):
        self.master.visible = True

    def enable(self):
        self.master.enable()
    def disable(self):
        self.master.disable()

# # # The Simplest Elements # # #
class BoxedText(Master):
    def __init__(self, parent, size=15, text="", anchor="n", wraplength=False,
                 align="left", width="fill", height="fill", border=0):
        super().__init__(parent, align=align, width=width, height=height, border=border)
        self.text = Text(self.master, size=size, text=text, width="fill", height="fill", anchor=anchor, wraplength=wraplength)
    def clear(self):
        self.text.clear()
    def getValue(self):
        return self.text.value
    def setValue(self, new_text):
        self.text.value = new_text

class BoxedButton(Master):
    def __init__(self, parent, text, command, args=[], 
                 align="top", width="fill", height="fill", border=0):
        super().__init__(parent, align=align, width=width, height=height, border=border)
        self.button = PushButton(self.master, command=command, args=args, text=text, align="right", width="fill", height="fill")

class InputElement(Master):
    def __init__(self, parent, text, 
                 label="left", 
                 multiline=False, scrollbar=False, command=False,
                 align="left", width="fill", height=30, border=0):
        super().__init__(parent, align=align, width=width, height=height, border=border)
        self.label = Text(self.master, text=text, align=label, width=0, height="fill")
        self.textbox = TextBox(self.master, align=label, multiline=multiline, scrollbar=scrollbar, command=command, width="fill", height="fill")
        self.textbox.bg = 'white'
        self.textbox.text_size = 10
    def clear(self):
        self.textbox.clear()
    def getValue(self):
        return self.textbox.value
    def setValue(self, new_text):
        self.textbox.value = new_text
    def isEmpty(self):
        return bool(self.textbox.value == "")

class EditableValue(object):
    def __init__(self, parent, button_master, screen, active, type, size=20, cutoff=False, prefix="", suffix=""):
        self.parent = parent
        self.button_master = button_master
        self.screen = screen
        self.active = active
        self.type = type
        self.cutoff = cutoff
        # Textbox
        self.text_master = Box(self.parent, align="top", width="fill", height=0)
        self.value = ""
        self.text = Text(self.text_master, size=size, wraplength=310)
        self.prefix_text = Text(self.text_master, size=size, text=prefix, visible=False, align="left")
        self.textbox = TextBox(self.text_master, visible=False, align="left", height=0, width=0)
        self.textbox.bg = 'white'
        self.textbox.text_size = size
        self.suffix_text = Text(self.text_master, size=size, text=suffix, visible=False, align="left", width=0)
        # Button
        self.edit_button = PushButton(self.button_master, command=self.edit, align="top", width="fill", height="fill", text=f"Edit {type}")
        self.confirm_button = PushButton(self.button_master, visible=False, command=self.confirm, align="top", width="fill", height="fill", text=f"Confirm {type}")
    def edit(self):
        self.text.visible = False
        self.edit_button.visible = False
        self.screen.disable()
        self.textbox.value = self.value
        self.textbox.visible = True
        self.textbox.enable()
        self.textbox.focus()
        self.prefix_text.visible = True
        self.suffix_text.visible = True
        self.confirm_button.visible = True
        self.confirm_button.enable()
    def confirm(self):
        self.textbox.visible = False
        self.prefix_text.visible = False
        self.suffix_text.visible = False
        self.confirm_button.visible = False
        self.value = self.textbox.value
        # Update Attribute
        if self.type == "Title" and self.active.obj.name != self.textbox.value:
            self.active.obj.name = self.textbox.value
        elif self.type == "Fandom" and self.active.obj.contents[0].getFandom() != self.text.value:
            self.active.obj.setFandom(self.active.obj.contents[0].getFandom(), self.textbox.value)
        self.update(self.textbox.value, self.prefix_text.value, self.suffix_text.value)
        self.text.visible = True
        self.edit_button.visible = True
        self.screen.enable()
    def update(self, string, prefix="", suffix=""):
        self.value = string
        if self.cutoff != False:
            string = string[:self.cutoff]
        self.text.value = prefix + string + suffix
    def visible(self, bool):
        self.text_master.visible = bool
        self.edit_button.visible = bool

class FandomContents(Master):
    def __init__(self, parent, screen,
                 align="left", width=200, height="fill", border=1):
        super().__init__(parent, align=align, width=width, height=height, border=border)
        self.title_master = Box(self.master, align="top", width="fill", height=30)
        self.title_display = Box(self.title_master, align="left", width=170, height="fill")
        self.title_button = Box(self.title_master, align="right", width=30, height="fill")
        self.fandom = EditableValue(self.title_display, self.title_button, screen, active.fan, "", size=12, cutoff=20)
        self.contents = Box(self.master, align="bottom", width="fill", height="fill")
        self.listbox = ListBox(self.contents, items=['Item 1', 'Item 2'], multiselect=True, width="fill", height="fill")
        self.listbox.bg = "white"
    def update(self, fandom):
        self.fandom.update(fandom[0].getFandom())
        self.listbox.clear()
        for work in fandom:
            self.listbox.append(work)

class ScrollElement(Master):
    def __init__(self, parent, active_obj, active_index, 
                visible=False,
                 text=False,
                 align="bottom", width="fill", height="fill", border=0,
                 ):
        super().__init__(parent, align=align, width=width, height=height, border=border)
        self.gui = None
        self.text = None
        self.active_obj = active_obj
        self.active_index = active_index
        self.contents = []
        # Vertical Scroll
        if height == "fill":
            self.type = "vertical"
            self.minus_arrow = PushButton(self.master, image=dir.up_arrow_icon, command=self.index_minus, align="top", width=30, height=30, text="Up", visible=False)
            self.plus_arrow = PushButton(self.master, image=dir.down_arrow_icon, command=self.index_plus, align='bottom', width=30, height=30, text="Down")
        # Horizontal Scroll
        elif width == "fill":
            self.type = "horizontal"
            self.minus_arrow = PushButton(self.master, image=dir.left_arrow_icon, command=self.index_minus, align="left", width=30, height=30, text="Left", visible=False)
            if text:
                self.text = BoxedText(self.master)
            self.plus_arrow = PushButton(self.master, image=dir.right_arrow_icon, command=self.index_plus, align='right', width=30, height=30, text="Right")
    
    def index_minus(self):
        self.active_index.update(self.active_index.int - 1)
        if self.type == "vertical":
            self.active_obj.update(self.contents[self.active_index.int])
        self.gui.refresh(self.active_obj.obj)
    def index_plus(self):
        if self.active_obj.obj == '':
            self.active_index.update(0)
            self.active_obj.update(self.contents[0])
        else:
            self.active_index.update(self.active_index.int + 1)
            if self.type == "vertical":
                self.active_obj.update(self.contents[self.active_index.int])
        self.gui.refresh(self.active_obj.obj)
    def update(self):
        if self.type == "vertical":
            start_test = bool(self.active_index.int == 0 or self.active_obj.obj == '')
            end_test = bool(self.active_index.int == len(self.contents)-1)
        else: # Fandom and Entry have a page zero added to the front (containing summaries), which is why they don't need a len-1
            start_test = bool(self.active_index.int == 0)
            end_test = bool(self.active_index.int == len(self.contents))            
        utils.obj.arrowVisibility(self.minus_arrow, self.plus_arrow, start_test, end_test)
        if self.text != None:
            if self.active_index.int == 0:
                self.text.setValue("Multi")
            else:
                self.text.setValue(utils.string.fix(self.contents[self.active_index.int-1][0].getFandom()[:15]))
    def refill(self, items):
        self.contents = []
        for item in items:
            self.contents.append(item)

# # # GUI Function # # #
class GUIConnector(object):
    def __init__(self, reset=[], zero=[], fill=[], scroll=[], update=[], method=[]):
        self.reset = reset
        self.zero = zero
        self.fill = fill
        self.scroll = scroll
        self.update = update
        self.method = method
    def refresh(self, obj):
        if obj != "":
            for el in self.reset:
                el.reset()
            for el in self.zero:
                el.int = 0
            for el, method in self.fill:
                el.refill(method())
            for el, method in self.scroll:
                el.refill(method())
                el.update()
            for el in self.update:
                el.update(obj)
            for el in self.method:
                el()

# # # Complex Elements # # #
class MarginalElement(Master):
    def __init__(self, parent, buttons=[], 
                 align="bottom", width="fill", height=50, border=0):
        super().__init__(parent, align=align, width=width, height=height, border=border)
        self.gui = None
        for button in buttons:
            # [button variable name, button command, button arguments, button text, button visible bool]
            setattr(self, button[0], PushButton(self.master, command=button[1], args=button[2], text=button[3], visible=button[4], align="left", width="fill"))

class TextDisplay(Master):
    def __init__(self, parent, lines=[],
                 align="top", width="fill", height="fill", border=0):
        super().__init__(parent, align=align, width=width, height=height, border=border)
        self.gui = None
        for line in lines:
            # [variable name, text size, wraplength]
            setattr(self, line[0], Text(self.master, text="Placeholder", size=line[1], wraplength=line[2], align="top", width="fill", height=0))
    
    def update(self, obj):
        if hasattr(self, 'title'):
            self.title.value = str(obj)
        if hasattr(self, 'work_title'):
            self.work_title.value = utils.string.fix(obj.title)
        if hasattr(self, "entry_title") and active.index.entry.int != 0:
            if self.entry_title.visible == True:
                self.entry_title.value = utils.string.fix(obj.contents[active.index.entry.int-1].getTitle())
        if hasattr(self, 'author'):
            self.author.value = utils.string.fix(obj.author)
        if hasattr(self, 'fandom'):
            self.fandom.value = obj.getFandomString()
        if hasattr(self, 'words'):
            self.words.value = obj.getWordsString()
        if hasattr(self, 'works'):
            self.works.value = obj.getWorksString()
        if hasattr(self, 'summary'):
            self.summary.value = obj.getSummary()

class SortList(Master):
    def __init__(self, parent, selected, options=[], lib=None,
                 align="top", width="fill", height=30, border=0):
        super().__init__(parent, align=align, width=width, height=height, border=border)
        self.combo = Combo(self.master, command=self.update, options=options, selected=selected, align="left", width="fill", height="fill")
        self.arrow = PushButton(self.master, command=self.toggle, image=dir.down_arrow_icon, align="right", width=30, height=30)
        self.reverse = False
        self.lib = lib
        self.temp = None
        self.list = None
    def getValue(self):
        return self.combo.value
    def toggle(self):
        self.reverse = not self.reverse
        if self.reverse == False:
            self.arrow.image = dir.down_arrow_icon
        else:
            self.arrow.image = dir.up_arrow_icon
        self.arrow.width = 30
        self.arrow.height = 30
        self.update()
    def update(self):
        self.temp = self.lib
        if self.list != None:
            if self.getValue() == "Series":
                self.temp = [work for work in self.temp if work.getType() == "Series"]
            elif self.getValue() == "Singletons":
                self.temp = [work for work in self.temp if work.getType() != "Series"]
            for value, key in [("Alphabetical", lambda x:x.getSort()), 
                               ("Author", lambda x:x.getAuthor().lower()),
                               ("Fandom", lambda x:x.getFandom()),
                               ("Word Count", lambda x:x.getWordcount()),
                               ("Series", lambda x:x.getSort()),
                               ("Singletons", lambda x:x.getSort())
                               ]:
                if self.getValue() == value:
                    self.temp.sort(key=key, reverse=self.reverse)
            self.list.refill(self.temp)
            
# Basic Listbox
class ListElement(object):
    def __init__(self, parent, 
                 active_obj, 
                 active_index=None, 
                 items=[], 
                 align="left", width="fill", height="fill", multiselect=False):
        self.parent = parent
        self.active_obj = active_obj
        self.active_index = active_index
        self.items = items
        self.gui = None
        self.multiselect = multiselect
        self.listbox = ListBox(self.parent, command=self.select, items=items, align=align, width=width, height=height, multiselect=multiselect)
        self.listbox.bg = "white"
        self.listbox.text_size = 10

    def clear(self):
        self.listbox.clear()
        self.items = []
    def getValue(self):
        return self.listbox.value
    def setValue(self, new_value):
        self.listbox.value = new_value
    def append(self, item):
        self.listbox.append(item)
        self.items.append(item)
    def refill(self, items):
        self.clear()
        for item in items:
            self.append(item)
    def select(self):
        # If there's a value selected
        if self.listbox.value != None:
            if self.active_obj != None:
                check_value = self.listbox.value if self.multiselect == False else self.listbox.value[0]
                # For each object in the relevant library
                for obj in self.items:
                    if check_value == str(obj):
                        self.active_obj.update(obj)
                        if self.active_index != None:
                            self.active_index.update(self.items.index(obj))
                        self.gui.refresh(obj)
            else:
                self.gui.refresh(None)


class SummaryBox(Master):
    def __init__(self, parent, 
                 align="right", width="fill", height="fill", border=0):
        super().__init__(parent, align=align, width=width, height=height, border=border)
        self.gui = None
        self.box = Box(self.master, border=1, align='top', width='fill', height="fill")
        self.listbox = ListBox(self.box, command=self.select, width="fill", height="fill", items=[])
        self.listbox.bg = "white"
        self.listbox.text_size = 10
        self.summary = Text(self.box, anchor='nw', justify='left', wraplength=250, align='top', size=12, width='fill', height=0)
    def select(self):
        new_str = self.listbox.value
        # Find new string in contents
        if new_str != None and new_str != str(active.work.obj):
            # Grab object from Series contents
            for obj in active.work.obj.getContents():
                if new_str == str(obj):
                    active.index.entry.update(active.work.obj.getContents().index(obj) + 1)
                    self.gui.refresh(active.work.obj)
    def update(self, obj):
        self.listbox.clear()
        self.listbox.append(obj)
        for i in obj.getContents():
            self.listbox.append(i)
        if isinstance(obj, anthclass.Singleton):
            self.summary.value = obj.getGuideSummary()
        elif isinstance(obj, anthclass.Series):
            self.summary.value = obj.contents[active.index.entry.int-1].getGuideSummary()
