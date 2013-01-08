# -*- coding: utf-8 -*-
from django.test import LiveServerTestCase, TestCase
from selenium import webdriver


class AdminTest(TestCase):
     
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        
    def test_can_admin(self):
        self.browser.get('http://127.0.0.1:8000' + '/register/')
        
        self.assertIn("registe", self.browser.title)
        
        #self.fail('finish this error for admin site')
        
    def tearDown(self):
        self.browser.quit()