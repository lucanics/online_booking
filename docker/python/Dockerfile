FROM python:3.8

MAINTAINER lgwiedemann@gmail.com

COPY ./django_project /django_project2

WORKDIR /django_project2

RUN pip install -r requirements.txt

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]