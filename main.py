from fastapi import FastAPI
from github_handler import get_info, is_authenticated
import os

app = FastAPI()

@app.get("/")
async def home():
    return {"Data": "Test"} 


@app.get("/get-repos/{username}")
async def get_users_repos(username: str):
    user = os.environ.get('GITHUB_USERNAME')
    token = os.environ.get('ALLEGRO_SUMMER_EXPERIENCE_2022')

    return get_info(username, user, token)

@app.get("/authenticated")
async def authentication():
    return is_authenticated()