from rest_framework import serializers

from .models import Audio, Uploader


class UploaderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Uploader
        fields = '__all__'


class AudioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Audio
        fields = '__all__'
