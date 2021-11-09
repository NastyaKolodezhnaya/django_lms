# generating objects of model Student - not actual
#
#
# from django.core.management import BaseCommand
# from faker import Faker
# from students.models import Student
#
#
# class Command(BaseCommand):
#     help = 'generate objects of class <Student>, add it to "students_student" database'
#
#     def handle(self, *args, **kwargs):
#         count = int(args[0])
#         faker = Faker()
#         for _ in range(count):
#             instance = Student(
#                 first_name=faker.first_name(),
#                 last_name=faker.last_name(),
#                 email=faker.email(),
#                 birthdate=faker.date_time_between(start_date='-30y', end_date='-18y'))
#             instance.save()
#
#     def add_arguments(self, parser):
#         parser.add_argument(
#             nargs='+',
#             type=int,
#             dest='args'
#         )
