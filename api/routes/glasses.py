from django.urls import path
from api.views import GlassesView

urlpatterns = [
    path("", GlassesView.as_view(), name="glasses_list"),
    path("<int:pk>/", GlassesView.as_view(), name="glasses_pk"),
]
