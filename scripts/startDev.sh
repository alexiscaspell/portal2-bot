docker build -t portal2-bot .

docker run -it -v "$(pwd)/.env":"/usr/app/.env" portal2-bot