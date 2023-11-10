FROM python:3.10.13

RUN apt-get update

WORKDIR /home/src

COPY . ./

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Container cleaning to reduce size
RUN apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

#Command to execute in terminal
#docker build -t pneumonia_detector . 

# CMD ["python", "pneumonia_detector/main.py"]
