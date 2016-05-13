FROM python:latest

# run python in unbuffered mode so we get logs instantly
ENV PYTHONUNBUFFERED 1

# postgres environment variables

# lets make a working directory
RUN mkdir /code

# and use it
WORKDIR /code

# add all files in project directory to '/code/' on container
ADD ./requirements.txt /code/
ADD ./app/ /code/app/
ADD ./migrations/ /code/migrations/
ADD ./tests/ /code/tests/
ADD ./*.py /code/

# install python requirements
RUN pip install --upgrade pip
RUN pip install -r requirements.txt