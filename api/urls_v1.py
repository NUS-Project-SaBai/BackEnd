from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from sabaibiometrics.settings import OFFLINE, MEDIA_ROOT, MEDIA_URL
from django.conf.urls.static import static


urlpatterns = [
    path("", include(("api.routes.patient_records", "patient_records"))),
]

if OFFLINE:
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)
