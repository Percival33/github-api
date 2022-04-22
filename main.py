from fastapi import FastAPI
from github_handler import get_info, get_repos, is_authenticated
import os

app = FastAPI()

@app.get("/")
async def home():
    return {"Data": "Test"} 


@app.get("/authenticated")
async def authentication():
    user = os.environ.get('GITHUB_USERNAME')
    token = os.environ.get('ALLEGRO_SUMMER_EXPERIENCE_2022')
    return is_authenticated(user, token)


@app.get("/get-repos/{username}")
async def get_user_repos(username: str):
    user = os.environ.get('GITHUB_USERNAME')
    token = os.environ.get('ALLEGRO_SUMMER_EXPERIENCE_2022')

    return get_repos(username, user, token)


@app.get("/get-info/{username}")
async def get_user_info(username: str):
    user = os.environ.get('GITHUB_USERNAME')
    token = os.environ.get('ALLEGRO_SUMMER_EXPERIENCE_2022')

    return get_info(username, user, token)