FROM python:3.9-buster
ENV BOT_NAME=$BOT_NAME

ADD . /usr/src/app/"${BOT_NAME:-tg_bot}"
WORKDIR /usr/src/app/"${BOT_NAME:-tg_bot}"
RUN pip install -r requirements.txt

CMD ["echo", "hello"]