from button import marginals

# only updates for anthologies
from button import edit
from button import fan
from button import cont

'''
Dependant:
    - data
    - gui
    - fun

Isolated:
    - active
    - lib

The Button module is to connect button presses to actions

# Header and Footer Buttons
marginals.py:
    - Header Buttons
        + active.header.update()
    - Anthology Library Footer Buttons
        - createAnthology
            + fun.anth.create()
        - uploadAnthology
            + fun.anth.upload()
        - downloadAnthology
            + fun.anth.download()
        - removeAnthology
            + fun.anth.remove()
        - editAnthology
            + active.copy.clone('edit')
    - Edit Anthology Footer Buttons
        - addToAnthology
            + fun.anth.addWork()
        - removeFromAnthology
            + fun.anth.removeWork()
        - saveAnthology
            + fun.anth.save()
        - cancelAnthology
            + fun.anth.cancel()
    - Fandom Editing Footer Buttons
        - saveFandom
            + gui.fan.save()
        - cancelFandom
            + active.copy.reset('fan')
    - Works Editing Footer Buttons
        - saveWork
            + gui.cont.save()
            + fun.misc.save()
        - cancelWork
            + active.copy.reset('cont')
            + active.work.reset()
    - Misc Footer Buttons
        - createWorks
            + gui.misc.createWorks()
        - grabWorks
            + gui.misc.grabWorks()
        - uploadWorks
            + fun.misc.upload()
        - makeSeries
            + fun.misc.series()
        - downloadWorks
            fun.misc.downloadWorks()
        - removeWorks
            + fun.misc.remove()
        - editWorks
            # Add functionality
    - Back Button

arrows.py:
    - Fandom Arrows
    - Contents Arrows
    - Entry Arrows

# Conects button presses to active state changes
actives.py:
    - header_update()
    - anth_obj_update()
    - anth_work_update()
    - anth_entry_update()

edit.py
cont.py
fan.py
misc.py
'''
