# lets use python v 2.7 for now since the tutorial says to
FROM python:2.7

# run python in unbuffered mode so we get logs instantly
ENV PYTHONUNBUFFERED 1

# postgres environment variables

# lets make a working directory
RUN mkdir /code

# and use it
WORKDIR /code

# add all files in project directory to '/code/' on container
ADD ./web/requirements.txt /code/

# install python requirements
RUN pip install -r requirements.txt