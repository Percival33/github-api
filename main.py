from fastapi import FastAPI, HTTPException, Response, status
from http import HTTPStatus
from github_handler import get_info, get_repos, is_authenticated
from models import Auth
from typing import Optional
from config import settings

app = FastAPI()

@app.get("/")
def home():
    return {"response": "/"}

@app.get("/api/info")
def info():
    return {
        "response": 
        {
            "Possible endpoints:" : [
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
        return {"response": "User is authenticated",
                "meta": meta
                }

    response.status_code = status.HTTP_401_UNAUTHORIZED
    return {"response": "Requires authentication",
            "meta": meta
    }


@app.post("/api/auth")
def get_authenticated(auth: Optional[Auth] = None):
    settings.user = settings.token = None

    if auth is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Requires authentication")
    
    res, meta = is_authenticated(auth.user, auth.token)

    if res:
        settings.user = auth.user
        settings.token = auth.token
        return {
            "response": "User authenticated successfully",
            "meta": meta
        }
    
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Bad credentials")

@app.get("/api/logout")
def logout(response: Response):
    res, meta = is_authenticated(settings.user, settings.token)
    if res:
        settings.user = settings.token = None
        return {"response": "Logged out successfully", "meta": meta}

    return Response(status_code=HTTPStatus.NOT_MODIFIED.value)

@app.get("/api/get-repos/{username}")
def get_user_repos(username: str):
    return get_repos(username, settings.user, settings.token)


@app.get("/api/get-info/{username}")
def get_user_info(username: str):
    return get_info(username, settings.user, settings.token)

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