import json
import requests
from bs4 import BeautifulSoup
from .utils.captcha import CaptchaSolver
from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
import os


class Chexsystems:

    def __init__(self):
        self.open_browser()
        self.solver = CaptchaSolver()

    def open_browser(self):
        #driver_path = chromedriver_autoinstaller.install(path=os.getcwd())
        #print(driver_path)

        opt = webdriver.ChromeOptions()
        opt.add_argument('--disable-blink-features=AutomationControlled')
        opt.add_argument("--start-maximized")
        opt.add_argument("--disable-blink-features")
        opt.add_argument('--disable-cached')
        opt.add_argument('--disable-dev-shm-usage')
        opt.add_argument("--no-sandbox")
        opt.add_argument("--disable-application-cache")
        opt.add_argument("accept-language=en-GB,en;q=0.9,en-US;q=0.8")
        opt.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36')
        opt.add_argument("--start-maximized")
        opt.add_argument("--headless")
        opt.add_argument("--window-size=1920,1080")
        opt.add_experimental_option("excludeSwitches", ["enable-automation"])
        opt.add_experimental_option('useAutomationExtension', False)
        opt.add_experimental_option("windowTypes", ["webview"])
        self.driver = webdriver.Chrome(options=opt,service=Service(ChromeDriverManager().install()))
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    def submit(self, fname, mname, lname, email, ssn, phone, dob, address_line1, address_line2, zip, city,  state_abbreviation):

        self.driver.get('https://www.chexsystems.com/web/chexsystems/consumerdebit/page/securityfreeze/placefreeze')

        self.driver.find_element(By.CSS_SELECTOR, '#optionAgree').click()
        self.driver.find_element(By.CSS_SELECTOR, '#deniedYes').click()

        self.driver.find_element(By.CSS_SELECTOR, '#firstName').send_keys(fname)
        self.driver.find_element(By.CSS_SELECTOR, '[name*=lastName]').send_keys(lname)

        self.driver.find_element(By.CSS_SELECTOR, '#dobMon').send_keys(dob.month)
        self.driver.find_element(By.CSS_SELECTOR, '[name*=dobDay]').send_keys(dob.day)
        self.driver.find_element(By.CSS_SELECTOR, '[name*=dobYear]').send_keys(dob.year)

        self.driver.find_element(By.CSS_SELECTOR, '[name*=govtNbrPart1]').send_keys(ssn[:3])
        self.driver.find_element(By.CSS_SELECTOR, '[name*=govtNbrPart2]').send_keys(ssn[3:5])
        self.driver.find_element(By.CSS_SELECTOR, '[name*=govtNbrPart3]').send_keys(ssn[5:])

        self.driver.find_element(By.CSS_SELECTOR, '[name*=vrfyGovtNbrPart1]').send_keys(ssn[:3])
        self.driver.find_element(By.CSS_SELECTOR, '[name*=vrfyGovtNbrPart2]').send_keys(ssn[3:5])
        self.driver.find_element(By.CSS_SELECTOR, '[name*=vrfyGovtNbrPart3]').send_keys(ssn[5:])

        self.driver.find_element(By.CSS_SELECTOR, '#addrLine1').send_keys(address_line1)
        self.driver.find_element(By.CSS_SELECTOR, '#cityName').send_keys(city)
        self.driver.find_element(By.CSS_SELECTOR, '#postalCode').send_keys(zip)
        states = Select(self.driver.find_element(By.CSS_SELECTOR, '#stateCode'))
        states.select_by_value(state_abbreviation)

        captcha_image = self.driver.find_element(By.CSS_SELECTOR, '#captcha_image').get_attribute('src')
        print(captcha_image)
        code = self.solver.solve_normal_captcha(captcha_image)['code']
        self.driver.find_element(By.CSS_SELECTOR, '#captchaText').send_keys(code)

        self.driver.find_element(By.CSS_SELECTOR, '#submitFreeze').click()

        errors = ' - '.join([e.text for e in self.driver.find_elements(By.CSS_SELECTOR, '.panel-body[style*=red] li')])
        if errors:
            print('=> Failed to submit:', errors)
            return False, errors
        else:
            msg = self.driver.find_element(By.CSS_SELECTOR, '.alert-success').text.replace('\n', ' ').replace('  ', ' ')
            print('=> Submitted Successfully!', msg)
            return True, msg

