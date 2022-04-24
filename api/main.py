from fastapi import FastAPI
from github_handler import GithubHandler
from models.authentication import Authentication
from config import settings
from typing import Optional

app = FastAPI()
github_handler = GithubHandler()

@app.get("/")
def home():
    return {
        "response": "/",
        "meta": {
            "limit": 0,
            "remaining": 0,
            "reset": 0,
            "used": 0,
        }
    }


@app.get("/api/info")
def info():
    return {
        "response": 
        {
            "Possible endpoints:": [
                "GET  /",
                "GET  /api/get-repos/{username}",
                "GET  /api/get-info/{username}",
                "GET  /api/info",
                "GET  /api/about"
            ]
        },
        "meta": {
            "limit": 0,
            "remaining": 0,
            "reset": 0,
            "used": 0,
        }
    }
        

@app.get("/api/get-repos/{username}")
def get_user_repos(username: str):
    auth = None
    
    if settings.auth is not None:
        auth = settings.auth

    return github_handler.get_repos(username, auth)


@app.get("/api/get-info/{username}")
def get_user_info(username: str):
    auth = None

    if settings.auth is not None:
        auth = settings.auth
        
    return github_handler.get_info(username, auth)


@app.get("/api/about")
def about():
    return {
        "app_name": settings.app_name,
        "created_by": settings.author,
        "admin_email": settings.admin_email,
        "meta": {
            "limit": 0,
            "remaining": 0,
            "reset": 0,
            "used": 0,
        }
    }
