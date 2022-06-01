from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F
from .models import Voting, CharacterOnVoting
from . import serializers


class VotingListAPIView(ListAPIView):
    """Getting a list of votes"""
    serializer_class = serializers.VotingListSerializer

    def get_queryset(self):
        queryset = Voting.objects.all()
        is_active = self.request.query_params.get('is_active')
        if is_active == 'True':
            queryset = queryset.filter(is_active=True)
        elif is_active == 'False':
            queryset = queryset.filter(is_active=False)
        return queryset


class VotingDetailAPIView(RetrieveAPIView):
    """Getting detailed information about voting"""
    serializer_class = serializers.VotingDetailSerializer
    queryset = Voting.objects.all().prefetch_related('characters__character')


class VotingParticipantsAPIView(RetrieveAPIView):
    """Getting voting participants"""
    serializer_class = serializers.VotingParticipantsSerializer
    queryset = Voting.objects.all().prefetch_related('characters__character')


class VotingWinnersListAPIView(ListAPIView):
    """Getting winners"""
    serializer_class = serializers.VotingWinnersListSerializer

    def get_queryset(self):
        queryset = Voting.objects.exclude(winner__isnull=True).select_related('winner')
        return queryset


class VoteAPIView(APIView):
    """increasing the number of votes"""
    def get(self, request, pk):
        try:
            character = CharacterOnVoting.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response('Character not found')
        if character.voting.is_active:
            if character.votes + 1 >= character.voting.max_votes:
                character.voting.is_active = False
                character.voting.winner = character.character
                character.voting.save()
            character.votes = F('votes') + 1
            character.save()
            return Response('Ok')
        return Response('Voting is not active')

