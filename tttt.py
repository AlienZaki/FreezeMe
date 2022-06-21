from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
from selenium.webdriver.support.ui import Select



class TestSelenium:

    def open_browser(self):
      chromedriver_autoinstaller.install()
      opt = webdriver.ChromeOptions()
      opt.add_argument('--disable-blink-features=AutomationControlled')
      opt.add_argument("--start-maximized")
      opt.add_argument("--disable-blink-features")

      opt.add_argument('--disable-cached')
      opt.add_argument('--disable-dev-shm-usage')
      opt.add_argument("--no-sandbox")
      opt.add_argument("--disable-application-cache")
      opt.add_argument("accept-language=en-GB,en;q=0.9,en-US;q=0.8")
      opt.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36')
      opt.add_argument("--start-maximized")
      # opt.add_argument("--headless")
      opt.add_argument("--window-size=1920,1080")

      opt.add_experimental_option("excludeSwitches", ["enable-automation"])
      opt.add_experimental_option('useAutomationExtension', False)
      opt.add_experimental_option("windowTypes", ["webview"])

      self.driver = webdriver.Chrome(options=opt)
      self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

      self.driver.get('https://www.chexsystems.com/web/chexsystems/consumerdebit/page/securityfreeze/placefreeze')



      self.driver.find_element(By.CSS_SELECTOR, '#optionAgree').click()
      self.driver.find_element(By.CSS_SELECTOR, '#deniedYes').click()


      self.driver.find_element(By.CSS_SELECTOR, '#firstName').send_keys('Yixian')
      self.driver.find_element(By.CSS_SELECTOR, '[name*=lastName]').send_keys('Li')

      self.driver.find_element(By.CSS_SELECTOR, '#dobMon').send_keys('06')
      self.driver.find_element(By.CSS_SELECTOR, '[name*=dobDay]').send_keys('20')
      self.driver.find_element(By.CSS_SELECTOR, '[name*=dobYear]').send_keys('1987')

      self.driver.find_element(By.CSS_SELECTOR, '[name*=govtNbrPart1]').send_keys('085')
      self.driver.find_element(By.CSS_SELECTOR, '[name*=govtNbrPart2]').send_keys('98')
      self.driver.find_element(By.CSS_SELECTOR, '[name*=govtNbrPart3]').send_keys('2518')

      self.driver.find_element(By.CSS_SELECTOR, '[name*=vrfyGovtNbrPart1]').send_keys('085')
      self.driver.find_element(By.CSS_SELECTOR, '[name*=vrfyGovtNbrPart2]').send_keys('98')
      self.driver.find_element(By.CSS_SELECTOR, '[name*=vrfyGovtNbrPart3]').send_keys('2518')

      self.driver.find_element(By.CSS_SELECTOR, '#addrLine1').send_keys('21540 23rd Avenue')
      self.driver.find_element(By.CSS_SELECTOR, '#cityName').send_keys('Bayside')
      self.driver.find_element(By.CSS_SELECTOR, '#postalCode').send_keys('11360')
      states = Select(self.driver.find_element(By.CSS_SELECTOR, '#stateCode'))
      states.select_by_value('NY')

      solve_normal_captcha('https://www.chexsystems.com/web/PA_ChexSystemsDotCom/CaptchaLoads.gif?1655817259651')
      self.driver.find_element(By.CSS_SELECTOR, '#captchaText').send_keys('11360')

      self.driver.find_element(By.CSS_SELECTOR, '#submitFreeze').click()

      msg = ''
      errors = ' - '.join([e.text for e in self.driver.find_elements(By.CSS_SELECTOR, '.panel-body[style*=red] li')])
      if errors:
        print(errors)
        return False, errors
      else:
        msg = self.driver.find_element(By.CSS_SELECTOR, '.alert-success').text.replace('\n', ' ').replace('  ', ' ')
        print(msg)
        return True, msg

      input('?')




if __name__ == '__main__':
    TestSelenium().open_browser()
