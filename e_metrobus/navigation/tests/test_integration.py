
import time
from selenium import webdriver

from django.shortcuts import reverse
from django.test import LiveServerTestCase, tag


SLEEP_TIME = 2


class SeleniumTestCase(LiveServerTestCase):
    """
    A base test case for Selenium, providing helper methods for generating
    clients and logging in profiles.
    """

    def setUp(self):
        self.selenium = webdriver.Firefox()
        super(SeleniumTestCase, self).setUpClass()

    def tearDown(self):
        self.selenium.quit()
        super(SeleniumTestCase, self).tearDown()

    def open(self, url):
        self.selenium.get("%s%s" % (self.live_server_url, url))


@tag("integration")
class DiversTestCase(SeleniumTestCase):
    def test_route(self):
        self.open(reverse("navigation:landing_page"))
    # def test_login_manually(self):
    #     # Login:
    #     self.open(reverse("stundenapp:index"))
    #     self.selenium.find_element_by_id("id_username").send_keys(USER)
    #     self.selenium.find_element_by_id("id_password").send_keys(self.password)
    #     self.selenium.find_element_by_css_selector("button.btn").click()
    #
    # def test_check_month(self):
    #     self.login()
    #     self.open(reverse("stundenapp:index"))
    #
    #     # Check month selection:
    #     time.sleep(SLEEP_TIME)
    #     while self.selenium.find_element_by_id("current_month").text != "2019 Oktober":
    #         self.selenium.find_element_by_id("previous_month").click()
    #     self.open(f"{reverse('stundenapp:index')}?date=2017-01-01")
