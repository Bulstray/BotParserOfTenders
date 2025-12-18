from requests import Response
from xml.etree import ElementTree


import ssl

import requests
import urllib3
from core.config import settings
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

TITLE = "📌 <b>Тендер #GZ</b>" "\n────────────────────\n\n"


class TLSAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        ctx = create_urllib3_context()
        ctx.set_ciphers("DEFAULT@SECLEVEL=1")
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        kwargs["ssl_context"] = ctx
        return super().init_poolmanager(*args, **kwargs)


def create_session() -> requests.Session:
    session: requests.Session = requests.Session()
    session.headers.update(settings.session_header.headers)
    return session


def create_secure_session() -> requests.Session:
    session = create_session()
    adapter: TLSAdapter = TLSAdapter()
    session.mount("https://", adapter)
    session.verify = False

    return session


SESSION: requests.Session = create_secure_session()


def check_connection(key_word: str) -> None | Response:
    try:
        response: Response = SESSION.get(
            f"{settings.parser_config.etp_gpb}{key_word}",
        )
        response.raise_for_status()
    except requests.exceptions.RequestException:
        return
    else:
        return response


def check_read_xml(text: str):
    try:
        data = ElementTree.fromstring(text)
    except ElementTree.ParseError:
        return
    else:
        return data


def parse_etp_gpb(key_word) -> list:
    response: Response | None = check_connection(key_word=key_word)

    if response is None:
        return []

    content: None | ElementTree = check_read_xml(response.text)

    if content is None:
        return []

    titles = []

    for i, item in enumerate(content.findall(".//item"), 1):

        description, customer, price = item.find("title").text.rsplit(" - ", 2)

        if key_word.lower() not in description.lower():
            continue

        titles.append(
            {
                "company": "#GAZP",
                "name": f"{description}",
                "customer": f"{customer}",
                "price": f"{price}",
                "link": f"{item.find('link').text}",
            }
        )

    return titles
