#use official python image
FROM python:3.9-slim-buster

#set wokring dir in containeer
WORKDIR /app

# copy req file
COPY requirements.txt .  

#install req files
RUN pip3 install --no-cache-dir -r requirements.txt

# copy application code to working dir
COPY . .

# set env var for flask app
ENV FLASK_RUN_HOST=0.0.0.0

# expose port where app run
EXPOSE 5000

# run docker file
CMD ["flask", "run"]