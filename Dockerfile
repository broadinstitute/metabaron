FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD metabaron /code/
ADD manage.py /code/
ADD scripts /code/

COPY /code/scripts/entrypoint.sh /code/
COPY /code/scripts/start.sh /code/

RUN chmod +x /code/start.sh
RUN chmod +x /code/entrypoint.sh

ENTRYPOINT ["/code/entrypoint.sh"]