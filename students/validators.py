import datetime

from django.core.exceptions import ValidationError

YEARS_18_IN_DAYS = 365.2425 * 18
PROHIBITED = ['@mail.ru', '@yandex.ru']


def no_elon_validator(email):
    if 'elon' in email.lower():
        raise ValidationError('No more Elons, please!')


def prohibited_domains(email):
    if any([email.endswith(mail) for mail in PROHIBITED]):
        raise ValidationError('Such domain is not accepted. Please use another email domain')


def older_than_18(birthdate):
    eighteen_years_ago = datetime.date.today() - datetime.timedelta(days=YEARS_18_IN_DAYS)  # 6570 days in 18 years
    if birthdate > eighteen_years_ago:
        raise ValidationError('A student cannot be younger than 18')
