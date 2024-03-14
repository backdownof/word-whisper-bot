FROM python:3.11-slim-bullseye

EXPOSE 6123

WORKDIR /app

COPY requirements.txt ./

RUN apt-get update
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]
