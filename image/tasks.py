from celery import shared_task

from proj import settings
from .models import Image, URL
from .utils import get_image_urls, download_image, save_images


@shared_task
def process_site_url(site_url, site_id):
    """
    Scraps all images from a site and saves them to the database
    """
    print(site_url)
    images = get_image_urls(site_url)
    locations = download_image(images)
    save_images(site_id, locations)


