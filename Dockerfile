#base image
FROM python:3.7

LABEL Author="EssamFakher"

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONBUFFERED 1

# create root directory for our project in the container
RUN mkdir /shopping_system
# Set the working directory to /music_service
WORKDIR /shopping_system
# Copy the current directory contents into the container at /music_service
ADD . /shopping_system/
#let pip install required packages
RUN pip install -r requirements.txt
