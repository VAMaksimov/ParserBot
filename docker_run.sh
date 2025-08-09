IMAGE_NAME="parser-bot"
CONTAINER_NAME="internship-bot"

if [ "$(docker volume ls -q -f name=bot-data | wc -l)" -eq "0" ]; then
    echo "bot-data volume does not exist, creating"
    docker volume create bot-data
else
    echo "bot-data volume already exists, skipping creation"
fi

docker run -d --name ${CONTAINER_NAME} \
  -v bot-data:/app \
  --mount type=bind,source=$(pwd)/bot.py,target=/app/bot.py \
  --restart unless-stopped \
  ${IMAGE_NAME}
