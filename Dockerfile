FROM python:3.11-alpine

EXPOSE 6123

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

USER engvocab

CMD ["python", "main.py"]
