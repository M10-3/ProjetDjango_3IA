from django.urls import path
from .views import*

urlpatterns = [
    path('list/', conferencesList, name="listConf"),
    path('listViewConf/', ConferenceListView.as_view(), name="listViewConf"),
    path('details/<int:pk>/', DetailsViewConference.as_view(), name="detailConf"),
]