from django.urls import path

from .views import AudioView, RecordView, UploaderView

urlpatterns = [
    path('user/', UploaderView.as_view({'post': 'create'})),
    path('audio/', AudioView.as_view({'post': 'create'})),
    path('record', RecordView.as_view({'get': 'get'}))
]
