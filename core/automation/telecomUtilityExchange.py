from .utils.captcha import CaptchaSolver
from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.service import Service
import os
import time

os.environ['GH_TOKEN'] = "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"


class TelecomUtilityExchange:

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
        #opt.add_argument("--headless")  # **

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
        self.driver.get('https://www.exchangeservicecenter.com/Freeze/#/')

        while not self.driver.find_elements(By.CSS_SELECTOR, 'input[lang*=requiredFirstName]'):
            time.sleep(1)

        print('=> Filling data 1 ...')
        self.driver.find_element(By.CSS_SELECTOR, 'input[lang*=requiredFirstName]').send_keys(fname)
        self.driver.find_element(By.CSS_SELECTOR, 'input[lang*=requiredLastName]').send_keys(lname)

        print('=> Filling data 2 ...')
        self.driver.find_element(By.CSS_SELECTOR, 'input[lang*=requiredSsn]').send_keys(ssn)

        print('=> Filling data 3 ...')
        self.driver.find_element(By.CSS_SELECTOR, 'input[lang*=requiredBirthdate]').send_keys(dob.strftime('%m/%d/%Y'))

        print('=> Filling data 4 ...')
        self.driver.find_element(By.CSS_SELECTOR, 'input[lang*=requiredAddress]').send_keys(address_line1)
        self.driver.find_element(By.CSS_SELECTOR, 'input[lang*=requiredCity]').send_keys(city)
        self.driver.find_element(By.CSS_SELECTOR, 'input[lang*=requiredZip]').send_keys(zip)

        print('=> Filling data 5 ...')
        self.driver.find_element(By.CSS_SELECTOR, 'input[lang*=requiredState]').find_element(By.XPATH, '..').click()
        states = self.driver.find_elements(By.CSS_SELECTOR, '.v-list-item__title')
        states[0].find_element(By.XPATH, '..').find_element(By.XPATH, '..').click()
        self.driver.execute_script(f"document.querySelector('.v-select__selection.v-select__selection--comma').innerHTML = '{state_abbreviation}';")


        print('=> Filling data 6 ...')
        code = self.solver.solve_recaptcha(site_key='6LddetAaAAAAAHQJkMXf8jX0bnlkIBor_6N9MJbD', url='https://www.exchangeservicecenter.com/Freeze/')['code']
        self.driver.execute_script(f"document.querySelector('#g-recaptcha-response').innerHTML = '{code}';")
        main_window = self.driver.current_window_handle
        self.driver.switch_to.frame(self.driver.find_element(By.TAG_NAME, 'iframe'))
        self.driver.find_element(By.CSS_SELECTOR, '#recaptcha-anchor').click()
        self.driver.switch_to.window(main_window)

        print('=> Filling data 7 ...')
        self.driver.find_element(By.CSS_SELECTOR, 'input[lang*=requiredAcceptTerms]').find_element(By.XPATH, '..').click()
        self.driver.find_element(By.CSS_SELECTOR, 'button[lang*=continue]').click()

        while self.driver.find_elements(By.CSS_SELECTOR, 'button[lang*=continue]'):
            time.sleep(1)

        errors = '\n'.join([e.text for e in self.driver.find_elements(By.CSS_SELECTOR, '[lang="additionalInfo.p1"]')])
        if errors:
            print('=> Failed to submit:', errors)
            return False, errors
        else:
            msg = self.driver.find_element(By.CSS_SELECTOR, '[lang*=title]').text
            print('=> Submitted Successfully!', msg)
            return True, msg

