from pydantic import BaseSettings
from models.authentication import Authentication
import json


class Settings(BaseSettings):
    app_name: str = "Allegro Summer Experience 2022"
    author: str = "Marcin Jarczewski"
    admin_email: str = "marcin.jarc@gmail.com"

    auth: Authentication = None


settings = Settings()


try:
    with open('credentials.json', 'r') as f:
        credentials = json.load(f)
        settings.auth = Authentication()
        settings.auth.user = credentials['user']
        settings.auth.token = credentials['token']
except Exception as err:
    pass
