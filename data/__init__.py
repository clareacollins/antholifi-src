from data import cont
from data import work
from data import book

'''
Dependant:
    - app

Isolated:
    - dir
    - lib
    - actives
    - utils

Grab:
    - Assigns values to guizero objects based on active objects
Clear:
    - Clears all guizero objects
Selected:
    - returns selected listbox values (so active module doesn't have to import app)
'''

def clear():
    cont.clear()
    work.clear()
    book.clear()
