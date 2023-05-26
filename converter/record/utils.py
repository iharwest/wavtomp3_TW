import io
import mimetypes

import pydub
from rest_framework import status
from rest_framework.response import Response


def convert_audio(audio_file):
    file_type, _ = mimetypes.guess_type(audio_file.filename)
    if file_type not in ('audio/wav', 'audio/x-wav'):
        response = {'error': 'Invalid audio file format (only .wav)'}
        return Response(response, status=status.HTTP_406_NOT_ACCEPTABLE)
    audio = pydub.AudioSegment.from_audio_file(
        io.BytesIO((audio_file).file.read()),
        format='wav'
        )
    audio_mp3 = io.BytesIO()
    audio.export(audio_mp3, format='mp3')
    return audio_mp3.getvalue()
