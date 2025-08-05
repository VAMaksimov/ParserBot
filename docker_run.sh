IMAGE_NAME="parser-bot"
CONTAINER_NAME="internship-bot"

docker volume create bot-data

docker run -d --name ${CONTAINER_NAME} \
  -v bot-data:/app \
  -v bot.py:/app/bot.py \
  -v requirements.txt:app/requirements.txt \
  --restart unless-stopped \
  ${IMAGE_NAME}
