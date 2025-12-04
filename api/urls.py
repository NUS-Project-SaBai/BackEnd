from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from sabaibiometrics.settings import OFFLINE, MEDIA_ROOT, MEDIA_URL
from django.conf.urls.static import static


urlpatterns = [
    path("test/", include(("api.routes.test", "test"))),
    path("medication/", include(("api.routes.medication", "medication"))),
    path("patients/", include(("api.routes.patients", "patients"))),
    path("visits/", include(("api.routes.visits", "visits"))),
    path("vitals/", include(("api.routes.vitals", "vitals"))),
    path("users/", include(("api.routes.users", "users"))),
    path("consults/", include(("api.routes.consults", "consults"))),
    path("diagnosis/", include(("api.routes.diagnosis", "diagnosis"))),
    path("orders/", include(("api.routes.orders", "orders"))),
    path(
        "medication_review/",
        include(("api.routes.medication_review", "medication_review")),
    ),
    path("files/", include(("api.routes.files", "files"))),
    path("glasses/", include(("api.routes.glasses", "glasses"))),
    path("referrals/", include(("api.routes.referrals", "referrals"))),
    path("villages/", include(("api.routes.villages", "villages"))),
    # CUSTOM ENDPOINTS
    path(
        "patient_records/", include(("api.routes.patient_records", "patient_records"))
    ),
    path(
        "pharmacy_orders/", include(("api.routes.pharmacy_orders", "pharmacy_orders"))
    ),
    path(
        "medication_history/",
        include(("api.routes.medication_history", "medication_history")),
    ),
    path(
        "patient_consult/", include(("api.routes.patient_consult", "patient_consult"))
    ),
    path("vision/", include(("api.routes.patient_vision", "patient_vision"))),
    path("login/", include(("api.routes.login", "login"))),
]

if OFFLINE:
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)
