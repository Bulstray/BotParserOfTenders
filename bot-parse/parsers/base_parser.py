import ssl

import requests
import urllib3
from core.config import settings
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context

# Отключаем предупреждения о безопасности
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class TLSAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        ctx = create_urllib3_context()
        ctx.set_ciphers("DEFAULT@SECLEVEL=1")
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        kwargs["ssl_context"] = ctx
        return super().init_poolmanager(*args, **kwargs)


class BaseParser:
    def __init__(self, key_word: str) -> None:
        self.session: requests.Session = self.create_secure_session()
        self.key_word: str = key_word

    def create_secure_session(self) -> requests.Session:
        session = self.create_session()
        adapter: TLSAdapter = TLSAdapter()
        session.mount("https://", adapter)
        session.verify = False

        return session

    @staticmethod
    def create_session() -> requests.Session:
        session: requests.Session = requests.Session()
        session.headers.update(settings.session_header.headers)
        return session
