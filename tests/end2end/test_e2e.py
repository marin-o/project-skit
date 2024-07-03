import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


@pytest.mark.usefixtures('driver_init')
@pytest.mark.django_db
class TestChromeAndFirefox:
    def test_navigation(self, live_server):
        self.driver.get(('%s%s' % (live_server.url, '/books/')))

        assert 'Books' in self.driver.title

        links = self.driver.find_elements(By.TAG_NAME, 'a')
        for i in range(1, len(links)-1):
            text = links[i].text
            links[i].click()
            time.sleep(1)

            assert text in self.driver.title

            links = self.driver.find_elements(By.TAG_NAME, 'a')

            addlink = self.driver.find_element(By.PARTIAL_LINK_TEXT, 'Add')
            addlink.click()
            time.sleep(1)

            assert 'Add' in self.driver.title or 'Edit' in self.driver.title

            self.driver.back()
            time.sleep(1)

            links = self.driver.find_elements(By.TAG_NAME, 'a')
