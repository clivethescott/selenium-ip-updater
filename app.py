import os
import time

import requests
import keyring
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
    dynu_user = os.environ.get('DYNU_USER')
    username.send_keys(dynu_user)
    password = browser.find_element_by_id('Password')
    password.send_keys(keyring.get_password("dynu", dynu_user))
    print('Logging into to Dynu...')
    browser.find_element_by_name('SubmitButton').click()
    condition = ec.presence_of_element_located(
        (By.ID, "LinkControlPanelDDNSServices"))
    ddns = WebDriverWait(browser, 10).until(condition)
    print('Going to DDNS settings')
    ddns.click()
    condition = ec.presence_of_element_located((By.CLASS_NAME, "pointer"))
    edit_ddns = WebDriverWait(browser, 10).until(condition)
    print('Editing DDNS settings')
    edit_ddns.click()
    condition = ec.presence_of_element_located((By.ID, "IPv4Address"))
    ipaddress = WebDriverWait(browser, 10).until(condition)
    ipaddress.clear()
    ipaddress.send_keys(ip)
    print('Submitting IP change')
    browser.find_element_by_name('SubmitButton').click()
    print('Dynu updated!')


def expressvpn(browser, ip):
    print('Updating Express VPN')
    expressvpn_url = 'https://www.expressvpn.com/sign-in'
    browser.get(expressvpn_url)
    condition = ec.presence_of_element_located((By.ID, "email"))
    email = WebDriverWait(browser, 10).until(condition)
    password = browser.find_element_by_id('password')
    expressvpn_user = os.environ.get('EXPRESSVPN_EMAIL')
    email.send_keys(expressvpn_user)
    password.send_keys(keyring.get_password("expressvpn", expressvpn_user))
    print('Logging In....')
    browser.find_element_by_name('commit').click()
    condition = ec.presence_of_element_located((By.CLASS_NAME, "container"))
    WebDriverWait(browser, 10).until(condition)
    print('Going to DNS settings')
    browser.get('https://www.expressvpn.com/dns_settings')
    condition = ec.presence_of_element_located((By.ID, "ip-button"))
    ip_button = WebDriverWait(browser, 10).until(condition)
    if not ip_button.is_enabled():
        print('Updating DNS setting')
        ip_button.click()
        print('Express VPN IP registered!')
    else:
        print('No need to update Express VPN, IP registered')


if __name__ == "__main__":
    driver_path = os.path.expandvars('$HOME/apps/Selenium/Chrome/chromedriver')
    chrome_options = webdriver.ChromeOptions()
    # Use previously set data to prevent 2 factor auth
    chrome_options.add_argument("user-data-dir=login-data")
    browser = webdriver.Chrome(driver_path, chrome_options=chrome_options)
    ip = requests.get('https://api.ipify.org').text
    dynu(browser, ip)
    time.sleep(3)
    expressvpn(browser, ip)
    browser.quit()
else:
    print('Run as script!')
