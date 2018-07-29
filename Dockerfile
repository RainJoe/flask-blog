FROM python:3.6

ENV FLASK_APP blog.py
ENV FLASK_CONFIG production
ENV FLASK_USER admin
ENV FLASK_USER_EMAIL 'email@example.com'
ENV FLASK_USER_PASSWORD '123456'

RUN adduser --disabled-login blog
USER blog

WORKDIR /home/blog

COPY .pip .pip
COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt

COPY app app
COPY migrations migrations
COPY blog.py config.py boot.sh ./

# run-time configuration
EXPOSE 5000
ENTRYPOINT ["./boot.sh"]