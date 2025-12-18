from bs4 import BeautifulSoup
from selenium import webdriver

import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from core.config import settings


def parce_lukhoil(key_word: str):

    # Init driver
    driver = webdriver.Chrome()
    driver.maximize_window()

    driver.get(settings.parser_config.lukhoil)

    # find tenders
    search_box = driver.find_element(By.CSS_SELECTOR, ".form-control.search-control")
    search_box.send_keys(key_word)
    search_box.send_keys(Keys.ENTER)

    time.sleep(3)

    while True:

        try:
            time.sleep(3)
            driver.execute_script(
                "window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'});"
            )

            load_more_button = driver.find_element(
                By.CSS_SELECTOR, ".button.load-more-button"
            )
            load_more_button.click()
        except:
            break

    soup = BeautifulSoup(driver.page_source, "html.parser")

    driver.quit()

    tenders = []

    for panel in soup.find_all(
        "div", class_="panel-default panel-collapsible panel-tender"
    ):

        tenders.append(
            {
                "company": "#LUKH",
                "name": panel.find("h2").text,
                "customer": panel.find("span").text,
                "key_word": key_word,
            }
        )

    if tenders:
        return tenders

    else:
        return []
