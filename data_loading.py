import pandas as pd
from PIL import Image


def load_raw():
    raw = []
    for i in range(2017, 2023):
        raw.append(pd.read_csv('data/' + str(i) + '_LoL_esports_match_data_from_OraclesElixir_20220408.csv', sep=','))
    return pd.concat(raw)
