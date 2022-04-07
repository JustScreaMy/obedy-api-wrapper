from typing import List
import bs4
import re
from obedy_api.models import DayMenu, Food, MonthMenu

DATE_RE = '(\d{2}.\d{2}.\d{4})'
ORDER_URI_RE = '\'(.*?)\''


class Parser():

    _soup: bs4.BeautifulSoup

    def __init__(self, content: str):
        self._soup = bs4.BeautifulSoup(content, 'html.parser')

    def _parse_day(self, date: str, foods: bs4.ResultSet) -> DayMenu:
        parsed = []
        for food in foods:
            name = food.find(
                'div', class_='jidWrapCenter').contents[0].lstrip('\n').strip()
            api_uri = re.findall(ORDER_URI_RE, food.find(
                'a', class_='btn')['onclick'])[0]
            parsed.append(Food(name, api_uri))
        return DayMenu(date, parsed)

    def parse(self):
        pass

    def parse_food(self) -> MonthMenu:
        parsed_days = []
        for day in self._soup.find(
                id='mainContext').find('table').find_all('tr'):
            date = re.findall(DATE_RE, day.select_one(
                'div.jidelnicekTop').string)[0]
            foods = day.find_all('div', class_='jidelnicekItemWrapper')
            parsed_days.append(self._parse_day(date, foods))
        return MonthMenu(parsed_days)
