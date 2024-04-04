import os

from dotenv import load_dotenv

from logic import PodcastScraper

# Env variables
load_dotenv()
HEADLESS = os.getenv("SHOW_BROWSER") != "True"


if __name__ == "__name__":
    # Initialize scraper
    podcast_scraper = PodcastScraper(HEADLESS)

    # Extract podcast from specified category
    podcast_scraper.extract_podcast()
