from rest_framework import serializers
from image.models import URL, Image
from sorl.thumbnail import get_thumbnail


class URLSerializer(serializers.ModelSerializer):
    class Meta:
        model = URL
        fields = '__all__'
        read_only_fields = ('id',)


class ImageSerializer(serializers.ModelSerializer):
    url = URLSerializer(read_only=True)

    class Meta:
        model = Image
        fields = '__all__'

    def __calculate_height_width(self, size, instance):
        height, width = 0, 0
        if size == 'small':
            width = 256
            height = instance.height / instance.width * width
        if size == "medium":
            width = 1024
            height = instance.height / instance.width * width
        if size == "large":
            width = 2048
            height = instance.height / instance.width * width
        return height, width

    def to_representation(self, instance):
        size = self.context.get('size')
        data = super().to_representation(instance)
        if size:
            height, width = self.__calculate_height_width(size, instance)

            if height < instance.height and height < instance.width:   # preventing upscale
                height = instance.height
                width = instance.width
                data['image'] = self.context['request'].build_absolute_uri(get_thumbnail(instance.image,
                                                                                         f'{width}x{height}').url)
                data['width'] = width
                data['height'] = height

        return data

