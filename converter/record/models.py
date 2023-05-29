import mimetypes
import os.path
import uuid

import pydub
from django.db import models
from django.http import FileResponse

from .exceptions import FileConvertError, InvalidAudioFileFormat, InvalidUser
from .validators import validate_file_extension


class Uploader(models.Model):
    username = models.CharField(
        max_length=30,
        unique=True,
        db_index=True,
        null=False
        )
    user_id = models.AutoField(primary_key=True)
    user_token = models.CharField(
        max_length=50,
        default=uuid.uuid4,
        unique=True,
        editable=False
        )

    @classmethod
    def get_valid(cls, user_id, user_token):
        try:
            return cls.objects.get(user_id=user_id, user_token=user_token)
        except Uploader.DoesNotExist:
            raise InvalidUser

    def __str__(self):
        return self.username


class Audio(models.Model):
    audio_file = models.FileField(validators=[validate_file_extension])
    audio_token = models.CharField(
        max_length=50,
        default=uuid.uuid4,
        unique=True,
        editable=False
        )
    user_id = models.ForeignKey(
        Uploader,
        on_delete=models.CASCADE,
        related_name='audios',
    )

    def convert(self):
        file_type, _ = mimetypes.guess_type(self.audio_file.name)

        if file_type not in ('audio/wav', 'audio/x-wav'):
            raise InvalidAudioFileFormat(
                'Invalid audio file format (only .wav)')

        converted_filename, _ = os.path.splitext(self.audio_file.path)
        converted_filename = converted_filename + '.mp3'
        try:
            sound = pydub.AudioSegment.from_wav(self.audio_file.path)
            sound.export(converted_filename, format='mp3')

            converted_url = f'/record?id={self.id}&user={self.user_id_id}'
            return converted_url
        except IndexError as e:
            raise FileConvertError(str(e))

    def download(self):
        file, _ = os.path.splitext(self.audio_file.path)
        file = file + '.mp3'
        response = FileResponse(open(file, 'rb'))
        return response
