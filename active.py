import anthclass

class ActiveInt(object):
    def __init__(self):
        self.int = 0
    def __str__(self):
        return str(self.int)
    def update(self, new_int):
        if new_int != self.int:
            self.int = new_int

class ActiveIndex(object):
    def __init__(self):
        self.page = ActiveInt()
        self.work = ActiveInt()
        self.entry = ActiveInt()
        self.summary = ActiveInt()
    
    def reset(self):
        self.page.int = 0
        self.work.int = 0
        self.entry.int = 0
        self.summary.int = 0

class ActiveObject(object):
    def __init__(self):
        self.obj = ''
    
    def __str__(self):
        return str(self.obj)
    
    def reset(self):
        self.obj = ''

    def update(self, new_obj):
        if new_obj != self.obj:
            self.obj = new_obj

    def getContents(self):
        if self.obj == '':
            return []
        if isinstance(self.obj, anthclass.Anthology):
            if len(self.obj.anth) == 1:
                return self.obj.contents
            else:
                if index.page.int == 0:
                    sorted_contents = []
                    for fandom in self.obj.anth:
                        for work in fandom:
                            sorted_contents.append(work)
                    return sorted_contents
                else:
                    return self.obj.anth[index.page.int-1]
        elif isinstance(self.obj, anthclass.Series):
            return self.obj.contents
        else:
            return []
    def getAnth(self):
        if self.obj == '':
            return []
        else:
            return self.obj.anth

index = ActiveIndex()
work = ActiveObject()
book = ActiveObject()
anth = ActiveObject()
edit = ActiveObject()
fan = ActiveObject()
