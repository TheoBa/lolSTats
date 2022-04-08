import requests
from datetime import datetime
import os.path
import argparse


def download_csv():
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


class Champions:

    IMAGE_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'champion_images')

    def __init__(self, patch_version: str = "12.6.1"):
        patch_version = patch_version
        self.base_url = f"http://ddragon.leagueoflegends.com/cdn/{patch_version}"

    def list_champions(self):
        url = f'{self.base_url}/data/en_US/champion.json'
        result = requests.get(url).json()
        return list(result.get('data').keys())

    def download_champion_images(self):
        champion_names = self.list_champions()
        for name in champion_names:
            base_url = f"https://ddragon.leagueoflegends.com/cdn/12.6.1/img/champion"
            filename = f"{name}.png"
            url = f"{base_url}/{filename}"
            r = requests.get(url)
            print((url, filename, r.status_code))
            with open(f'{self.IMAGE_FOLDER}/{filename}', 'wb') as f:
                f.write(r.content)


parser = argparse.ArgumentParser(description='Process some downloads.')
parser.add_argument('--csv', action='store_true', help='Download csv files')
parser.add_argument('--images', action='store_true', help='Download csv files')
args = parser.parse_args()
if args.csv:
    download_csv()
if args.images:
    champions = Champions()
    champions.download_champion_images()
