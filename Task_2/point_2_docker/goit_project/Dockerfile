FROM python:3.11

WORKDIR /app

COPY requirements.txt /app

RUN pip3 install -r requirements.txt

COPY . /app

EXPOSE 8000

ENV NAME Test_Bot


ENTRYPOINT ["python", "goit_project/main.py"]