from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Allegro Summer Experience 2022"
    author: str = "Marcin Jarczewski"
    admin_email: str = "marcin.jarc@gmail.com"

    user: str = None
    token: str = None

settings = Settings()