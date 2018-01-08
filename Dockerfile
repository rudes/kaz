FROM python:3-onbuild

WORKDIR /bot
ADD . /bot

ENTRYPOINT [ "python", "bot.py" ]
