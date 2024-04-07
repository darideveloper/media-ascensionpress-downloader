import csv
import os
import re
from time import sleep

import requests
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

    def __create_csv__(self) -> None:
        """Create a CSV file if it doesn't exist and write headers."""
        csv_file = "podcasts_content.csv"

        # Define csv headers
        headers = [
            "podcast_title",
            "date",
            "title",
            "description",
            "mp3_filename",
            "mp3_link",
        ]

        # Checks if csv already exists
        file_exists = os.path.isfile(csv_file)

        # Open csv in ('a') mode
        with open(csv_file, mode="a", newline="", encoding="utf-8") as file:
            # Create csv file writer
            writer = csv.writer(file)

            # Write headers only if csv file doesn't exists
            if not file_exists:
                writer.writerow(headers)

    def __save_csv__(self, data: list) -> None:
        """Write data to the CSV file.

        Args: (list) data The data to write to the CSV.
        """
        csv_file = "podcasts_content.csv"

        # Open csv in ('a') mode
        with open(csv_file, mode="a", newline="", encoding="utf-8") as file:
            # Create csv file writer
            writer = csv.writer(file)

            # Write data to CSV
            writer.writerow(data)

    def __create_folder__(self, folder_name: str) -> str:
        """Creates a folder with the specified folder inside .podcast/.

        Args:
            foldername: (str) the specified folder name.
        """
        folder_name = re.sub(r"\s+", "_", folder_name)
        folder_name = re.sub(r"[^\w\s]", "", folder_name)

        if not os.path.exists(os.path.join("podcast/", folder_name)):
            os.makedirs(os.path.join("podcast/", folder_name))

        folder_path = os.path.join("podcast", folder_name)

        return folder_path

    def __save_file__(self, folder_name: str, file_name: str, url: str) -> str:
        """Save a file in the specified destiny

        Args:
            folder_name: (str) folder path.

            file_name: (str) the desired name for the file.

            url: (str) url from the file to be downloaded.
        """
        file_name = re.sub(r"\s+", "_", file_name)
        file_name = re.sub(r"[^\w\s]", "", file_name)

        # Adds the .mp3 extension
        if not file_name.endswith(".mp3"):
            file_name += ".mp3"

        response = requests.get(url)

        if response.status_code == 200:
            # Create file path
            file_path = os.path.join(folder_name, file_name)

            # Save file
            with open(file_path, "wb") as f:
                f.write(response.content)

        return file_name

    def __get_podcast__(self) -> None:
        """Extract a URL

        Returns: (str) podcast url.
        """

        # Get first value from the list
        url = self.urls[0]

        # Remove the readed value
        self.urls.pop(0)

        return url

    def __loop_podcast__(self, url: str) -> None:
        """Loop through one podcast and extract its content

        Args: (str) podcast's url.
        """

        # CSS selectors
        selectors = {
            "podcast_title": "h1, h1 > span",
            "contents": ".episode-list__entry",
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
        self.__load_files__()

        # Extract podcast's name
        folder_name = self.get_text(selectors["podcast_title"])

        print("Extracting", folder_name, "...\n")

        # Extract data
        contents = self.get_elems(selectors["contents"])
        elems = tqdm(range(len(contents)))

        # Create a folder to store podcast's content
        folder_path = self.__create_folder__(folder_name)

        for num in elems:
            title = self.get_text(contents[num], selectors["title"])

            sleep(0.3)
            elems.set_description(f"Extracting {title}")

            date_published = self.get_text(contents[num], selectors["date_published"])

            contents[num].click()

            sleep(3)

            description = self.get_text(selectors["description"])

            mp3_link = self.get_attrib("href", selectors["mp3_link"])

            # Download mp3
            mp3_filename = self.__save_file__(folder_path, title, mp3_link)

            # Data to write to CSV
            data = [
                folder_name,
                date_published,
                title,
                description,
                mp3_filename,
                mp3_link,
            ]

            # Call the function to write data to CSV
            self.__save_csv__(data)

        print("\n")

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

    def extract_podcast(self) -> None:
        """Extracts podcast data"""

        podcasts = len(self.urls)
        print("Working on", podcasts, "podcasts ...\n")

        while self.urls:

            # Set podcast's url
            url = self.__get_podcast__()

            # Loop and extract content
            self.__loop_podcast__(url)
