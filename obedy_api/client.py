import requests
from obedy_api.models import Food
from obedy_api.parser import Parser
from obedy_api.exceptions import InvalidPageTypeException


class APIClient:
    _session: requests.Session
    _base_url: str

    _username: str
    _password: str

    _logged: bool = False

    _pages: dict = {
        'food': 'faces/secured/month.jsp',
        'burza': 'faces/secured/burza.jsp',
        'platby': 'faces/secured/platby.jsp',
        'objednavky': 'faces/secured/objednavky.jsp',
        'historie': 'faces/secured/historie.jsp',
        'secured': 'faces/secured/',
    }

    def __init__(self, url: str, username: str, password: str):

        self._session = requests.Session()
        if not url.endswith('/'):
            url += '/'
        self._base_url = url
        self._username = username
        self._password = password

    # TODO: reuse parser?
    def _get_parser(self, html: str):
        return Parser(html)

    def order(self, food: Food):

        res = self._session.get(
            self._base_url + self._pages['secured'] + food.api_uri)

        print(res.text)

        return

    def get_food(self):

        page = self._get_page('food')
        parser = self._get_parser(page)

        return parser.parse_food()

    def get_credit(self):

        page = self._get_page('food')
        parser = self._get_parser(page)

        return parser.parse_credit()

    @property
    def _login_url(self):
        return self._base_url + "j_spring_security_check"

    @property
    def _logout_url(self):
        return self._base_url + "logout"

    def login(self):

        token = self._get_token()
        res = self._session.post(self._login_url, data={
            'targetUrl': 'faces/secured/main.jsp',
            'j_username': self._username,
            'j_password': self._password,
            '_csrf': token,
        })
        self._logged = True

        return res.url

    def logout(self):

        token = self._get_token()
        res = self._session.post(self._login_url, data={
            '_csrf': token,
        })
        self._logged = False

        return res.url

    def _get_token(self) -> str:

        self._session.get(self._base_url)

        return self._session.cookies['XSRF-TOKEN']

    def _get_page(self, page: str):

        if page not in self._pages:
            raise InvalidPageTypeException

        return self._session.get(self._base_url + self._pages[page]).text

    def __del__(self):

        if self._logged:
            self.logout()
