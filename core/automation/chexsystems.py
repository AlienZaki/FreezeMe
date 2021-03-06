import json
import requests
from bs4 import BeautifulSoup
from .utils.captcha import CaptchaSolver
from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import os

os.environ['GH_TOKEN'] = "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"

class Chexsystems:

    def __init__(self):
        self.open_browser()
        self.solver = CaptchaSolver()

    def open_browser(self):
        print('=> Opening browser...')
        #driver_path = chromedriver_autoinstaller.install(path=os.getcwd())
        #print(driver_path)

        opt = webdriver.ChromeOptions()
        #opt.add_argument('--disable-dev-shm-usage')
        opt.add_argument("--no-sandbox")    # **
        opt.add_argument("--headless")  # **

        #opt.add_argument('--disable-blink-features=AutomationControlled')
        # opt.add_argument("--disable-blink-features")
        # opt.add_argument('--disable-cached')
        # opt.add_argument("--disable-application-cache")
        # opt.add_argument("accept-language=en-GB,en;q=0.9,en-US;q=0.8")
        # opt.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36')
        # opt.add_argument("--start-maximized")
        # opt.add_argument("--window-size=1920,1080")
        # opt.add_experimental_option("excludeSwitches", ["enable-automation"])
        # opt.add_experimental_option('useAutomationExtension', False)
        # opt.add_experimental_option("windowTypes", ["webview"])

        # FireFox binary path (Must be absolute path)
        FIREFOX_BINARY = FirefoxBinary('/opt/firefox/firefox')

        # FireFox PROFILE
        PROFILE = webdriver.FirefoxProfile()
        PROFILE.set_preference("browser.cache.disk.enable", False)
        PROFILE.set_preference("browser.cache.memory.enable", False)
        PROFILE.set_preference("browser.cache.offline.enable", False)
        PROFILE.set_preference("network.http.use-cache", False)
        PROFILE.set_preference("general.useragent.override", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:72.0) Gecko/20100101 Firefox/72.0")

        # FireFox Options
        FIREFOX_OPTS = Options()
        FIREFOX_OPTS.log.level = "trace"  # Debug
        FIREFOX_OPTS.headless = True
        GECKODRIVER_LOG = '/geckodriver.log'
        self.driver = webdriver.Firefox(firefox_profile=PROFILE, options=FIREFOX_OPTS, service_log_path=GECKODRIVER_LOG, executable_path=GeckoDriverManager().install()) #firefox_binary=FIREFOX_BINARY,
        #self.driver = webdriver.Chrome(options=opt, service=Service(GeckoDriverManager().install()))  #'/usr/local/bin/chromedriver'
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    def submit(self, fname, mname, lname, email, ssn, phone, dob, address_line1, address_line2, zip, city,  state_abbreviation):
        print('=> Submitting...')
        print('=> Opening website...')
        self.driver.get('https://www.chexsystems.com/web/chexsystems/consumerdebit/page/securityfreeze/placefreeze')

        print('=> Filling data 1 ...')

        self.driver.find_element(By.CSS_SELECTOR, '#optionAgree').click()
        self.driver.find_element(By.CSS_SELECTOR, '#deniedYes').click()

        print('=> Filling data 2 ...')
        self.driver.find_element(By.CSS_SELECTOR, '#firstName').send_keys(fname)
        self.driver.find_element(By.CSS_SELECTOR, '[name*=lastName]').send_keys(lname)

        print('=> Filling data 3 ...')
        self.driver.find_element(By.CSS_SELECTOR, '#dobMon').send_keys(dob.month)
        self.driver.find_element(By.CSS_SELECTOR, '[name*=dobDay]').send_keys(dob.day)
        self.driver.find_element(By.CSS_SELECTOR, '[name*=dobYear]').send_keys(dob.year)

        print('=> Filling data 4 ...')
        self.driver.find_element(By.CSS_SELECTOR, '[name*=govtNbrPart1]').send_keys(ssn[:3])
        self.driver.find_element(By.CSS_SELECTOR, '[name*=govtNbrPart2]').send_keys(ssn[3:5])
        self.driver.find_element(By.CSS_SELECTOR, '[name*=govtNbrPart3]').send_keys(ssn[5:])

        print('=> Filling data 5 ...')
        self.driver.find_element(By.CSS_SELECTOR, '[name*=vrfyGovtNbrPart1]').send_keys(ssn[:3])
        self.driver.find_element(By.CSS_SELECTOR, '[name*=vrfyGovtNbrPart2]').send_keys(ssn[3:5])
        self.driver.find_element(By.CSS_SELECTOR, '[name*=vrfyGovtNbrPart3]').send_keys(ssn[5:])

        print('=> Filling data 6 ...')
        self.driver.find_element(By.CSS_SELECTOR, '#addrLine1').send_keys(address_line1)
        self.driver.find_element(By.CSS_SELECTOR, '#cityName').send_keys(city)
        self.driver.find_element(By.CSS_SELECTOR, '#postalCode').send_keys(zip)
        states = Select(self.driver.find_element(By.CSS_SELECTOR, '#stateCode'))
        states.select_by_value(state_abbreviation)

        print('=> Filling data 7 ...')
        captcha_image = self.driver.find_element(By.CSS_SELECTOR, '#captcha_image').get_attribute('src')
        print(captcha_image)
        code = self.solver.solve_normal_captcha(captcha_image)['code']
        self.driver.find_element(By.CSS_SELECTOR, '#captchaText').send_keys(code)

        print('=> Filling data 8 ...')
        self.driver.find_element(By.CSS_SELECTOR, '#submitFreeze').click()

        errors = '\n'.join([e.text for e in self.driver.find_elements(By.CSS_SELECTOR, '.panel-body[style*=red] li')])
        if errors:
            print('=> Failed to submit:', errors)
            return False, errors
        else:
            msg = self.driver.find_element(By.CSS_SELECTOR, '.alert-success').text.replace('\n', ' ').replace('  ', ' ')
            print('=> Submitted Successfully!', msg)
            return True, msg

