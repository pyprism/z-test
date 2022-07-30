from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response

from image.models import URL, Image
from image.seriazliers import URLSerializer, ImageSerializer
from image.tasks import process_site_url


class UrlViewSet(viewsets.ModelViewSet):
    queryset = URL.objects.get_all_urls()
    serializer_class = URLSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            process_site_url.delay(serializer.data['url'], serializer.data['id'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Image.objects.get_all_image()
    serializer_class = ImageSerializer

    def list(self, request, *args, **kwargs):
        url = request.query_params.get('url')
        size = request.query_params.get('size')

        if url:
            queryset = Image.objects.get_image_by_url(url)
        else:
            queryset = self.get_queryset()

        serializer = self.get_serializer(queryset, many=True, context={'size': size, "request": request})
        return Response(serializer.data)


