from pydantic import BaseSettings
import json


class Settings(BaseSettings):
    app_name: str = "Allegro Summer Experience 2022"
    author: str = "Marcin Jarczewski"
    admin_email: str = "marcin.jarc@gmail.com"

    user: str = None
    token: str = None


settings = Settings()


try:
    with open('credentials.json', 'r') as f:
        auth = json.load(f)
        settings.user = auth['user']
        settings.token = auth['token']
except Exception as err:
    pass
