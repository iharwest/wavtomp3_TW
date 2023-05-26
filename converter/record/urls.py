from django.urls import path

from .views import AudioView, UploaderView

urlpatterns = [
    path('user/', UploaderView.as_view()),
    path('audio/', AudioView.as_view()),
]
