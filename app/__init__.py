from app import main
from app import anth
from app import book
from app import misc
from app import edit
from app import fan
# from app import cont

'''
All Module Imports:

Dependant:
    - button

Isolated:
    - dir
    - lib

Library:
    - guizero

The App module is used to create all the gui objects, including screens and windows

# Creates the main window and it's three header tabs (which call active.header)
main.py:
- Main App Window | app.main.app
    - Header Box | app.main.header

# Creates the Anthology Library Page
anth.py:
- Screen | app.anth.screen
    - Footer Box | app.anth.footer
    - Library Master | app.anth.library_master
        - Library Listbox | app.anth.listbox_main
    - Anthology Master Frame | app.anth.anth_master
        - Contents Master Frame | app.anth.contents_master
            - Contents Scrollbox | app.anth.contents_scroll
            - Contents Listbox | app.anth.listbox_contents
        - Work Master
            - Fandom Scrollbox | app.anth.fandom_scroll
            - Entry Scrollbox | app.anth.entry_scroll
            - Main Box | app.anth.main_box
                - Title Box | app.anth.title_box
                - Main Stats Box | app.anth.main_stats_box
                    - Stats Box | app.anth.stats_box
                    - Summary Box | app.anth.summary_box

# Creates the Book Library Page          
book.py:
- Screen | app.book.screen
    - Footer Box | app.book.footer
        - Footer Buttons
    - Main Listbox | app.book.listbox_main
    - Book Details Text | app.book.book_details_text

# Creates the Misc Works Page
misc.py:
- Screen | app.misc.screen
    - Footer Box | app.misc.footer
    - Library Master | app.misc.misc_library_box
        - Sort Combo Box | app.misc.sort_combo_box
        - Library Listbox | app.misc.listbox_main
    - Scraper Master | app.misc.scraper_master
        - Scraper Footer | app.misc.scraper_footer
        - Scraper Textbox | app.misc.links_textbox
    - Write Master | app.misc.write_master
        - Write Footer | app.misc.write_footer

edit.py:
- Screen | app.edit.screen
    - Footer Box | app.edit.footer
    - Contents Master | app.edit.contents_master
        - Fandom Scrollbox | app.edit.fandom_scroll
        - Main Listbox | app.edit.listbox_main
    - Anth Master | app.edit.anth_master
        - Stats Master | app.edit.stats_master
            - Buttons | app.edit.buttons_main'
        - Misc Listbox | app.edit.listbox_misc

fan.py:
- Window | app.fan.window
    - Master Box | app.fan.master_box
        - Header Box | app.fan.header
        - Contents Box | app.fan.contents_box
            - New Fandom Master | app.fan.new_fandom_master
            - Fandom Groups Master | app.fan.fandom_groups_master_box
            - Misc Master | app.fan.misc_master_box
            - Options Box | app.fan.options_box
    - Footer Box | app.fan.footer

cont.py:
- Window | app.cont.window
    - Footer Box | app.cont.footer
    - Fandom Master | app.cont.fandom_master
        - Fandom Combo Box | app.cont.fandom_combo_box
        - Contents Scrollbox | app.cont.contents_scroll
        - Contents Listbox | app.cont.listbox_contents
    - Work Master | app.cont.work_master
        - Stats Master | app.cont.stats_master
            - Buttons | app.cont.buttons_stats
        - Button Bar | app.cont.button_bar
        - Button Footer | app.cont.button_foot
        - Details Master | app.cont.details_master
'''
