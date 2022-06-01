from some_project.celery import app
from datetime import datetime
from . import models
from .utils import create_results_xlsx, send


@app.task
def activate_voting(voting_id):
    """Makes voting active when the start date arrives"""
    voting = models.Voting.objects.get(id=voting_id)
    if voting.start_date <= datetime.now().date() and not voting.winner:
        voting.is_active = True
        voting.save()


@app.task
def deactivate_voting(voting_id):
    """Completes the voting after the time has elapsed"""
    voting = models.Voting.objects.get(id=voting_id)
    if voting.end_date <= datetime.now().date() and not voting.winner:
        winner = voting.characters.order_by('-votes').first().character
        voting.winner = winner
        voting.is_active = False
        voting.save()


@app.task
def send_results(email, voting_id):
    """Sends the voting results to email"""
    voting = models.Voting.objects.get(id=voting_id)
    file_path = create_results_xlsx(voting)
    send(user_email=email, name=voting.name, file_path=file_path)
