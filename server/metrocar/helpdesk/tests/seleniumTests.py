# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class ChangeLanguageFormTestCase(unittest.TestCase):
    """
    Tests form for change language.
    1. Set lang to en and check page content. Should be in EN.
    2. Set lang to cs and check page content. Should be in CS.
    3. Change lang back to en and check page content. Should be in EN.
    """
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:8000"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_lang(self):
        driver = self.driver
        driver.get(self.base_url + "/bugrep/change_language/")
        # Select EN in form and send it.
        Select(driver.find_element_by_name("language")).select_by_visible_text("English (en)")
        driver.find_element_by_css_selector("input.btn.btn-primary").click()
        # Check page lang.
        self.assertTrue(u'Change the display language' in driver.page_source)
        try: self.assertTrue(self.is_element_present(By.XPATH, "//a[@href='/bugrep/change_language/' and contains(text(),'Change language')]"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        # Select CS in form and send it.
        Select(driver.find_element_by_name("language")).select_by_visible_text(u"česky (cs)")
        driver.find_element_by_css_selector("input.btn.btn-primary").click()
        # Check page lang, should be cs.
        self.assertTrue(u'Změnit jazyk stránek' in driver.page_source)
        try: self.assertTrue(self.is_element_present(By.XPATH, u"//a[@href='/bugrep/change_language/' and contains(text(),'Změnit jazyk')]"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        # Change back to EN and check page lang, should be EN.
        Select(driver.find_element_by_name("language")).select_by_visible_text("English (en)")
        driver.find_element_by_css_selector("input.btn.btn-primary").click()
        self.assertTrue(u'Change the display language' in driver.page_source)
        try: self.assertTrue(self.is_element_present(By.XPATH, "//a[@href='/bugrep/change_language/' and contains(text(),'Change language')]"))
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

class CustomerLoginLogoutTestCase(unittest.TestCase):
    """
    Test Login and Logout of customer.
    1. Customer fills the form and clicks Login button. -> Customer is logged in.
    2. Customer clicks Logout in Menu. -> Customer is logged out.
    Ends on Login page.
    """
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:8000"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_login_logout(self):
        driver = self.driver
        # go to Login page
        driver.get(self.base_url + "/bugrep/login/")
        try: self.assertTrue(self.is_element_present(By.XPATH, "//h2[contains(text(),'Login')]"))
        except AssertionError as e: self.verificationErrors.append(str(e))     
        # fill in the login form   
        driver.find_element_by_id("id_username").clear()
        driver.find_element_by_id("id_username").send_keys("zakaznik")
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys("password")
        driver.find_element_by_css_selector("input.btn.btn-primary").click()
        # check redirect - should be on Helpdesk title page
        try: self.assertTrue(self.is_element_present(By.XPATH, "//h1[contains(text(),'Metrocar Helpdesk')]"))
        except AssertionError as e: self.verificationErrors.append(str(e))    
        # Logout        
        driver.find_element_by_link_text("Logout").click()
        # Should be on Login Page
        try: self.assertTrue(self.is_element_present(By.XPATH, "//h2[contains(text(),'Login')]"))
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


class TicketLifeCycleTestCase(unittest.TestCase):
    """
    This test case tests ticket life cycle.
    1. Customer reports a defect (login, report defect, logout).
    2. Admin approves defect (login, approve defect, logout).
    3. Technician takes report to resolve it (login, take defect).
    4. Technician resolves defect (change status + description, logout).
    5. Admin approves solution and closes ticket (login, approve solution, logout).
    """
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:8000"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_ticket_lifecycle(self):
        import random, string
        ticket_title = ''.join(random.choice(string.lowercase) for i in range(10))
        
        driver = self.driver
        driver.get(self.base_url + "/bugrep/login/")
        # customer login
        driver.find_element_by_id("id_username").clear()
        driver.find_element_by_id("id_username").send_keys("zakaznik")
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys("password")
        driver.find_element_by_css_selector("input.btn.btn-primary").click()
        
        # customer - report defect
        driver.find_element_by_link_text("Report a car defect").click()
        # customer - filling defect reprot form
        Select(driver.find_element_by_id("id_queue")).select_by_visible_text(u"Název typu")
        driver.find_element_by_id("id_title").clear()
        driver.find_element_by_id("id_title").send_keys(ticket_title)
        driver.find_element_by_id("id_body").clear()
        driver.find_element_by_id("id_body").send_keys(u"Popis závady")
        driver.find_element_by_css_selector("input.btn.btn-primary").click()
        # customer logout
        driver.find_element_by_link_text("Logout").click()
        
        # admin login
        driver.get(self.base_url + "/bugrep/login/")
        driver.find_element_by_id("id_username").clear()
        driver.find_element_by_id("id_username").send_keys("admin")
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys("password")
        driver.find_element_by_css_selector("input.btn.btn-primary").click()
        # admin logged in
        driver.find_element_by_xpath(u"(//a[contains(text(),'" + ticket_title + "')])").click()
        driver.find_element_by_id("st_to_resolve").click()
        driver.find_element_by_css_selector("input.btn.btn-primary").click()
        # admin logout
        driver.find_element_by_xpath("//div[@id='helpdesk-nav-collapse']/ul/li[8]/a/span[2]").click()
        driver.find_element_by_link_text("Logout").click()
        
        # technician log in
        driver.find_element_by_id("id_username").clear()
        driver.find_element_by_id("id_username").send_keys("technik")
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys("password")
        driver.find_element_by_css_selector("input.btn.btn-primary").click()
        # technician take ticket
        driver.find_element_by_link_text(ticket_title).click()
        driver.find_element_by_css_selector("span.button.button_take").click()
        driver.find_element_by_id("st_checking").click()
        driver.find_element_by_id("commentBox").clear()
        driver.find_element_by_id("commentBox").send_keys(u"Vyřešeno")
        driver.find_element_by_id("logged_hours_id").clear()
        driver.find_element_by_id("logged_hours_id").send_keys("5")
        driver.find_element_by_css_selector("input.btn.btn-primary").click()
        # technician logout
        driver.find_element_by_xpath("//div[@id='helpdesk-nav-collapse']/ul/li[8]/a/span[2]").click()
        driver.find_element_by_link_text("Logout").click()
        # admin log in
        driver.find_element_by_id("id_username").clear()
        driver.find_element_by_id("id_username").send_keys("admin")
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys("password")
        driver.find_element_by_css_selector("input.btn.btn-primary").click()
        # admin check solution
        driver.find_element_by_xpath(u"(//a[contains(text(),'" + ticket_title + "')])").click()
        driver.find_element_by_id("st_closed").click()
        driver.find_element_by_id("commentBox").clear()
        driver.find_element_by_id("commentBox").send_keys(u"Zkontrolováno, OK.")
        driver.find_element_by_css_selector("input.btn.btn-primary").click()
        # admin log out
        driver.find_element_by_link_text("admin").click()
        driver.find_element_by_link_text("Logout").click()
    
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
