import dir
import fun
import utils

import os
import pickle

def makeAllAnths():
    for f in os.listdir(dir.anth_cont):
        if f != 'AUTHOR':
            print(f)
            fun.anth.create(os.path.join(dir.anth_cont, f))

def downloadAllAnths():
    for f in os.listdir(dir.anth):
        utils.files.makeEpub(pickle.load(open(os.path.join(dir.anth, f),'rb')), dir.pos, anthBool=True)
