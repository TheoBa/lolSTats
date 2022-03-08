import pandas as pd

def transform_patch(df):
    df.patch = df.patch.map(lambda x: int(x[2:] + x[:2]))
    return df