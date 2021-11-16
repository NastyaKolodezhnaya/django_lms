from django.db import models
import uuid
from faker import Faker
from django.core.validators import MinLengthValidator, RegexValidator


# Create your models here.
class Person(models.Model):
    first_name = models.CharField(
        max_length=60, null=False, validators=[MinLengthValidator(2)]
    )
    last_name = models.CharField(
        max_length=80, null=False, validators=[MinLengthValidator(2)]
    )
    email = models.EmailField(max_length=120, null=True,
                              blank=True)

    phone_number = models.CharField(
        null=True, max_length=14, unique=True,
        blank=True, validators=[RegexValidator("\d{10,14}")]
    )

    class Meta:
        abstract = True  # no Person table to create


class Teacher(Person):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ManyToManyField(to="courses.Course", related_name="teacher_course")

    def __str__(self):
        return f"{self.first_name} {self.last_name}, ({self.id})"

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
                phone_number=f'+380{faker.msisdn()[3:]}'
            )
            st.save()
