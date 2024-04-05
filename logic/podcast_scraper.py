from time import sleep

from libs.web_scraping import WebScraping


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

    def __get_podcast__(self) -> str:
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
            "podcast_title": "ppjs__podcast-title",
            "container": ".pod-content__list.episode-list .episode-list__wrapper",
        }

        # Load url
        self.set_page(url)

        # Wait till page loads
        sleep(5)

        # Load podcast's content
        self.__load_files__()

        print("Loaded")

    def __load_files__(self) -> None:
        """Show all hidden items."""

        selectors = {
            "container": ".episode-list__wrapper",
            "load_button": ".episode-list__load-more",
        }

        # TODO add condictionals and logic
        while True:
            self.click(selectors["load_button"])

    def extract_podcast(self):
        """Extracts podcast data"""

        podcasts = len(self.urls)
        print("Extracting", podcasts, "podcasts")

        while self.urls:

            # Set podcast's url
            url = self.__get_podcast__()

            # Loop and extract content
            self.__loop_podcast__(url)
