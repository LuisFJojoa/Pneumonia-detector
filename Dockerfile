FROM python:3.10.13

RUN apt-get update -y && \
    apt-get install python3-opencv -y  

WORKDIR /home/src

COPY ./pneumonia_detector ./pneumonia_detector

RUN pip install --upgrade pip
RUN pip install -r pneumonia_detector/requirements.txt

# Container cleaning to reduce size
RUN apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
