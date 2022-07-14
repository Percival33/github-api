from pydantic import BaseSettings
from .models.authentication import Authentication
import json
import os


def get_credentials():
    auth = Authentication()

    absolute_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(absolute_path, "credentials.json")

    try:
        with open(file_path, "r") as f:
            credentials = json.load(f)
            auth.user = credentials["user"]
            auth.token = credentials["token"]
    except Exception:
        auth = None
    finally:
        return auth


class Settings(BaseSettings):
    app_name: str = "Github API"
    author: str = "Marcin Jarczewski"
    admin_email: str = "admin@domain.com"

    auth: Authentication = get_credentials()
