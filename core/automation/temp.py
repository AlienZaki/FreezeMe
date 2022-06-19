from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
import chromedriver_autoinstaller



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

      self.driver.get('https://www.ars-consumeroffice.com/add')

      consumer_btn = self.driver.find_element(By.CSS_SELECTOR, 'section > div  button')
      consumer_btn.click()

      terms = self.driver.find_element(By.CSS_SELECTOR, '#mat-checkbox-1')
      terms.click()

      contiue_btn = self.driver.find_element(By.CSS_SELECTOR, '#cdk-step-content-0-0 button.mat-stepper-next.mat-raised-button')
      contiue_btn.click()

      fname = self.driver.find_element(By.CSS_SELECTOR, '#mat-input-5')
      fname.send_keys('asdasd')

      lname = self.driver.find_element(By.CSS_SELECTOR, '#mat-input-7')
      lname.send_keys('asdasd')

      address_line1 = self.driver.find_element(By.CSS_SELECTOR, '#mat-input-9')
      address_line1.send_keys('asdasd')

      address_line2 = self.driver.find_element(By.CSS_SELECTOR, '#mat-input-10')
      address_line2.send_keys('asdasd')

      city = self.driver.find_element(By.CSS_SELECTOR, '#mat-input-11')
      city.send_keys('asdasd')

      city = self.driver.find_element(By.CSS_SELECTOR, '#mat-input-11')
      city.send_keys('asdasd')

      states_select = self.driver.find_element(By.CSS_SELECTOR, '#mat-select-0')
      states_select.click()
      states = self.driver.find_elements(By.CSS_SELECTOR, '#mat-select-0-panel > mat-option > .mat-option-text')
      state = [s for s in states if s.text.upper() == 'California'.upper()]
      state = state[0] if state else None
      state.click()

      zip = self.driver.find_element(By.CSS_SELECTOR, '#mat-input-12')
      zip.send_keys('09654')

      phone = self.driver.find_element(By.CSS_SELECTOR, '#mat-input-13')
      phone.send_keys('7017320037')

      email = self.driver.find_element(By.CSS_SELECTOR, '#mat-input-14')
      email.send_keys('asasdd@rsvssffsdf.vgd')

      ssn = self.driver.find_element(By.CSS_SELECTOR, '#mat-input-15')
      ssn.send_keys('653219874')

      contiue_btn = self.driver.find_element(By.CSS_SELECTOR, '#cdk-step-content-0-1 button.mat-stepper-next.mat-raised-button')
      contiue_btn.click()

      contiue_btn = self.driver.find_element(By.CSS_SELECTOR, '#cdk-step-content-0-2 button.mat-stepper-next.mat-raised-button')
      contiue_btn.click()

      """
      Upload attachments
      """

      attachments = self.driver.find_elements(By.CSS_SELECTOR, 'app-documents > section')
      for attach in attachments:
        header = attach.find_element(By.CSS_SELECTOR, 'section-header').text
        if 'Identification Document' in header:
          # Driver's license, State issued ID card, or Passport.
          attach.find_element(By.CSS_SELECTOR, 'button').click()


        if 'Proof of Residency' in header:
          pass

      input()



if __name__ == '__main__':
    TestSelenium().open_browser()
