# syntax = docker/dockerfile:1.2
FROM node:12.13.1-slim as frontend-dev
WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
COPY ["passit/frontend/package.json", "passit/frontend/package-lock.json", "./"]
RUN --mount=type=cache,target=/root/.npm npm install
COPY passit/frontend .
CMD npm run start

FROM node:12.13.1-slim as frontend-builder
WORKDIR /app
COPY --from=frontend-dev /app ./
RUN npm run build

FROM alpine as frontend-build
WORKDIR /app
COPY --from=frontend-builder /app/build ./build
COPY --from=frontend-builder /app/config ./config

FROM python:3.7-slim as backend

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PORT=8000
WORKDIR /app

ADD requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt
ADD . ./
CMD ["./entrypoint.sh"]

FROM backend as production
COPY --from=frontend-build /app/build ./passit/frontend/build
COPY --from=frontend-build /app/config ./passit/frontend/config
RUN python manage.py collectstatic --noinput
