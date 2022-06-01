from rest_framework import serializers
from .models import Voting, CharacterOnVoting, Character


class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ['surname', 'name', 'patronymic', 'photo', 'age', 'biography']


class CharacterOnVotingSerializer(serializers.ModelSerializer):
    character = CharacterSerializer(read_only=True)

    class Meta:
        model = CharacterOnVoting
        fields = ['id', 'votes', 'character']


class VotingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voting
        fields = ['id', 'name']


class VotingDetailSerializer(serializers.ModelSerializer):
    characters = CharacterOnVotingSerializer(many=True, read_only=True)
    winner = CharacterSerializer(read_only=True)

    class Meta:
        model = Voting
        fields = ['id', 'name', 'start_date', 'end_date', 'max_votes', 'is_active', 'winner', 'characters']


class VotingParticipantsSerializer(serializers.ModelSerializer):
    characters = CharacterOnVotingSerializer(many=True, read_only=True)

    class Meta:
        model = Voting
        fields = ['id', 'name', 'characters']


class VotingWinnersListSerializer(serializers.ModelSerializer):
    winner = CharacterSerializer(read_only=True)

    class Meta:
        model = Voting
        fields = ['id', 'name', 'winner']
