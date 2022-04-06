from typing import List
import bs4
import re

DATE_RE = '(\d{2}.\d{2}.\d{4})'


class Parser():

    _soup: bs4.BeautifulSoup

    def __init__(self, content: str):
        self._soup = bs4.BeautifulSoup(content, 'html.parser')

    def parse(self):
        pass

    def parse_food(self):
        parsed_food = {}
        for day in self._soup.find(
                id='mainContext').find('table').find_all('tr'):
            date = re.findall(DATE_RE, day.select_one(
                'div.jidelnicekTop').string)[0]
            foods = day.find_all('div', class_='jidWrapCenter')
            parsed_food[date] = list(
                map(lambda x: str(x.contents[0]).lstrip('\n').strip(), foods))
        return parsed_food
