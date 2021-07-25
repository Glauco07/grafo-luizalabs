FROM python:3.9

WORKDIR /usr/src/app

RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

COPY ./ /usr/src/app/

EXPOSE 5000

EXPOSE 8080
EXPOSE 9080
EXPOSE 8000

ENTRYPOINT ["python"]
CMD ["run.py"]
