from datetime import datetime
from enum import Enum
from pydantic import BaseModel
import typing as tp


class SxodimConstants(Enum):
    page_count = 'page-link'
    card_class = 'impression-card'
    card_info = 'impression-card-info'
    mean_bill_xpath = '//*[@id="content"]/div[3]/div[3]/div[1]/div/div[1]/div[1]/div[1]'
    text_content_class = 'content_wrapper'
    place_kitchen = 'text kitchen'
    publication_class = 'publication'
    date_pattern = r"\b(\d{2}\.\d{2}\.\d{4})\b"

class CardProps(BaseModel):
    info: str
    link: str
    name: str

class PlaceProps(BaseModel):
    mean_bill: tp.Optional[str]
    kitchens: tp.List[str]
    text: str
    publication_date: str

class Place(CardProps, PlaceProps):
    pass