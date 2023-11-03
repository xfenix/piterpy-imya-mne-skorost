ARG USERNAME=benchmark-user
ARG USER_UID=2000
ARG USER_GID=$USER_UID
ARG WORKDIR=/srv/www/

FROM python:3.12-slim as builder
ARG USERNAME
ARG USER_UID
ARG USER_GID
ARG WORKDIR
WORKDIR $WORKDIR
RUN groupadd --gid $USER_GID $USERNAME
RUN useradd --uid $USER_UID --gid $USER_GID -m $USERNAME
COPY poetry.lock .
COPY pyproject.toml .
RUN apt-get update && apt-get install gcc -y
RUN pip install --no-cache-dir poetry
RUN poetry config virtualenvs.create false
RUN poetry install --compile
RUN rm poetry.lock
RUN poetry cache clear pypi --all
RUN pip uninstall -y poetry pip setuptools
RUN apt-get remove -y gcc
RUN apt-get clean autoclean
RUN apt-get autoremove -y
RUN rm -rf /var/lib/{apt,dpkg,cache,log}/
RUN rm -rf /var/lib/apt/lists/*

FROM scratch as runtime
ARG USERNAME
ARG WORKDIR
WORKDIR $WORKDIR
COPY --from=builder / /
COPY . $WORKDIR
USER $USERNAME
# CMD ["uvicorn", "app:MAIN_APP", "--host", "0.0.0.0", "--port", "80"]
CMD ["gunicorn", "app:MAIN_APP", "--workers", "8", "--worker-class", "uvicorn.workers.UvicornWorker",\
     "--bind", "0.0.0.0:80"]
