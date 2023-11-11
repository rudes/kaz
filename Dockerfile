FROM python:3.11.6-alpine

WORKDIR /bot
ADD . /bot
RUN pip install --disable-pip-version-check -q -r requirements.txt

ENTRYPOINT [ "python", "bot.py" ]
