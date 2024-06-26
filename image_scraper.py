import requests
from bs4 import BeautifulSoup
import os

URL = 'https://mausam.imd.gov.in/imd_latest/contents/satellite.php'

# Directory to save the downloaded image
SAVE_DIR = 'images'

def download_image(url, save_path):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"Image successfully downloaded: {save_path}")
    else:
        print("Failed to retrieve the image")

def find_image_url(soup):
    # Find the div with id 'images'
    image_div = soup.find('div', id='images')
    if image_div:
        # Find the first image tag within this div
        image_tag = image_div.find('img')
        if image_tag and 'src' in image_tag.attrs:
            return image_tag['src']
    return None

def main():
    # Fetch the website content
    response = requests.get(URL)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        image_url = find_image_url(soup)
        
        if image_url:
            # If the image URL is relative, convert it to absolute
            if not image_url.startswith(('http://', 'https://')):
                image_url = requests.compat.urljoin(URL, image_url)
            
            # Ensure the save directory exists
            if not os.path.exists(SAVE_DIR):
                os.makedirs(SAVE_DIR)
            
            # Extract the image file name from the URL
            image_name = os.path.basename(image_url)
            save_path = os.path.join(SAVE_DIR, image_name)
            
            # Download the image
            download_image(image_url, save_path)
        else:
            print("No image found on the page")
    else:
        print(f"Failed to retrieve the web page. Status code: {response.status_code}")


main()
