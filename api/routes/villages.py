from django.urls import path
from api.views import VillageView

urlpatterns = [
    path("", VillageView.as_view(), name="village_list"),
    path("<int:pk>/", VillageView.as_view(), name="village_pk"),
]