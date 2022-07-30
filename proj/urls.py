from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework import routers
from image import views

router = routers.DefaultRouter()
router.register('url', views.UrlViewSet)
router.register('image', views.ImageViewSet)

urlpatterns = [
    path('v1/api/', include(router.urls), name='api'),
    path('', RedirectView.as_view(url='/v1/api/', permanent=False), name='index')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
