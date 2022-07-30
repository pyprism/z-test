from django.db import models


class URLManager(models.Manager):
    def get_all_urls(self):
        return self.order_by("-id")


class URL(models.Model):
    url = models.URLField(max_length=2048)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = URLManager()

    def __str__(self):
        return self.url


class ImageManager(models.Manager):
    def create_image(self, site_id, image_location, width, height):
        url = URL.objects.filter(id=site_id).first()
        image = self.create(url=url, image=image_location, width=width, height=height)
        return image

    def get_all_image(self):
        return self.select_related('url').order_by("-id")

    def get_image_by_url(self, url):
        url_obj = URL.objects.filter(url=url).first()
        return self.select_related('url').filter(url=url_obj).order_by("-id")


class Image(models.Model):
    url = models.ForeignKey(URL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ImageManager()

    def __str__(self):
        return self.image.url
