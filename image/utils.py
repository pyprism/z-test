import os

import requests
from bs4 import BeautifulSoup
from django.conf import settings
from django.core.files import File
from PIL import Image as PILImage
from .models import Image


def get_image_urls(site_url):
    """
    Get all image urls from a site
    returns a list of image urls
    """
    response = requests.get(site_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        image_urls = []
        for img in soup.find_all('img'):
            if img.get('src').startswith('http') and "jpg" in img.get('src'):   # filtering base64 images and jpg images
                image_urls.append(img.get('src'))
        return image_urls
    return []


def download_image(urls):
    """
    Download and save image to filesystem
    returns a list of image locations
    """
    locations = []
    for url in urls:
        response = requests.get(url)
        if response.status_code == 200:
            image_name = url.split('/')[-1]
            image_location = f'{settings.MEDIA_ROOT }/{image_name}'
            with open(image_location, 'wb') as f:
                f.write(response.content)
            locations.append(image_location)
    return locations


def get_image_size(location):
    with PILImage.open(location) as img:
        return img.size[0], img.size[1]


def save_images(url_obj_id, image_locations):
    """
    Save images to database
    """
    for location in image_locations:
        width, height = get_image_size(location)
        with open(location, 'rb') as fi:
            Image.objects.create_image(url_obj_id, File(fi, name=os.path.basename(fi.name)), width, height)


