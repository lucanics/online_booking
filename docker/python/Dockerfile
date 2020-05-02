FROM python:3.8

MAINTAINER lgwiedemann@gmail.com

COPY ./django_project /django_project

WORKDIR /django_project

RUN pip install -r requirements.txt

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]