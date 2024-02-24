# Fetch Rss App

## Overview
Fetch Rss is a Python application that fetches RSS feeds and extracts relevant information using BeautifulSoup (bs4). It is designed to be run in a Docker environment for easy setup and deployment.

## Version
Version: 0.1.0

## Requirements
- Docker: [Download Docker](https://docs.docker.com/get-docker/)
- Docker Compose: [Download Docker Compose](https://docs.docker.com/compose/install/)

## Installation
1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/MADITIS/rss-fetch-py.git
   cd rss-fetch-py

2.  ```mv sample.env .env```

3. Open the `.env` file in a text editor and fill in the following values:
   ```plaintext
   api_id = your_api_id
   api_hash = "your_api_hash"
   bot_token = "your_bot_token"
   owner_id = your_id #optional
   group_id = group_id_to_send_rss
    ```

    - Follow the [instructions](https://core.telegram.org/api/obtaining_api_id) to create ```api_id``` & ```api_hash```.
    - Get the ```bot_token``` from [Botfather](https://t.me/BotFather) by creating a new bot.

4. Run the app
    ```bash
    docker-compose up
    ```


## Note
This app is still in its early stages, so it's a bit basic for now. Right now, it can only grab RSS feeds from one URL.

