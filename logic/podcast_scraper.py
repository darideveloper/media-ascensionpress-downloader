from libs import WebScraping


class PodcastScraper(WebScraping):
    def __init__(self, headless: bool):
        """Starts Chrome and initializes the WebScraping class.
        Args:
            headless: (bool, optional): if true the browser will
            not be shown. Defaults to False.
        """

        # Start scraper
        super().__init__(
            headless=headless,
        )

        # Control variables
        self.header_removed = False

        # Store data
        self.extracted_data = {}

    def extract_podcast(self):
        """Extracts podcast data from the website."""
