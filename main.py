from fastapi import FastAPI, Response, status
from http import HTTPStatus
from github_handler import get_info, get_repos, is_authenticated
from models import Auth
from typing import Optional
from config import settings

app = FastAPI()


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
                "GET  /api/authenticated", 
                "POST /api/auth",
                "GET  /api/logout",
                "GET  /api/get-repos/{username}",
                "GET  /api/get-info/{username}",
                "GET  /api/info"
            ]
        },
        "meta": {
            "limit": 0,
            "remaining": 0,
            "reset": 0,
            "used": 0,
        }
    }
        

@app.get("/api/is_auth")
def is_authentication(response: Response):
    res, meta = is_authenticated(settings.user, settings.token)
    if res:
        return {
            "response": "User is authenticated",
            "meta": meta
        }

    if int(meta["remaining"]) == 0:
        response.status_code = status.HTTP_403_FORBIDDEN
        return {
            "response": "Github API rate limit exceeded",
            "meta": meta
        }

    response.status_code = status.HTTP_401_UNAUTHORIZED
    return {
        "response": "Requires authentication",
        "meta": meta
    }


@app.post("/api/auth")
def get_authenticated(response: Response, auth: Optional[Auth] = None):
    settings.user = settings.token = None

    if auth is None:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {
            "response": "Requires authentication",
            "meta": {
                "limit": 0,
                "remaining": 0,
                "reset": 0,
                "used": 0
            }
        }

    res, meta = is_authenticated(auth.user, auth.token)

    if res:
        settings.user = auth.user
        settings.token = auth.token
        return {
            "response": "User authenticated successfully",
            "meta": meta
        }
    
    response.status_code = status.HTTP_401_UNAUTHORIZED
    return {
        "response": "Bad credentials",
        "meta": meta
    }


@app.get("/api/logout")
def logout():
    if settings.user is not None and settings.token is not None:
        settings.user = settings.token = None
        return {
            "response": "Logged out successfully", 
            "meta": {
                "limit": 0,
                "remaining": 0,
                "reset": 0,
                "used": 0,
            }
        }

    return Response(status_code=HTTPStatus.NOT_MODIFIED.value)


@app.get("/api/get-repos/{username}")
def get_user_repos(username: str, response: Response):
    res, response.status_code = get_repos(username, settings.user, settings.token)
   
    return res


@app.get("/api/get-info/{username}")
def get_user_info(username: str, response: Response):
    res, response.status_code = get_info(username, settings.user, settings.token)

    return res


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
