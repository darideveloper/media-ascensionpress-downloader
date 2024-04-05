from libs.web_scraping import WebScraping


class PodcastScraper(WebScraping):
    def __init__(self, headless: bool, urls: str) -> None:
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
        self.extracted_data = {}

    def podcast_urls(self) -> None:
        """Loop through a CSV and extract the links to use later
        Args:
            csv_urls: (csv) csv containing podcast links
        """
        print(self.urls)

    def extract_podcast(self):
        """Extracts podcast data"""
        pass
