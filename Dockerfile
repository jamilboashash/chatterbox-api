FROM ubuntu:18.04

RUN apt-get update -y
RUN apt-get install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get install python3.9 -y
RUN apt-get install python3-pip -y
RUN apt-get install python3.9-dev -y
RUN apt-get install python3.9-venv -y
RUN apt-get install build-essential -y
#RUN #apt-get install git -y

WORKDIR /home/chatterbox
ADD . /home/chatterbox

RUN python3.9 -m venv venv
RUN source venv/bin/activate
RUN pip install -r requirements.txt
#CMD ["python3.9","main.py"]

#ENV PATH=/home/chatterbox:$PATH
