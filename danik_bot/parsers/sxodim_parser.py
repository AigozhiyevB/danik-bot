import json
import re

import requests
from lxml import html
from bs4 import BeautifulSoup
import typing as tp

from tqdm import tqdm

from danik_bot.parsers.constants import (SxodimConstants, CardProps,
                                         PlaceProps, Place)


class SxodimParser:
    def __init__(self, url = 'https://sxodim.com/almaty/places/cafe'):
        self.base_url = url
        self.base_response = requests.get(url)
        if self.base_response.status_code != 200:
            raise Exception('Something went wrong while parsing')
        self.constants = SxodimConstants
        self.page_count = self._get_page_count()

    def _get_page_count(self)->int:
        soup = BeautifulSoup(self.base_response.text, 'html.parser')
        page_links = soup.find_all(class_=self.constants.page_count.value)
        last_page = int(page_links[-1].text)
        return last_page

    def _ingest_page(self, url)->tp.List[CardProps]:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        cards = soup.find_all('div', class_=self.constants.card_class.value)
        ret = []
        for i in cards:
            props = CardProps(
                link=i.find('a', href=True)['href'],
                name=i['data-title'],
                info=i.find(class_=self.constants.card_info.value).text
            )
            ret.append(props)

        return ret

    def _parse_place(self, url)->PlaceProps:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        tree = html.fromstring(response.text)
        mean_bill = tree.xpath(self.constants.mean_bill_xpath.value)
        mean_bill = mean_bill[0].text if len(mean_bill) > 0 else None
        if mean_bill:
            mean_bill = mean_bill if re.search(r'\d+', mean_bill) else None
        kitchens = [i.text for i in soup.find_all(class_=self.constants.place_kitchen.value)]
        content = soup.find(class_=self.constants.text_content_class.value)
        text = ' '.join([i.text for i in content.find_all('p')])
        date_str = soup.find(class_=self.constants.publication_class.value).text
        match = re.search(self.constants.date_pattern.value, date_str)

        if match:
            date_obj = match.group(1)
        else:
            date_obj = None

        return PlaceProps(mean_bill=mean_bill,
                          kitchens=kitchens,
                          text=text,
                          publication_date=date_obj)

    def _parse_places(self,
                      place_cards: tp.List[CardProps],
                      save_path
    )->tp.Union[tp.List[Place], None]:
        ret = []
        for card in tqdm(place_cards, '[cards from page]'):
            properties = self._parse_place(card.link)
            place = Place(**{**card.dict(), **properties.dict()})
            if save_path:
                with open(save_path, 'a+') as f:
                    f.write(json.dumps(place.dict()))
                    f.write('\n')
            else:
                ret.append(place)

        return None if save_path else ret

    def parse(
            self,
            num_page: tp.Union[int, str] = 'all',
            save_pass = None
    )->tp.Union[tp.List[dict], None]:
        if num_page == 'all':
            num_page = self.page_count
        elif isinstance(num_page, int):
            pass
        else:
            raise ValueError('num_page must either int either "all"')

        ret = []
        for page_number in tqdm(range(1, num_page+1), '[page from pages]'):
            new_link = f'{self.base_url}?page={page_number}'
            cards = self._ingest_page(new_link)
            places = self._parse_places(cards, save_pass)
            if places:
                ret.extend(places)

        return ret if not save_pass else None
