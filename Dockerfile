FROM python:alpine3.12

WORKDIR /app

RUN apk add gcc

COPY ["requirements.txt", "./"]
RUN pip install -r requirements.txt

COPY ["*.py", "./"]

CMD ["python", "/app/KasaSender.py"]
