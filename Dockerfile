# # Указывает Docker использовать официальный образ python 3 с dockerhub в качестве базового образа
# FROM python:3
# # Устанавливает переменную окружения, которая гарантирует, что вывод из python будет отправлен прямо в терминал без предварительной буферизации
# ENV PYTHONUNBUFFERED 1
# # Устанавливает рабочий каталог контейнера — "app"
# WORKDIR /app
# # Копирует все файлы из нашего локального проекта в контейнер
# ADD . /app
# # Запускает команду pip install для всех библиотек, перечисленных в requirements.txt
# RUN pip install -r requirements.txt


# pull official base image
FROM python:3.8.3-alpine
# set work directory
WORKDIR /usr/src/app
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev
# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt
# copy entrypoint.sh
COPY ./entrypoint.sh .
# copy project
COPY . .
# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
