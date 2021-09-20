# init a base image (Alpine is small Linux distro)
FROM python:3.9.2-alpine
# define the present working directory
WORKDIR /docker-dxf-microservice
# copy the contents into the working dir
ADD . /docker-dxf-microservice
# run pip to install the dependencies of the flask app
RUN pip install -r requirements.txt
# define the command to start the container
CMD ["python","simple_server.py"]