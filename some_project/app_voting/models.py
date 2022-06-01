from django.db import models
from .tasks import activate_voting, deactivate_voting


class Voting(models.Model):
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    max_votes = models.PositiveIntegerField()
    is_active = models.BooleanField(default=False)
    winner = models.ForeignKey('Character', on_delete=models.CASCADE, blank=True, null=True)

    __original_start_date = None
    __original_end_date = None

    def __init__(self, *args, **kwargs):
        super(Voting, self).__init__(*args, **kwargs)
        self.__original_start_date = self.start_date
        self.__original_end_date = self.end_date

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Voting, self).save(*args, **kwargs)
        if self.start_date != self.__original_start_date:
            activate_voting.apply_async(args=[self.id], eta=self.start_date)
            self.__original_start_date = self.start_date
        if self.end_date != self.__original_end_date:
            deactivate_voting.apply_async(args=[self.id], eta=self.end_date)
            self.__original_end_date = self.end_date


class Character(models.Model):
    surname = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    patronymic = models.CharField(max_length=30, blank=True, null=True)
    photo = models.ImageField(upload_to='characters/', blank=True, null=True)
    age = models.PositiveIntegerField()
    biography = models.TextField()

    def __str__(self):
        return f'{self.surname} {self.name}'


class CharacterOnVoting(models.Model):
    voting = models.ForeignKey(Voting, on_delete=models.CASCADE, related_name='characters')
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    votes = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'app_voting_voting_characters'
