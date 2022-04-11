import pandas as pd
import glob
from utils import DATA_FOLDER


def load_raw():
    raw = []
    for year in range(2017, 2023):
        raw.append(
            pd.read_csv(
                glob.glob(DATA_FOLDER + f'/{year}_LoL_esports_match_data_from_OraclesElixir_*.csv')[0], sep=','
            )
        )
    return pd.concat(raw)
