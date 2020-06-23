FROM python:alpine3.7
COPY templates /var/
COPY application.py /var
COPY dynamodb.py /var
COPY requirements.txt /var
WORKDIR /var
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["application.py"]