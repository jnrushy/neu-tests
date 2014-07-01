from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re

class TestCompanySearch(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://neuehouse.lunabell.com:8080/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_untitled(self):
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
        driver.find_element_by_link_text("Find Company").click()
        driver.find_element_by_css_selector("input[type=\"text\"]").clear()
        driver.find_element_by_css_selector("input[type=\"text\"]").send_keys("neu")
        driver.find_element_by_css_selector("input[type=\"text\"]").send_keys(Keys.RETURN)
        time.sleep(3)
        
        try: self.assertTrue(self.is_element_present(By.LINK_TEXT, "Joshua Abram"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.LINK_TEXT, "New Company"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.LINK_TEXT, "Neuehouse"))
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
