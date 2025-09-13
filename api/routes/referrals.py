from django.urls import path
from api.views import ReferralView

urlpatterns = [
    path("", ReferralView.as_view(), name="referrals_list"),
    path("<int:pk>/", ReferralView.as_view(), name="referrals_pk"),
]
