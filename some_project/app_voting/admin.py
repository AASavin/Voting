from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, reverse
from django.utils.html import format_html
from django.core.exceptions import PermissionDenied
from .models import Voting, Character, CharacterOnVoting
from .forms import VotingAdminForm
from .tasks import send_results


class CharacterOnVotingInline(admin.TabularInline):
    model = CharacterOnVoting
    min_num = 2
    fields = ['character']


@admin.register(Voting)
class VotingAdmin(admin.ModelAdmin):
    inlines = (CharacterOnVotingInline,)
    list_display = ['name', 'winner', 'voting_actions']
    list_select_related = ['winner']
    form = VotingAdminForm

    def get_urls(self):
        urls = super(VotingAdmin, self).get_urls()
        custom_urls = [
            path('<int:pk>/export', self.voting_export, name='voting_export')
        ]
        return custom_urls + urls

    def voting_actions(self, obj):
        return format_html(
            '<a class="button" href="{}" target="_blank">send</a>',
            reverse('admin:voting_export', args=[obj.pk])
        )

    voting_actions.short_description = 'send to email'
    voting_actions.allow_tags = False

    def voting_export(self, request, pk):
        if not request.user.has_perm('app_voting.view_voting') or not request.user.email:
            raise PermissionDenied
        send_results.delay(email=request.user.email, voting_id=pk)
        return HttpResponse('<h1>The xlsx file has been sent to your email</h1>')


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ['name', 'surname']

