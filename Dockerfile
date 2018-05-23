FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
COPY . /code/
RUN pip install -r /code/requirements.txt

RUN cp /code/scripts/entrypoint.sh /code/
RUN cp /code/scripts/start.sh /code/
RUN cp /code/scripts/gunicorn_start.sh /code/

RUN chmod +x /code/start.sh
RUN chmod +x /code/entrypoint.sh
RUN chmod +x /code/gunicorn_start.sh

#RUN apt-get update && apt-get install -y gunicorn
WORKDIR /code
CMD ["/code/entrypoint.sh"]