from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class MoviesPage(object):
    def __init__(self, driver):
        self.driver = driver
        self.url = 'https://www.themoviedb.org/movie/?language=en'
        self.movies_locator = (
            By.XPATH, '/html/body/div[1]/header/div[1]/div/div[1]/ul/li[1]/a')
        self.content_locator = (
            By.XPATH, '//div[@class="card style_1"]//div[@class="content"]')
        self.titles_locator = (
            By.XPATH, '//div/div[2]/h2/a')
        self.release_dates_locator = (
            By.XPATH, '//div/div[2]/p')
        self.user_scores_locator = (
            By.XPATH, '//div[@class="page_wrapper"]/div/div[2]/div/div/div/div/span')

    def open_page(self, option='Popular'):
        """
        Go to movie page depending on the option.
        option is set 'Popular' by default.

        Keyword arguments:
        option (string) - "Popular", "Now Playing", "Upcoming", "Top Rated"
        """
        driver = self.driver
        self.driver.get(self.url)

        movies_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                self.movies_locator
            )
        )
        movies_button.click()
        movies_option = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.LINK_TEXT, option)
            )
        )
        movies_option.click()

    def get_content(self, number=20):
        """
        Returns a list of dictionarys
        with the information about the movies.

        Limit the amount with the number parameter.

        Keyword arguments:
        number - A integer between 1 and 20

        Return:
        content_list (list)
        """
        driver = self.driver
        content_list = []

        content = WebDriverWait(driver, 10).until(
            EC.visibility_of_any_elements_located(
                self.content_locator
            )
        )

        for element in content:

            title = element.find_element(By.XPATH, "./h2").text or "No title"
            release_date = element.find_element(
                By.XPATH, "./p").text or "No release date"
            user_score = element.find_element(
                By.XPATH, "./div/div/div").get_attribute("data-percent") or "No rated"

            content_list.append(
                {
                    "title": title,
                    "release_date": release_date,
                    "user_score": user_score
                }
            )

        return content_list[:number]
