from django.urls import path
from . import api


urlpatterns = [
    path('list/', api.VotingListAPIView.as_view()),
    path('detail/<int:pk>', api.VotingDetailAPIView.as_view()),
    path('participants/<int:pk>', api.VotingParticipantsAPIView.as_view()),
    path('winners/', api.VotingWinnersListAPIView.as_view()),
    path('vote/<int:pk>', api.VoteAPIView.as_view())
]
