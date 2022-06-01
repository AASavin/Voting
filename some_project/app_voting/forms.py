from django.forms.models import ModelForm
from django.forms import ValidationError
from .models import Voting


class VotingAdminForm(ModelForm):
    class Meta:
        model = Voting
        fields = ['name', 'start_date', 'end_date', 'max_votes']

    def clean_end_date(self):
        start_date = self.cleaned_data['start_date']
        end_date = self.cleaned_data['end_date']
        if end_date <= start_date:
            raise ValidationError(message='start date must be less than end date')
        return end_date
