FROM pytorch/pytorch@sha256:8711d55e2b5c42f3c070e1f2bacc2d1988c9b3b5b99694abc6691a852536efbe

RUN apt-get update
#RUN apt-get install ffmpeg libsm6 libxext6  -y

ADD /requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

ADD /src /docker_project/src/
ADD /cfgs /docker_project/cfgs/

WORKDIR /docker_project/
ENTRYPOINT ["python3", "-u", "/docker.py"]