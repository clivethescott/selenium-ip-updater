import os

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


def dynu(browser, ip):

    print('Updating Dynu....')
    dynu_url = \
        'https://www.dynu.com/ControlPanel/Login?ReturnUrl=%2fen-US%2fControlPanel'
    browser.get(dynu_url)
    condition = ec.presence_of_element_located((By.ID, "Username"))
    username = WebDriverWait(browser, 10).until(condition)
    username.send_keys(os.environ.get('DYNU_USER'))
    password = browser.find_element_by_id('Password')
    password.send_keys(os.environ.get('DYNU_PASSWORD'))
    browser.find_element_by_name('SubmitButton').click()
    condition = ec.presence_of_element_located((By.ID, "LinkControlPanelDDNSServices"))
    ddns = WebDriverWait(browser, 10).until(condition)
    ddns.click()
    condition = ec.presence_of_element_located((By.CLASS_NAME, "pointer"))
    edit_ddns = WebDriverWait(browser, 10).until(condition)
    edit_ddns.click()
    condition = ec.presence_of_element_located((By.ID, "IPv4Address"))
    ipaddress = WebDriverWait(browser, 10).until(condition)
    ipaddress.clear()
    ipaddress.send_keys(ip)
    browser.find_element_by_name('SubmitButton').click()
    print('Dynu updated!')



if __name__ == "__main__":
    driver_path = os.path.expandvars('$HOME/apps/Selenium/Chrome/chromedriver')
    browser = webdriver.Chrome(driver_path)
    ip = requests.get('https://api.ipify.org').text
    dynu(browser, ip)
else:
    print('Run as script!')
