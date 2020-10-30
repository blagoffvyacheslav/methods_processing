from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import re

LOGIN = "study.ai_172"
PASS = "NextPassword172"
HOST = "https://account.mail.ru/login/"

chrome_options = Options()
chrome_options.add_argument('start-maximized')
driver = webdriver.Chrome(executable_path='driver',options=chrome_options
)

driver.get(HOST)

login_field = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.NAME,'username'))
)
login_field.send_keys(LOGIN)
login_field.submit()

password_field = WebDriverWait(driver, 30).until(
    EC.visibility_of_element_located((By.NAME,'password'))
)
password_field.send_keys(PASS)
password_field.submit()

inbox_element = WebDriverWait(driver, 30).until(
    EC.visibility_of_element_located((By.CLASS_NAME,'nav__item_active'))
)
title = inbox_element.get_attribute('title')
regex = r"Входящие, (\d*) "
count_emails = int(re.search(regex, title).group(1))

urls_marker = WebDriverWait(driver, 30).until(
    EC.visibility_of_element_located((By.CLASS_NAME,'js-letter-list-item'))
)
url_list = driver.find_elements_by_class_name('js-letter-list-item')
urls = set()

for a in url_list:
    urls.add(a.get_attribute('href'))

while len(urls) != count_emails:
    actions = ActionChains(driver)
    actions.move_to_element(url_list[-1])
    actions.perform()
    time.sleep(1)
    url_list = driver.find_elements_by_class_name('js-letter-list-item')
    for item in url_list:
        urls.add(item.get_attribute('href'))

emails = []
for item in urls:
    driver.get(item)
    letter_author_wrapper = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'letter__author'))
    )
    email = {
        'letter_author': letter_author_wrapper.find_element_by_class_name('letter-contact').get_attribute('title'),
        'letter_date': letter_author_wrapper.find_element_by_class_name('letter__date').text,
        'letter_title': driver.find_element_by_class_name('thread__subject').text,
        'letter_body': driver.find_element_by_class_name('letter-body').text
    }
    emails.append(email)