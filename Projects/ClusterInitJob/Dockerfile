# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.7-alpine

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

RUN apk update && \
    apk add --virtual build-deps python-dev musl-dev && \
    apk add postgresql-dev && \
    apk add --update --no-cache gcc

# Install pip requirements
ADD requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
ADD . /app

# During debugging, this entry point will be overridden. For more information, refer to https://aka.ms/vscode-docker-python-debug
CMD ["python", "clusterInit.py"]