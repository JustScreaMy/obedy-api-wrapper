from typing import List
import bs4
import re

from obedy_api.models import Day, Food

DATE_RE = '(\d{2}.\d{2}.\d{4})'
ORDER_URI_RE = '\'(.*?)\''


class Parser():
    # TODO: Make it reusable?

    _soup: bs4.BeautifulSoup

    def __init__(self, content: str):
        self._soup = bs4.BeautifulSoup(content, 'html.parser')

    def _parse_day(self, foods: bs4.ResultSet, date: str) -> List[Food]:
        fl = []
        for food in foods:
            name = food.find(
                'div', class_='jidWrapCenter').contents[0].lstrip('\n').strip()
            api_uri = re.findall(ORDER_URI_RE, food.find(
                'a', class_='btn')['onclick'])[0]
            price = float(food.find('span', class_='important').string[:-3])
            ordered = not not food.find('span', class_='button-link-tick')
            orderable = not not not food.find('a', class_='disabled')
            fl.append(Food(name, api_uri, price, ordered, orderable))

        return Day(date, fl)

    def parse(self):
        pass

    def parse_credit(self) -> dict:
        cr = self._soup.find('span', id='Kredit').string[:-3].replace(',', '.')
        return {
            'credit': float(cr)
        }

    def parse_food(self) -> List[Day]:
        parsed_days = []

        for day in self._soup.find(
                id='mainContext').find('table').find_all('tr'):
            date = re.findall(DATE_RE, day.select_one(
                'div.jidelnicekTop').string)[0]
            foods = day.find_all('div', class_='jidelnicekItemWrapper')
            parsed_days.append(self._parse_day(foods, date))

        return parsed_days
