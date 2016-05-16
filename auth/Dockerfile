FROM atmoscape/pythonflask:latest

# run python in unbuffered mode so we get logs instantly
ENV PYTHONUNBUFFERED 1

# postgres environment variables

# lets make a working directory
RUN mkdir /code

# and use it
WORKDIR /code

# add all files in project directory to '/code/' on container
ADD ./app/ /code/app/
# ADD ./migrations/* /code/migrations/
ADD ./tests/ /code/tests/
ADD ./*.py /code/