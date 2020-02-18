import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


driver_path = os.path.expandvars('$HOME/apps/Selenium/Chrome/chromedriver')
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("user-data-dir=login-data")
browser = webdriver.Chrome(driver_path, chrome_options=chrome_options)
expressvpn_url = 'https://www.expressvpn.com/sign-in'
browser.get(expressvpn_url)
condition = ec.presence_of_element_located((By.ID, "email"))
email = WebDriverWait(browser, 10).until(condition)
password = browser.find_element_by_id('password')
email.send_keys(os.environ.get('EXPRESSVPN_EMAIL'))
password.send_keys(os.environ.get('EXPRESSVPN_PASSWORD'))
print('Logging In....')
browser.find_element_by_name('commit').click()

