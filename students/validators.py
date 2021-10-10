import datetime

from django.core.exceptions import ValidationError


def no_elon_validator(email):
    if 'elon' in email.lower():
        raise ValidationError('No more Elons, please!')


def prohibited_domains(email):
    if email.endswith('@mail.ru') or email.endswith('@yandex.ru'):
        raise ValidationError('Such domain is not accepted. Please, use another email')


def older_than_18(birthdate):
    eighteen_years_ago = datetime.date.today() - datetime.timedelta(days=6570)  # 6570 days in 18 years
    if birthdate > eighteen_years_ago:
        raise ValidationError('A student cannot be younger than 18')
