import requests
from datetime import datetime
import os.path

base_url = 'https://oracleselixir-downloadable-match-data.s3-us-west-2.amazonaws.com'
date = datetime.now().strftime('%Y%m%d')
data_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

for year in range(2014, 2022 + 1):
    filename = f'{year}_LoL_esports_match_data_from_OraclesElixir_{date}.csv'
    url = f'{base_url}/{filename}'
    r = requests.get(url)
    print((url, r.status_code, len(r.content)))
    with open(f'{data_folder}/{filename}', 'wb') as f:
        f.write(r.content)