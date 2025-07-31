FROM python:3.9
COPY bot.py
RUN pip install -r requests.txt
CMD ["python", "bot.py"]