

import pandas as pd


def preprocess_dat(fileDat):

    # ? show data from DataEdited
    tableDat = pd.read_csv("DatEdited/"+fileDat.name)
    tableDat.drop(0, inplace=True)
    tableDat.drop(1, inplace=True)

    # set index
    tableDat['index'] = range(1, len(tableDat)+1)
    tableDat.set_index('index', inplace=True)

    # replace missing vlans with 0
    tableDat = tableDat.replace('NAN', 0)
    return tableDat
