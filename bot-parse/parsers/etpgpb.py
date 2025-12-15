import requests
from core.config import settings
from requests import Response
from xml.etree import ElementTree

from parsers.base_parser import BaseParser


TITLE = "📌 <b>Тендер #GZ</b>" "\n────────────────────\n\n"


class EtpGpb(BaseParser):
    def __init__(self, key_word: str) -> None:
        super().__init__(key_word=key_word)

    def check_connection(self) -> None | Response:
        try:
            response: Response = self.session.get(
                f"{settings.parser_config.etp_gpb}{self.key_word}",
            )
            response.raise_for_status()
        except requests.exceptions.RequestException:
            return
        else:
            return response

    def check_read_xml(self, text: str):
        try:
            data = ElementTree.fromstring(text)
        except ElementTree.ParseError:
            return
        else:
            return data

    def parse_etp_gpb(self) -> list[str]:
        response: Response | None = self.check_connection()

        if response is None:
            return "Не получилось получить данные #GZ"

        content: None | ElementTree = self.check_read_xml(response.text)

        if content is None:
            return "Не получилось получить данные #GZ"

        titles: list[str] = []

        for i, item in enumerate(content.findall(".//item"), 1):

            description, customer, price = item.find("title").text.rsplit(" - ", 2)

            title = (
                f"\n\n{TITLE}<b>{i}) Наименование:</b>\n{description}\n\n"
                f"<b>Заказчик:</b> {customer}\n"
                f"<b>Стоимость:</b> {price}\n"
                f"<b>Ссылка:</b> {item.find('link').text}\n"
                f"────────────────────"
            )

            titles.append(title)

        return titles
