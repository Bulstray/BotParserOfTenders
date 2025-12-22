import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

from core.config import settings


def parce_tek_torg(key_word: str):
    request = requests.get(f"{settings.parser_config.tek_torg}{key_word}")

    soup = BeautifulSoup(request.text, "html.parser")

    now_posts = []
    for tender in soup.find_all("div", class_="sc-6c01eeae-0 jtfzxc"):

        time_now = datetime.now().date()

        tender_deadline = (
            tender.find("time", class_="sc-7909e12c-2 fIvbdF")
            .find("span", class_="sc-7909e12c-0 glSvLE")
            .text
        )

        tender_deadline = datetime.strptime(tender_deadline, "%d.%m.%Y").date()

        if tender_deadline > time_now:
            name = tender.find("a")
            now_posts.append(
                {
                    "company": "#ROSH",
                    "name": f"{name.text}",
                    "link": f"https://www.tektorg.ru{name.get('href')}",
                    "customer": f"{tender.find('div', class_='sc-6c01eeae-10 hqcmWX').text}",
                    "price": f"{tender.find('div', class_='sc-a6b34174-0 cLruXa').text}",
                    "key_word": f"{key_word}",
                }
            )

    return now_posts
