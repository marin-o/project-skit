import pytest
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time


@pytest.mark.usefixtures('driver_init')
@pytest.mark.django_db
class TestChrome:

    def __find_and_click_element__(self, by=By.CSS_SELECTOR, selector="button[type='submit']"):
        submit = self.driver.find_element(by, selector)
        wait = WebDriverWait(self.driver, 10)
        wait.until(ec.element_to_be_clickable(submit))
        ActionChains(self.driver).move_to_element(submit).click().perform()

    def test_navigation(self, live_server):
        self.driver.get(('%s%s' % (live_server.url, '/books/')))

        assert 'Books' in self.driver.title

        links = self.driver.find_elements(By.TAG_NAME, 'a')
        for i in range(1, len(links) - 1):
            text = links[i].text
            links[i].click()

            assert text in self.driver.title

            links = self.driver.find_elements(By.TAG_NAME, 'a')

            self.__find_and_click_element__(by=By.PARTIAL_LINK_TEXT, selector='Add')

            assert 'Add' in self.driver.title or 'Edit' in self.driver.title

            self.driver.back()

            links = self.driver.find_elements(By.TAG_NAME, 'a')

    @pytest.mark.parametrize("url_segment, model_name, expected_title", [
        ('/authors/', 'Author Name', 'Authors'),
        ('/publishers/', 'Publisher Name', 'Publishers'),
    ])
    def test_add_simple_entities(self, live_server, url_segment, model_name, expected_title):
        self.driver.get(f'{live_server.url}{url_segment}')

        assert expected_title in self.driver.title

        self.__find_and_click_element__(by=By.PARTIAL_LINK_TEXT, selector='Add')

        assert 'Add' in self.driver.title

        name = self.driver.find_element(By.NAME, 'name')
        name.send_keys(model_name)

        self.__find_and_click_element__()

        assert expected_title in self.driver.title
        assert model_name in self.driver.page_source

    def test_add_book(self, live_server, create_author, create_publisher):
        author_name = create_author().name
        publisher_name = create_publisher().name

        self.driver.get(f'{live_server.url}/books/')
        self.__find_and_click_element__(by=By.PARTIAL_LINK_TEXT, selector='Add')

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
                wait.until(ec.element_to_be_clickable(option))
                ActionChains(self.driver).move_to_element(option).click().perform()
                break

        publishers_select = self.driver.find_element(By.ID, 'id_publishers')
        for option in publishers_select.find_elements(By.TAG_NAME, 'option'):
            if option.text == publisher_name:
                wait = WebDriverWait(self.driver, 10)
                wait.until(ec.element_to_be_clickable(option))
                ActionChains(self.driver).move_to_element(option).click().perform()
                break

        self.__find_and_click_element__()

        assert 'Books' in self.driver.title
        assert 'Test Book Title' in self.driver.page_source

    @pytest.mark.parametrize("url_segment, create_entity_fixture, new_name, html_element_id", [
        ('/books/', 'create_book', 'Updated Book Title', 'id_title'),
        ('/authors/', 'create_author', 'Updated Author Name', 'id_name'),
        ('/publishers/', 'create_publisher', 'Updated Publisher Name', 'id_name'),
    ])
    def test_edit_entity(self, request, live_server, url_segment, create_entity_fixture, new_name, html_element_id):
        entity = request.getfixturevalue(create_entity_fixture)()
        self.driver.get(f'{live_server.url}{url_segment}')
        self.__find_and_click_element__(By.LINK_TEXT, 'Edit')
        assert 'Edit' in self.driver.title

        input = self.driver.find_element(By.ID, html_element_id)
        input.clear()
        input.send_keys(new_name)
        self.__find_and_click_element__()

        assert url_segment.strip('/').capitalize() in self.driver.title
        assert new_name in self.driver.page_source

    @pytest.mark.parametrize("entity_url, create_entity_fixture, entity_identifier_attribute", [
        ('/books/', 'create_book', 'title'),
        ('/authors/', 'create_author', 'name'),
        ('/publishers/', 'create_publisher', 'name'),
    ])
    def test_delete_entity(self, request, live_server, entity_url, create_entity_fixture, entity_identifier_attribute):
        entity = request.getfixturevalue(create_entity_fixture)()
        entity_attr_value = getattr(entity, entity_identifier_attribute)

        self.driver.get(f'{live_server.url}{entity_url}')

        self.__find_and_click_element__(By.LINK_TEXT, 'Delete')

        self.__find_and_click_element__()

        assert entity_attr_value not in self.driver.page_source
