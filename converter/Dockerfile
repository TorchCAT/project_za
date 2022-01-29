FROM jrottenberg/ffmpeg:3.4.9-ubuntu1804
RUN apt update
RUN apt-get -y install python3.6 python3-pip
ENV LC_ALL=C.UTF-8 LANG=C.UTF-8
WORKDIR /app
COPY requirements.txt .
RUN /usr/bin/python3.6 -m pip install -r requirements.txt
COPY . .
ENTRYPOINT [""]
ENV FLASK_APP=converter.py
CMD ["flask", "run", "-p", "4000", "--host", "0.0.0.0"]
