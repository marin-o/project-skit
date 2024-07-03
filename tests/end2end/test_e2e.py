import pytest
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

    @pytest.mark.parametrize("url_segment, model_name, expected_title", [
        ('/authors/', 'Author Name', 'Authors'),
        ('/publishers/', 'Publisher Name', 'Publishers'),
    ])
    def test_add_simple_entities(self, live_server, url_segment, model_name, expected_title):
        self.driver.get(f'{live_server.url}{url_segment}')

        assert expected_title in self.driver.title

        addlink = self.driver.find_element(By.PARTIAL_LINK_TEXT, 'Add')
        addlink.click()
        time.sleep(1)
        assert 'Add' in self.driver.title

        name = self.driver.find_element(By.NAME, 'name')
        name.send_keys(model_name)
        time.sleep(1)

        submit = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit.click()
        time.sleep(1)

        assert expected_title in self.driver.title
        assert model_name in self.driver.page_source

    def test_add_book(self, live_server, create_author, create_publisher):
        author_name = create_author().name
        publisher_name = create_publisher().name

        self.driver.get(f'{live_server.url}/books/')
        addlink = self.driver.find_element(By.PARTIAL_LINK_TEXT, 'Add')
        addlink.click()
        time.sleep(1)

        assert 'Add' in self.driver.title

        # Fill in the book form
        title_input = self.driver.find_element(By.ID, 'id_title')
        title_input.send_keys("Test Book Title")

        isbn10_input = self.driver.find_element(By.ID, 'id_isbn10')
        isbn10_input.send_keys("1234567890")

        isbn13_input = self.driver.find_element(By.ID, 'id_isbn13')
        isbn13_input.send_keys("1234567890123")

        pages_input = self.driver.find_element(By.ID, 'id_pages')
        pages_input.send_keys("300")

        description_input = self.driver.find_element(By.ID, 'id_description')
        description_input.send_keys("This is a test description.")

        price_input = self.driver.find_element(By.ID, 'id_price')
        price_input.send_keys("29.99")

        authors_select = self.driver.find_element(By.ID, 'id_authors')
        for option in authors_select.find_elements(By.TAG_NAME, 'option'):
            if option.text == author_name:
                wait = WebDriverWait(self.driver, 10)
                wait.until(EC.element_to_be_clickable(option))
                ActionChains(self.driver).move_to_element(option).click().perform()
                break

        publishers_select = self.driver.find_element(By.ID, 'id_publishers')
        for option in publishers_select.find_elements(By.TAG_NAME, 'option'):
            if option.text == publisher_name:
                wait = WebDriverWait(self.driver, 10)
                wait.until(EC.element_to_be_clickable(option))
                ActionChains(self.driver).move_to_element(option).click().perform()
                break

        submit = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.element_to_be_clickable(submit))
        time.sleep(1)
        ActionChains(self.driver).move_to_element(submit).click().perform()

        assert 'Books' in self.driver.title
        assert 'Test Book Title' in self.driver.page_source
