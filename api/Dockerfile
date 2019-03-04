FROM alpine:3.7
RUN mkdir /app
RUN apk add --no-cache python3
RUN pip3 install --upgrade pip
COPY requirements.txt /app/
RUN pip3 install --quiet -r /app/requirements.txt
COPY *.py /app/
WORKDIR /app
EXPOSE 52000
ENTRYPOINT ["gunicorn", "--bind=0.0.0.0:52000", "main:api"]

