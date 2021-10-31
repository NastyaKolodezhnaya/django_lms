import datetime
import uuid

from faker import Faker

from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator
# from phonenumber_field.modelfields import PhoneNumberField


from students.validators import no_elon_validator, prohibited_domains, older_than_18


class Person(models.Model):
    first_name = models.CharField(
        max_length=60, null=False, validators=[MinLengthValidator(2)]
    )
    last_name = models.CharField(
        max_length=80, null=False, validators=[MinLengthValidator(2)]
    )
    email = models.EmailField(max_length=120, null=True,
                              blank=True, validators=[no_elon_validator, prohibited_domains])

    phone_number = models.CharField(
        null=True, max_length=14, unique=True,
        blank=True, validators=[RegexValidator("\d{10,14}")]
    )

    # phone_number = PhoneNumberField(unique=True, null=True)

    class Meta:
        abstract = True  # no Person table to create


class Student(Person):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    birthdate = models.DateField(null=True, blank=True, default=datetime.date.today, validators=[older_than_18])

    avatar = models.ImageField(upload_to='media', null=True,
                               blank=True)
    resume = models.FileField(upload_to='static', null=True,
                              blank=True)

    course = models.ForeignKey(
        "students.Course", null=True, blank=True, related_name="student_course", on_delete=models.SET_NULL
    )

    def __str__(self):
        return f"{self.full_name()}, {self.age()}, {self.email} ({self.id})"

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def age(self):
        if self.birthdate:
            return datetime.datetime.now().year - self.birthdate.year
        return 'Enter a valid birthdate, please!'

    @classmethod
    def generate_instances(cls, count):
        faker = Faker()
        for _ in range(count):
            st = cls(
                first_name=faker.first_name(),
                last_name=faker.last_name(),
                email=faker.email(),
                birthdate=faker.date_time_between(start_date="-30y",
                                                  end_date="-18y")
            )
            st.save()


class Course(models.Model):
    id = models.UUIDField(primary_key=True, unique=True,
                          default=uuid.uuid4,
                          editable=False)
    name = models.CharField(null=False, max_length=100)
    start_date = models.DateField(null=True, default=datetime.date.today())
    count_of_students = models.IntegerField(default=0)
    room = models.ForeignKey(
        "students.Room", null=True, blank=True, related_name="courses", on_delete=models.SET_NULL
    )

    def __str__(self):
        return f"{self.name}"


class Teacher(Person):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ManyToManyField(to="students.Course", related_name="teacher_course")

    def __str__(self):
        return f"{self.first_name} {self.last_name}, ({self.id})"


class Room(models.Model):
    location = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
    color = models.ForeignKey("students.Color", null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.location}, {self.color}"


class Color(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"


class Invitations(models.Model):
    # 1st option
    # id = models.UUIDField(primary_key=True, unique=True,
    #                       default=uuid.uuid4,
    #                       editable=False)
    # old_student_id = models.ForeignKey("students.Student", null=False, blank=False,
    #                                    related_name="inviter", on_delete=models.RESTRICT)
    # new_student_id = models.OneToOneField("students.Student", null=False, blank=False,
    #                                       related_name='invitee', on_delete=models.RESTRICT)
    #
    # & add 'count' field to Student model depending on the count of Invitations records with student's id

    # 2nd option
    old_student = models.ForeignKey("students.Student", null=False, blank=False, related_name="inviter",
                                    on_delete=models.RESTRICT)
    count = models.IntegerField(default=0)
