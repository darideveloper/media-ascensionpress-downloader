from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from tqdm import tqdm

from libs import WebScraping


class PodcastScraper(WebScraping):
    def __init__(self, headless: bool, urls: list) -> None:
        """Starts Chrome and initializes the WebScraping class.

        Args:
            headless: (bool, optional) if true the browser will
            not be shown. Defaults to False.

            urls: (list) podcast urls from the podcast.csv file.
        """

        # Start scraper
        super().__init__(
            headless=headless,
        )

        # Control variables
        self.header_removed = False

        # Urls
        self.urls = urls

        # Store data
        self.extracted_data: dict = {}

    def __get_podcast__(self):
        """Extract a URL

        Returns: (str) podcast url.
        """

        # Get first value from the list
        url = self.urls[0]

        # Remove the readed value
        self.urls.pop(0)

        return url

    def __loop_podcast__(self, url) -> None:
        """Loop through one podcast and extract its content

        Args: (str) podcast's url.
        """

        # CSS selectors
        selectors = {
            "contents": ".episode-list__entry",
            "podcast_title": "ppjs__podcast-title",
            "title": ".pod-entry__title",
            "description": ".ppjs__excerpt-content",
            "date_published": ".pod-entry__date",
            "mp3_link": ".ppshare-item.download .ppshare__download",
        }

        # Load url
        self.set_page(url)

        # Wait till page loads
        sleep(5)

        # Load podcast's content
        # self.__load_files__()

        # Extract data
        contents = self.get_elems(selectors["contents"])
        elems = tqdm(range(len(contents)))

        for num in elems:
            title = self.get_text(contents[num], selectors["title"])

            sleep(0.3)
            elems.set_description(f"Extracting {title}")

            date_published = self.get_text(contents[num], selectors["date_published"])

            contents[num].click()

            sleep(3)

            description = self.get_text(selectors["description"])

            mp3_link = self.get_attrib("href", selectors["mp3_link"])

    def __load_files__(self) -> None:
        """Show all hidden items."""

        selectors = {
            "load_button": ".episode-list__load-more",
        }

        # Load content loop
        while True:
            try:
                load_button = WebDriverWait(self.get_browser(), 10).until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, selectors["load_button"])
                    )
                )
                load_button.click()
                sleep(3)
            except Exception:
                break

    def extract_podcast(self):
        """Extracts podcast data"""

        podcasts = len(self.urls)
        print("Working on", podcasts, "podcasts ...")

        while self.urls:

            # Set podcast's url
            url = self.__get_podcast__()

            # Loop and extract content
            self.__loop_podcast__(url)
