# use base image
FROM bitnami/python:3.10-prod

# set working directory
WORKDIR /app

#COPY src{upto txt}  dest
COPY server/app.py server/requirements.txt /app/

# install dependencies from requirements.txt
RUN pip install -r requirements.txt

# 5000 port exposed for external connection 
EXPOSE 5000

# execute command python app.py to run the file
CMD  ["python", "app.py"]