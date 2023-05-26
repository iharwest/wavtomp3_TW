import uuid

from django.db import models


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

    def __str__(self):
        return self.username


class Audio(models.Model):
    audio_file = models.FileField(upload_to="record/")
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
