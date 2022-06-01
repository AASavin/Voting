from django.core.mail import EmailMessage
import xlsxwriter
import os


def create_results_xlsx(voting):
    """Creates a results file in xls format"""
    characters = voting.characters.all().order_by('-votes').prefetch_related('character')
    file_path = f'media/results/results{voting.id}.xlsx'
    xlsx_file = xlsxwriter.Workbook(file_path)
    worksheet = xlsx_file.add_worksheet()
    worksheet.merge_range('A1:D2', voting.name)
    worksheet.write('E1', 'status')
    if voting.is_active:
        worksheet.write('E2', 'active')
    elif voting.winner:
        worksheet.write('E2', 'finished')
    else:
        worksheet.write('E2', 'not started yet')
    titles = ['id', 'name', 'surname', 'votes']
    worksheet.write_row('A3', titles)
    for i, character in enumerate(characters, start=4):
        character_data = [
            character.character.id,
            character.character.name,
            character.character.surname,
            character.votes
        ]
        worksheet.write_row(f'A{i}', character_data)
    xlsx_file.close()
    return file_path


def send(user_email, name, file_path):
    """Sends an email with file"""
    message = EmailMessage(
        'Voting results',
        f'Voting results for {name}',
        os.getenv('EMAIL_HOST_USER'),
        [user_email],
    )
    message.attach_file(file_path)
    message.send()
