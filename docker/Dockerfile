FROM python:3.11-slim-buster

WORKDIR /code

RUN apt-get update \
    && apt-get install -y build-essential libpq-dev \
    && apt-get install -y libxml2-dev libxslt1-dev libz-dev \
    && apt-get install -y inotify-tools \
    && pip install --upgrade pip \
    && python --version

# Set user and group
ARG user=appuser
ARG uid=1000
ARG gid=1000
RUN groupadd -g ${gid} ${user}
RUN useradd -u ${uid} -g ${user} -s /bin/sh -m ${user} # <--- the '-m' create a user home directory

COPY --chown=${user}:${user} requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Switch to user
USER ${user}

COPY . /code


EXPOSE 80

ENTRYPOINT ["sh", "/code/docker/entrypoint.sh"]
