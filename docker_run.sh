IMAGE_NAME="parser-bot"
CONTAINER_NAME="internship-bot"

if [ "$(docker volume ls -q -f name=bot-data | wc -l)" -eq "0" ]; then
    echo "bot-data volume does not exist, creating"
    docker volume create bot-data
else
    echo "bot-data volume already exists, skipping creation"
fi

# TO DO: properly mount bot.py
docker run -d --name ${CONTAINER_NAME} \
  -v bot-data:/app \
  --mount type=bind,source=/host/path/to/bot.py,target=/app/bot.py \
  --restart unless-stopped \
  ${IMAGE_NAME}
