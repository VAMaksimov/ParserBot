FROM python:3.12-alpine
WORKDIR /app

COPY requirements.txt .
# COPY bot.py .

RUN python -m venv venv
RUN source venv/bin/activate
RUN pip install -r requirements.txt

CMD ["python", "bot.py"]