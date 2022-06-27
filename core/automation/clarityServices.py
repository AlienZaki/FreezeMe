from .utils.captcha import CaptchaSolver
from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
import os
import time

os.environ['GH_TOKEN'] = "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"


class ClarityServices:

    def __init__(self):
        self.open_browser()
        self.solver = CaptchaSolver()

    def open_browser(self):
        print('=> Opening browser...')
        #driver_path = chromedriver_autoinstaller.install(path=os.getcwd())
        #print(driver_path)

        opt = webdriver.ChromeOptions()
        opt.add_argument('--disable-dev-shm-usage')
        opt.add_argument("--no-sandbox")    # **
        opt.add_argument("--headless")  # **

        opt.add_argument('--disable-blink-features=AutomationControlled')
        opt.add_argument("--disable-blink-features")
        opt.add_argument('--disable-cached')
        opt.add_argument("--disable-application-cache")
        opt.add_argument("accept-language=en-GB,en;q=0.9,en-US;q=0.8")
        # opt.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36')
        # opt.add_argument("--start-maximized")
        # opt.add_argument("--window-size=1920,1080")
        opt.add_experimental_option("excludeSwitches", ["enable-automation"])
        opt.add_experimental_option('useAutomationExtension', False)
        opt.add_experimental_option("windowTypes", ["webview"])

        self.driver = webdriver.Chrome(options=opt, service=Service(ChromeDriverManager().install()))  #'/usr/local/bin/chromedriver'
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    def submit(self, fname, mname, lname, email, ssn, phone, dob, address_line1, address_line2, zip, city,  state_abbreviation):
        print('=> Submitting...')
        print('=> Opening website...')
        self.driver.get('https://consumers.clarityservices.com/idv?type=PLACE_SECURITY_FREEZE')

        while not self.driver.find_elements(By.CSS_SELECTOR, '#first-name'):
            time.sleep(1)

        print('=> Filling data 1 ...')
        self.driver.find_element(By.CSS_SELECTOR, '#first-name').send_keys(fname)
        self.driver.find_element(By.CSS_SELECTOR, '#last-name').send_keys(lname)

        print('=> Filling data 2 ...')
        self.driver.find_element(By.CSS_SELECTOR, '#ssn-input').send_keys(ssn)

        print('=> Filling data 3 ...')
        self.driver.find_element(By.CSS_SELECTOR, '#dob').send_keys(dob.strftime('%m/%d/%Y'))

        print('=> Filling data 4 ...')
        self.driver.find_element(By.CSS_SELECTOR, '#street1').send_keys(address_line1)
        self.driver.find_element(By.CSS_SELECTOR, '#city').send_keys(city)
        self.driver.find_element(By.CSS_SELECTOR, '#postal-code').send_keys(zip)
        self.driver.find_element(By.CSS_SELECTOR, '#email-input').send_keys(email)

        print('=> Filling data 5 ...')
        states = Select(self.driver.find_element(By.CSS_SELECTOR, '[id*=State]'))
        states.select_by_value(state_abbreviation)

        errors = self.driver.find_elements(By.CSS_SELECTOR, '.v-messages__message')
        if errors:
            errors = '\n'.join([e.text for e in errors])
            return False, errors

        print('=> Filling data 6 ...')
        code = self.solver.solve_recaptcha(site_key='6LdHJZoUAAAAANmKyn_5fJ1UeXrXrrcnUhLRIN_Y', url='https://consumers.clarityservices.com/idv?type=PLACE_SECURITY_FREEZE', invisible=1)['code']
        self.driver.execute_script(f"document.querySelector('#g-recaptcha-response').innerHTML = '{code}';")

        print('=> Filling data 7 ...')
        self.driver.find_element(By.CSS_SELECTOR, '[type="submit"]').click()

        # proccessing
        time.sleep(3)
        while True:
            processing = self.driver.find_elements(By.CSS_SELECTOR, 'svg circle')
            if not processing:
                break

        #input('?')

        errors = '\n'.join([e.text for e in self.driver.find_elements(By.CSS_SELECTOR, '.MuiAlert-standardError')])
        if errors:
            print('=> Failed to submit:', errors)
            return False, errors
        else:
            # check for popup confirm
            popups = self.driver.find_elements(By.CSS_SELECTOR, '.MuiDialog-paper')
            if popups:
                popups[0].find_elements(By.CSS_SELECTOR, 'button')[1].click()

            # proccessing
            time.sleep(3)
            while True:
                processing = self.driver.find_elements(By.CSS_SELECTOR, 'svg circle')
                if not processing:
                    break

            #input('?')

            if 'Unable To Process Request' in self.driver.page_source:
                self.driver.quit()
                return False, 'Unable To Process Request'

            msg = 'success'
            print('=> Submitted Successfully!', msg)
            self.driver.quit()
            return True, msg


