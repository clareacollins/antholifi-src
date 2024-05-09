import lib
import active, appclass

from button import marginals

from guizero import Box, PushButton

from app import main

screen = Box(main.app, visible=False, align="top", border=0, width="fill", height="fill")

tab = PushButton(main.header, command=main.update, args=['Book Library', screen], text="Book Library", align="left", width="fill", height="fill")

'''Footer'''
footer = appclass.MarginalElement(screen, buttons=[
                                ['add', None, [], 'Add to Library', True],
                                ['remove', None, [], 'Remove from Library', False],
                                ['back', marginals.back_button_pressed, [], 'Back', False]
                                ])

'''List Box'''
library = appclass.ListElement(screen, active.book, items=lib.book, width=250)

'''Details'''
details = Box(screen, align="top", width="fill", height="fill", visible=False)

stats = appclass.TextDisplay(details, lines=[
    ("title", 20, False),
    ("fandom", 15, 500),
    ("words", 15, False),
    ("summary", 12, False)
    ])

def update():
    element_visibility = [
        # Visible depending on active.anth.obj
        (bool(active.book.obj != ""), [details, footer.remove, footer.back])]
    # Test Elements
    for test, elements in element_visibility:
        for element in elements:
            element.visible = test

library.gui = appclass.GUIConnector(update=[stats],
                                    method=[update])
