import requests
from bs4 import BeautifulSoup

from core.config import settings


def parce_tek_torg(key_word: str):
    request = requests.get(f"{settings.parser_config.tek_torg}{key_word}")

    soup = BeautifulSoup(request.text, "html.parser")

    now_posts = []
    for tender in soup.find_all("div", class_="sc-6c01eeae-0 jtfzxc"):

        name = tender.find("a")
        now_posts.append(
            {
                "company": "#ROSH",
                "name": f"{name.text}",
                "link": f"{name.get('href')}",
                "customer": f"https://www.tektorg.ru{tender.find('div', class_='sc-6c01eeae-10 hqcmWX').text}",
                "price": f"{tender.find('div', class_='sc-a6b34174-0 cLruXa').text}",
            }
        )

    return now_posts
