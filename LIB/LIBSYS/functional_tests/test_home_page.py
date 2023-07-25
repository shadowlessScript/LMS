from selenium import webdriver
from LIBSYS.models import AddBook
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
import time
from selenium.webdriver.common.by import By

class TestHomePage(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome('functional_tests/chromedriver.exe')
    
    def tearDown(self):
        self.browser.close()
    
    def test_no_home_page(self):
        self.browser.get(self.live_server_url)
        
        # First view of the home page without announcements

        alert = self.browser.find_element(By.CLASS_NAME,'welcome-bg')
        self.assertEquals(
            alert.text,
            "WELCOME TO THE ONLINE  LIBRARY MANAGEMENT SYSTEM. Where knowlegde is shared."
        )