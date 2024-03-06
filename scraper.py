"""
=============================
Camera Images Scraper
=============================

This script scrapes images from an URL.
Images should be stored in the format "camera_name/YYYY-MM-DD/timestamp.jpg".
For example, "kooks_fabriek_1/2024-02-21/1708528555.jpg"
Anothe example, "kooks_fabriek_2/2024-02-20/1708438684.jpg"

Parameters
----------
url : str
    URL of the image to download.
camera_name : str
    Name of the camera for directory structuring.

Examples
----------
Command-line usage example:
    $ python scraper.py http://username:password@root:port/image.jpg kooks_fabriek_1

Warnings
----------
Never put the camera URL in this file.
Never push the camera URL to the repository.
"""


import requests
import time
import os
from datetime import datetime
import argparse
from requests.auth import HTTPDigestAuth
from urllib.parse import urlparse


def get_credentials(url):
    """
    Extract the credentials from a URL.

    Parameters
    ----------
    url : str
        URL of the image to download.
    """
    parsed_url = urlparse(url)
    return parsed_url.username, parsed_url.password

def download_image(url, path, username, password):
    """
    Download an image from a URL and save it to a specified path.

    Parameters
    ----------
    url : str
        URL of the image to download.
    path : str
        The directory path to store the image.
    username : str
        The username extracted from the URL.
    password : str
        The password extracted from the URL.
    """
    try:
        if username and password: # Check whether we need credentials to access the URL
            response = requests.get(url, timeout=30, verify=False, auth=HTTPDigestAuth(username, password))
        else:
            response = requests.get(url, timeout=30, verify=False)
        with open(path, 'wb') as f:
            f.write(response.content)
        print(f"Image downloaded and saved to {path}")
    except requests.RequestException as e:
        print(f"Failed to download the image: {e}")


def main(url, camera_name):
    while True:
        # Get the current date and time
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        timestamp = int(now.timestamp())

        # Create the directory structure if it does not exist
        directory_path = os.path.join(camera_name, date_str)
        os.makedirs(directory_path, exist_ok=True)

        # Generate the full path for the new image file
        file_path = os.path.join(directory_path, f"{timestamp}.jpg")

        # Get the username and password from secure URL
        username, password = get_credentials(url)

        # Download the image
        download_image(url, file_path, username, password)

        # Wait for 5 seconds before downloading the next image
        time.sleep(5)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download images from a specified URL at intervals.")
    parser.add_argument("url", type=str, help="URL of the image to download")
    parser.add_argument("camera_name", type=str, help="Name of the camera for directory structuring")
    args = parser.parse_args()
    main(args.url, args.camera_name)