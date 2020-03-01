FROM node:alpine as nodejs
WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
COPY teleagh/frontend/package.json package.json
RUN npm install
COPY teleagh/frontend .
RUN npm run build

# pull official base image
FROM python:3.7-slim

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PORT=8000

# set work directory
WORKDIR /app

# install dependencies
ADD requirements.txt .
RUN pip install -r requirements.txt
ADD . ./
RUN python manage.py collectstatic --noinput
CMD ["./entrypoint.sh"]
