import pandas as pd
import data_processing as process


raw = pd.read_csv('data/2022_LoL_esports_match_data_from_OraclesElixir_20220301.csv', sep=';')

#raw = process.transform_patch(raw)