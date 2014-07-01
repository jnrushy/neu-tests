from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re

class LoginReportsAndSetup(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://neuehouse.lunabell.com:8080/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_login_reports_and_setup(self):
        driver = self.driver
        driver.get(self.base_url + "/neuehouse/signin")
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys("aash")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("letmein1")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        try: self.assertTrue(self.is_element_present(By.ID, "aside"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.ID, "logout"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_link_text("Reports and Setup").click()
        for i in range(60):
            try:
                if self.is_element_present(By.CSS_SELECTOR, "h2"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertTrue(self.is_element_present(By.LINK_TEXT, "Member List"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.LINK_TEXT, "Company Snapshot (M1)"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.LINK_TEXT, "Quickbooks Sync Util"))
        except AssertionError as e: self.verificationErrors.append(str(e))
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
