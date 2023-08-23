from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

chrome_driver_path = r"PATH\chromedriver.exe"
service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service)

URL = "http://orteil.dashnet.org/experiments/cookie/"
driver.get(url=URL)


def click_cookie():
    cookie = driver.find_element(By.ID,"cookie")
    cookie.click()


def get_cookie_count():
    cookie_counter = driver.find_element(By.ID, "money").text
    if "," in cookie_counter:
        cookie_counter = cookie_counter.replace(",", "")
    return int(cookie_counter)


def buy_upgrade(cookie_count):

    upgrades = driver.find_elements(By.CSS_SELECTOR, "#store b")
    upgrades_list = []
    for _ in range (len(upgrades)):
        upgrade = (upgrades[_].text)
        if upgrade != "":
            upgrades_list.append(upgrade)

    list_upgrade_prices = []
    for upgrade_price in upgrades_list:
        upgrade_price = upgrade_price.split('-')[1].strip()
        if "," in upgrade_price:
            upgrade_price = upgrade_price.replace(",","")
        list_upgrade_prices.append(int(upgrade_price))

    affordable_items=[]
    for item in list_upgrade_prices:
        if item < cookie_count:
            affordable_items.append(item)
    if len(affordable_items) > 0:
        most_expensive_affordable_item = max(affordable_items)

        index_item_to_buy = list_upgrade_prices.index(most_expensive_affordable_item)
        item_to_buy = upgrades_list[index_item_to_buy]
        item_to_buy = str(item_to_buy.split("-")[0].strip())

        buy_item = driver.find_element(By.ID, f"buy{item_to_buy}")
        buy_item.click()

    else:
        pass

t_end = time.time() + 20

game_end = time.time() + (60*5)
game_on = True

while game_on:
    click_cookie()
    if time.time() > t_end:
        cookie_count = get_cookie_count()
        item_to_buy = buy_upgrade(cookie_count)
        t_end = time.time() + 20

    if time.time() > game_end:
        game_on = False
        cookies_per_second = driver.find_element(By.ID,"cps").text
        print(f"Time Up!!, your {cookies_per_second}. Congratulations")
