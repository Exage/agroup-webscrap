from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

company_url = 'https://agroup.by/'
category_url = f'{company_url}kompyuternaya-tekhnika/noutbuki-i-aksessuary/noutbuki/'

driver = webdriver.Chrome()
driver.get(category_url)

# Таймер, установлен так как интернет универа калл
time.sleep(10)

# Убить ебучие кукиы
cookies = driver.find_element(By.CSS_SELECTOR, 'div.cookies')
driver.execute_script('arguments[0].setAttribute("style", "display: none")', cookies)

# Найти элементы с первой по пятую страницу 
for i in range(4):
    load_more_button = driver.find_element(By.CSS_SELECTOR, 'button.btn.btn--more')
    
    load_more_button.click()

    time.sleep(10)

soup = BeautifulSoup(driver.page_source, 'html.parser')

products = soup.find_all('div', 'product-grid__list-item')

for product in products:
    print(product.find('div', 'product-list-item__name').text.replace('Ноутбук', '').replace('Игровой', '').replace('ноутбук', '').strip())
