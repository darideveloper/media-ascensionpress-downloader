import os
from dotenv import load_dotenv
from logic import PodcastScraper

# Read .env's configuration
load_dotenv()
HEADLESS = os.getenv("SHOW_BROWSER") != "True"

# Read podcast's CSV
current_folder = os.path.dirname(__file__)
podcast_csv = os.path.join(current_folder, "podcast.csv")

# Create file if it doesn't exist
if not os.path.exists(podcast_csv):
    with open(podcast_csv, "w") as urls:
        urls.write("")

with open(podcast_csv, "r") as urls:
    URLS = [url.strip() for url in urls.readlines() if url.strip()]

if __name__ == "__main__":
    # Initialize scraper
    podcast_scraper = PodcastScraper(HEADLESS, URLS)

    # Extract podcast
    podcast_scraper.extract_podcast()
