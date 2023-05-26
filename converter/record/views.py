import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Audio, Uploader
from .serializers import AudioSerializer, UploaderSerializer
from .utils import convert_audio


class UploaderView(APIView):

    def post(self, request):
        serializer = UploaderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        queryset = Uploader.objects.filter(username=request.data['username'])
        if not queryset.exists():
            serializer.save()
            response = queryset.values('user_id', 'user_token')
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AudioView(APIView):

    def post(self, request):
        user = Uploader.objects.filter(
                user_token=request.data['user_token'],
                user_id=request.data['user_id'],
                ).exists()
        if user:
            audio_mp3 = convert_audio(request.files['audio_file'])
            serializer = AudioSerializer(data=request.data, files=audio_mp3)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            audio_obj = Audio.objects.filter(
                user_id=serializer.data['user_id']).last()
            response = {'url': f'http://localhost:8000/record?id={audio_obj.id}&user={audio_obj.user_id}'}
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
