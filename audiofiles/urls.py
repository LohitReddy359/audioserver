from django.urls import include, path
from .views import audio_post, audio_list, download_file, audio_info
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path(r'api/post/', audio_post),
    path(r'api/list/', audio_list),
    path(r'api/download/', download_file),
    path(r'api/info/', audio_info),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)