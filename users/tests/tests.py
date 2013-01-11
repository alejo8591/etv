# -*- coding: utf-8 -*-
from django.test import LiveServerTestCase, TestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from dajaxice.decorators import dajaxice_register

class RegisterFranchiseeTest(TestCase):
     
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(5)
        
    def tearDown(self):
        self.browser.close()
        self.browser.quit()
    
    @dajaxice_register(method='POST')
    def test_can_admin(self):
        self.browser.get('http://127.0.0.1:8000' + '/register/')
           
        self.assertIn("register", self.browser.title)
        
        user = self.browser.find_element_by_id("id_identification")
        user.send_keys("80912071")
        user.send_keys(Keys.RETURN)
        
        email = self.browser.find_element_by_id("id_email")
        email.send_keys("alejo8591@gmail.com")
        email.send_keys(Keys.RETURN)
        
        passwordOne = self.browser.find_element_by_id("id_passwordOne")
        passwordOne.send_keys("80912070")
        passwordOne.send_keys(Keys.RETURN)
        
        passwordTwo = self.browser.find_element_by_id("id_passwordTwo")
        passwordTwo.send_keys("80912070")
        passwordTwo.send_keys(Keys.RETURN)
        
        franchiseeCode = self.browser.find_element_by_id("id_franchiseeCode")
        franchiseeCode.send_keys("XXXXXXX")
        franchiseeCode.send_keys(Keys.RETURN)
        
        self.browser.find_element_by_id("buttonSend").click()