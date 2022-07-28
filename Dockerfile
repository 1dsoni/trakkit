FROM python:3.9-buster
# copy src code
RUN mkdir /code
WORKDIR /code/

# just copy the requirements file and install
ADD requirements.txt /code/requirements.txt
# installing project requirements
RUN pip install -r requirements.txt
# add the rest of code
ADD . /code/
# makes sure logs are not missing when system crashes
ENV PYTHONUNBUFFERED 1
EXPOSE 8000
CMD ["/code/runner.sh"]
