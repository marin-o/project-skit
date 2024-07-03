import pytest
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


@pytest.mark.usefixtures('driver_init')
@pytest.mark.django_db
class TestChrome:
    """
    Test class for Chrome browser End-to-End testing.
    """

    def __find_and_click_element__(self, by=By.CSS_SELECTOR, selector="button[type='submit']"):
        """
        Find and click an element based on the provided method and selector string.

        Args:
            by (By): Method to locate the element.
            selector (str): The selector string to locate the element.
        """
        submit = self.driver.find_element(by, selector)
        wait = WebDriverWait(self.driver, 10)
        wait.until(ec.element_to_be_clickable(submit))
        ActionChains(self.driver).move_to_element(submit).click().perform()

    def test_navigation(self, live_server):
        """
        Test navigation through the application.

        Verifies:
        1. The 'Books' page loads correctly.
        2. Navigation through each link on the 'Books' page functions as expected.
        3. Each link leads to a page with the correct title.
        4. The 'Add' button on each page is present and functional.
        """

        # Arrange and Act
        self.driver.get(('%s%s' % (live_server.url, '/books/')))

        # Assert
        assert 'Books' in self.driver.title, "The title should contain 'Books'"

        # Arrange, Act, and Assert
        links = self.driver.find_elements(By.TAG_NAME, 'a')
        for i in range(1, len(links) - 1):
            text = links[i].text
            links[i].click()

            assert text in self.driver.title, f"The title should contain '{text}'"

            self.__find_and_click_element__(by=By.PARTIAL_LINK_TEXT, selector='Add')

            assert 'Add' in self.driver.title or 'Edit' in self.driver.title, "The title should contain 'Add' or 'Edit'"

            self.driver.back()

            links = self.driver.find_elements(By.TAG_NAME, 'a')

    @pytest.mark.parametrize("url_segment, model_name, expected_title", [
        ('/authors/', 'Author Name', 'Authors'),
        ('/publishers/', 'Publisher Name', 'Publishers'),
    ])
    def test_add_simple_entities(self, live_server, url_segment, model_name, expected_title):
        """
        Test adding simple entities like authors and publishers.

        Verifies that the entity is added and appears on the list page.

        Args:
            live_server: The live server fixture.
            url_segment (str): The URL segment for the entity.
            model_name (str): The name of the entity to be added.
            expected_title (str): The expected title of the page.
        """
        # Arrange
        self.driver.get(f'{live_server.url}{url_segment}')

        # Assert
        assert expected_title in self.driver.title, f"The title should contain '{expected_title}'"

        # Act
        self.__find_and_click_element__(by=By.PARTIAL_LINK_TEXT, selector='Add')

        # Assert
        assert 'Add' in self.driver.title, "The title should contain 'Add'"

        # Act
        name = self.driver.find_element(By.NAME, 'name')
        name.send_keys(model_name)

        self.__find_and_click_element__()

        # Assert
        assert expected_title in self.driver.title, f"The title should contain '{expected_title}'"
        assert model_name in self.driver.page_source, f"The page should contain '{model_name}'"

    def test_add_book(self, live_server, create_author, create_publisher):
        """
        Test adding a book with valid details and related entities.

        Verifies that the book is added and appears on the list page.

        Args:
            live_server: The live server fixture.
            create_author: Fixture to create an author.
            create_publisher: Fixture to create a publisher.
        """
        author_name = create_author().name
        publisher_name = create_publisher().name

        # Arrange
        self.driver.get(f'{live_server.url}/books/')
        self.__find_and_click_element__(by=By.PARTIAL_LINK_TEXT, selector='Add')

        # Assert
        assert 'Add' in self.driver.title, "The title should contain 'Add'"

        # Act
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

        # Assert
        assert 'Books' in self.driver.title, "The title should contain 'Books'"
        assert 'Test Book Title' in self.driver.page_source, "The page should contain 'Test Book Title'"

    @pytest.mark.parametrize("url_segment, create_entity_fixture, new_name, html_element_id", [
        ('/books/', 'create_book', 'Updated Book Title', 'id_title'),
        ('/authors/', 'create_author', 'Updated Author Name', 'id_name'),
        ('/publishers/', 'create_publisher', 'Updated Publisher Name', 'id_name'),
    ])
    def test_edit_entity(self, request, live_server, url_segment, create_entity_fixture, new_name, html_element_id):
        """
        Test editing an entity (book, author, or publisher).

        Verifies that the entity is updated and the changes are reflected on the list page.

        Args:
            request: The request fixture to get other fixtures.
            live_server: The live server fixture.
            url_segment (str): The URL segment for the entity.
            create_entity_fixture (str): The fixture to create the entity.
            new_name (str): The new name to be set.
            html_element_id (str): The HTML element ID for the name field.
        """
        entity = request.getfixturevalue(create_entity_fixture)()
        self.driver.get(f'{live_server.url}{url_segment}')

        # Act
        self.__find_and_click_element__(By.LINK_TEXT, 'Edit')

        # Assert
        assert 'Edit' in self.driver.title, "The title should contain 'Edit'"

        # Act
        input_element = self.driver.find_element(By.ID, html_element_id)
        input_element.clear()
        input_element.send_keys(new_name)
        self.__find_and_click_element__()

        # Assert
        assert url_segment.strip(
            '/').capitalize() in self.driver.title, f"The title should contain '{url_segment.strip('/').capitalize()}'"
        assert new_name in self.driver.page_source, f"The page should contain '{new_name}'"

    @pytest.mark.parametrize("entity_url, create_entity_fixture, entity_identifier_attribute", [
        ('/books/', 'create_book', 'title'),
        ('/authors/', 'create_author', 'name'),
        ('/publishers/', 'create_publisher', 'name'),
    ])
    def test_delete_entity(self, request, live_server, entity_url, create_entity_fixture, entity_identifier_attribute):
        """
        Test deleting an entity (book, author, or publisher).

        Verifies that the entity is deleted and no longer appears on the list page.

        Args:
            request: The request fixture to get other fixtures.
            live_server: The live server fixture.
            entity_url (str): The URL segment for the entity.
            create_entity_fixture (str): The fixture to create the entity.
            entity_identifier_attribute (str): The attribute to identify the entity.
        """
        entity = request.getfixturevalue(create_entity_fixture)()
        entity_attr_value = getattr(entity, entity_identifier_attribute)

        # Arrange
        self.driver.get(f'{live_server.url}{entity_url}')

        # Act
        self.__find_and_click_element__(By.LINK_TEXT, 'Delete')

        self.__find_and_click_element__()

        # Assert
        assert entity_attr_value not in self.driver.page_source, f"The page should not contain '{entity_attr_value}'"
