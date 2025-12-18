from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


import time

# Создаём драйвер Edge
driver = webdriver.Chrome()

driver.maximize_window()

driver.get(
    "https://lukoil.ru/Company/Tendersandauctions/Tenders/TendersofLukoilgroup?tab=1&organization=0&country=0"
)

search_box = driver.find_element(By.CSS_SELECTOR, ".form-control.search-control")

search_box.send_keys("балло")
search_box.send_keys(Keys.ENTER)

time.sleep(5)


# while True:
#
#     try:
#         time.sleep(5)
#         driver.execute_script(
#             "window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'});"
#         )
#
#         load_more_button = driver.find_element(
#             By.CSS_SELECTOR, ".button.load-more-button"
#         )
#         load_more_button.click()
#     except:
#         break


soup = BeautifulSoup(driver.page_source, "html.parser")


for panel in soup.find_all(
    "div", class_="panel-default panel-collapsible panel-tender"
):
    print(panel.find("h2").text)
