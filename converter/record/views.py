from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .exceptions import FileConvertError, InvalidAudioFileFormat, InvalidUser
from .models import Audio, Uploader
from .serializers import AudioSerializer, UploaderSerializer


class UploaderView(ViewSet):
    serializer_class = UploaderSerializer

    def create(self, request):
        serializer = UploaderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {
            "id": serializer.data['user_id'],
            "user_token": serializer.data['user_token']}
        return Response(response, status=status.HTTP_201_CREATED)


class AudioView(ViewSet):
    serializer_class = AudioSerializer

    def create(self, request):
        user_id = request.data.get('user_id', 0)
        user_token = request.META.get('HTTP_X_USER_TOKEN', "")

        try:
            Uploader.get_valid(user_id, user_token)
        except InvalidUser:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = AudioSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        audio = serializer.save()

        try:
            url = audio.convert()
            return Response(
                {'url': request.build_absolute_uri(url)},
                status=status.HTTP_201_CREATED)
        except InvalidAudioFileFormat as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_406_NOT_ACCEPTABLE)
        except FileConvertError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RecordView(ViewSet):
    serializer_class = AudioSerializer

    def get(self, request):
        id = request.GET.get('id')
        user_id = request.GET.get('user')
        audio = Audio.objects.filter(id=id, user_id=user_id)
        if not audio:
            response = {'error': 'Audio not found'}
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        obj = Audio.objects.get(id=id, user_id=user_id)
        response = obj.download()
        return response
