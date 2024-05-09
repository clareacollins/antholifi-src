# Because of the position of this file, don't import anything else from the app here.
from guizero import App, Box

app = App(title="Antholifi", width=750, bg = "white smoke")
header = Box(app, width="fill", height=50, align="top")
tab = 'Anthology Library'

def update(type, screen):
    global tab
    for child in header.children:
        child.bg = "white smoke"
        if child.text == type:
            child.bg = "white"
    for child in app.children[1:]:
        child.hide()
    screen.show()
    tab = type
