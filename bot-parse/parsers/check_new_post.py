import json

from parsers.lukhoil import parce_lukhoil
from parsers.tektorg import parce_tek_torg
from parsers.etpgpb import parse_etp_gpb
from parsers.sber import parce_sber

from core.config import KeyWord

names = {
    "LUKH": parce_lukhoil,
    "ROSH": parce_tek_torg,
    "GAZP": parse_etp_gpb,
    "SBER": parce_sber,
}


def get_database_posts():
    with open("package.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    return data


def checks_in_database():
    data = get_database_posts()
    new_all_posts = []

    for company in data.keys():
        for key_word in KeyWord:
            key_word = key_word.value
            posts_site = names[company](key_word=key_word)

            if not posts_site:
                data[company][key_word] = []
                continue

            new_posts = []

            for post in posts_site:
                if post not in data[company][key_word]:
                    new_posts.append(post)
                    data[company][key_word].append(post)

            #data[company][key_word] = posts_site

            new_all_posts.extend(new_posts)

    save_json(data=data)

    return new_all_posts


def save_json(data: dict):
    with open("package.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
