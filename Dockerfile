FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY thai_massage_bot.py imghdr.py ./

CMD ["python", "-u", "thai_massage_bot.py"]
