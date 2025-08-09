# ParserBot info

Performed actions:
```
pip freeze > requirements.txt
./docker_build.sh
./docker_run.sh
crontab -e
```

crontab options:
```
0 8 * * * docker exec internship-bot python /app/bot.py check
0 20 * * * docker exec internship-bot python /app/bot.py check
```

manual check:
```
docker run --rm -v bot-data:/app --mount type=bind,source=$(pwd)/bot.py,target=/app/bot.py telegram-internship-bot python /app/bot.py check
```

options for debug:
```
docker logs internship-bot --details
```