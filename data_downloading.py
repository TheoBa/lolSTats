import requests
from datetime import datetime
import os.path
import argparse
from pytz import timezone
from utils import IMAGE_FOLDER


def download_csv():
    base_url = 'https://oracleselixir-downloadable-match-data.s3-us-west-2.amazonaws.com'
    date = datetime.now(timezone('US/Eastern')).strftime('%Y%m%d')
    data_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

    for year in range(2014, 2022 + 1):
        filename = f'{year}_LoL_esports_match_data_from_OraclesElixir_{date}.csv'
        url = f'{base_url}/{filename}'
        r = requests.get(url)
        print((url, r.status_code, len(r.content)))
        with open(f'{data_folder}/{filename}', 'wb') as f:
            f.write(r.content)


class Champions:

    def __init__(self, patch_version: str = "12.6.1"):
        patch_version = patch_version
        self.base_url = f"http://ddragon.leagueoflegends.com/cdn/{patch_version}"

    def list_champions(self):
        url = f'{self.base_url}/data/en_US/champion.json'
        result = requests.get(url).json()
        return [
            {'id': item.get('id'), 'name': item.get('name')}
            for item in result.get('data').values()
        ]

    def download_champion_images(self):
        champion_data = self.list_champions()
        for champion_item in champion_data:
            champion_id, champion_name = champion_item.get('id'), champion_item.get('name')
            base_url = f"https://ddragon.leagueoflegends.com/cdn/12.6.1/img/champion"
            url = f"{base_url}/{champion_id}.png"
            r = requests.get(url)
            print((url, r.status_code, champion_id, champion_name))
            with open(f'{IMAGE_FOLDER}/{champion_name}.png', 'wb') as f:
                f.write(r.content)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some downloads.')
    parser.add_argument('--csv', action='store_true', help='Download csv files')
    parser.add_argument('--images', action='store_true', help='Download csv files')
    args = parser.parse_args()
    if args.csv:
        download_csv()
    if args.images:
        champions = Champions()
        champions.download_champion_images()
