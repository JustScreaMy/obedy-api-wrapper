import requests
from obedy_api.parser import Parser
from obedy_api.exceptions import InvalidPageTypeException


class APIClient:
    _session: requests.Session
    _base_url: str

    _username: str
    _password: str

    _logged: bool = False
    _paser: Parser

    _pages: dict = {
        'food': '/faces/secured/month.jsp',
        'burza': '/faces/secured/burza.jsp',
        'platby': '/faces/secured/platby.jsp',
        'objednavky': '/faces/secured/objednavky.jsp',
        'historie': '/faces/secured/historie.jsp'
    }

    def __init__(self, url: str, username: str, password: str):
        self._session = requests.Session()
        self._base_url = url
        self._username = username
        self._password = password

    def get_food(self):
        res = self._session.get(self._base_url + self._pages['food'])
        self._paser = Parser(res.text)
        return self._paser.parse_food()

    @property
    def _login_url(self):
        return self._base_url + "/j_spring_security_check"

    @property
    def _logout_url(self):
        return self._base_url + "/logout"

    def login(self):
        token = self.get_token()
        res = self._session.post(self._login_url, data={
            'targetUrl': '/faces/secured/main.jsp',
            'j_username': self._username,
            'j_password': self._password,
            '_csrf': token,
        })
        self._logged = True
        return res.url

    def logout(self):
        token = self.get_token()
        res = self._session.post(self._login_url, data={
            '_csrf': token,
        })
        self._logged = False
        return res.url

    def get_token(self) -> str:
        self._session.get(self._base_url)
        return self._session.cookies['XSRF-TOKEN']

    def __del__(self):
        if self._logged:
            self.logout()
