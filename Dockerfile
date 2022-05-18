FROM python:3.10

WORKDIR /lms_project

COPY . /lms_project

EXPOSE 3000


RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt


RUN python ./manage.py makemigrations
RUN python ./manage.py migrate
RUN python ./manage.py check

RUN python ./manage.py loaddata db_lms.json

RUN flake8


CMD ["python", "./manage.py", "runserver"]