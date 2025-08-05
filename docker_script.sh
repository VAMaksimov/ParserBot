CONTAINER_NAME="parser-bot"

docker volume create bot-data

docker run -d --name internship-bot \
  -v bot-data:/app \
  -v bot.py:/app/bot.py \
  -v requirements.txt:app/requirements.txt \
  --restart unless-stopped \
  ${CONTAINER_NAME}
