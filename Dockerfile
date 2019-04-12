FROM python:3.6

WORKDIR /bot
ADD . /bot
RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "bot.py" ]
