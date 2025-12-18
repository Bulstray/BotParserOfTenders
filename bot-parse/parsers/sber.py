from bs4 import BeautifulSoup
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from core.config import settings

import time


def parce_sber(key_word: str):

    driver = webdriver.Chrome()
    driver.maximize_window()

    driver.get(settings.parser_config.sber)

    search_box = driver.find_element(
        By.ID,
        "txtUnitedPurchaseSearch",
    )

    time.sleep(3)

    search_box.send_keys(key_word)
    search_box.send_keys(Keys.ENTER)

    time.sleep(15)

    select_element = driver.find_element(By.ID, "headerPagerSelect")

    dropdown = Select(select_element)
    dropdown.select_by_visible_text("100")

    html = driver.execute_script("return document.documentElement.outerHTML;")

    soup = BeautifulSoup(html, "lxml")

    driver.quit()

    tenders = []

    try:

        for panel in soup.find_all("tbody"):

            name = panel.find("span", class_="es-el-name")

            if name is None:
                continue

            tenders.append(
                {
                    "company": "#SBER",
                    "customer": f"{panel.find('div', class_="es-el-org-name").text}",
                    "name": f"{name.text}",
                    "price": f"{panel.find('span', class_='es-el-amount').text}",
                }
            )

        return tenders
    except:
        return []
