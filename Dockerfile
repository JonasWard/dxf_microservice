FROM python:3.9.2
#
## install environment dependencies
#RUN apt-get update -yqq \
#  && apt-get install -yqq --no-install-recommends \
#    netcat \
#  && apt-get -q clean
#
## set working directory
#RUN mkdir -p /usr/src/
#WORKDIR /usr/src/
#
## add requirements (to leverage Docker cache)
#ADD src/requirements.txt /usr/src/requirements.txt
#
## install requirements
#RUN pip install -r requirements.txt
#
## add entrypoint.sh
#ADD src/entrypoint.sh /usr/src/entrypoint.sh
#
## add app
#ADD src/reference /usr/src/
#
## run server
#CMD ["./entrypoint.sh"]
#
#
#

# MAINTANER JonasWard "ward@ugd.ai"

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

# set working directory
RUN mkdir -p /usr/src
WORKDIR /usr/src

# add requirements (to leverage Docker cache)
ADD /src /usr/src

# install requirements
RUN pip install -r /usr/src/requirements.txt

WORKDIR /usr/

CMD ["flask", "run", "--host", "1.1.1.1"]
EXPOSE 5000
ENTRYPOINT [ "python" ]
CMD [ "/usr/src/__init__.py" ]

"""python
import sys
sys.path.append("/usr")"""