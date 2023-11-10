FROM python:latest

RUN apt-get update -y && \
    apt-get install python3-opencv -y 

WORKDIR /home/src

COPY . ./

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

#linea para ejecutar en el terminarl
#docker build -t img_neumonia . 

CMD ["python", "neumonia/app.py"]
