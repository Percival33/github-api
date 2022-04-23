from fastapi import FastAPI, HTTPException, Response, status
from http import HTTPStatus
from github_handler import get_info, get_repos, is_authenticated
from models import Auth
from typing import Optional
from config import settings

app = FastAPI()

@app.get('/')
def home():
    return {"response": "/"}

@app.get("/info")
def info():
    return {"response": 
    {
        "Possible endpoints:" : [
            "GET  /",
            "GET  /authenticated", 
            "POST /auth",
            "GET  /logout",
            "GET  /get-repos/{username}",
            "GET  /get-info/{username}",
            "GET  /info"
        ]
    }}
        

@app.get("/authenticated")
def authentication(response: Response):
    if is_authenticated(settings.user, settings.token):
        return {"response": "User is authenticated"}

    response.status_code = status.HTTP_401_UNAUTHORIZED
    return {"response": "Requires authentication"}


@app.post('/auth')
def get_authenticated(auth: Optional[Auth] = None):
    settings.user = settings.token = None

    if auth is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Requires authentication")
    
    res = is_authenticated(auth.user, auth.token)

    if res:
        settings.user = auth.user
        settings.token = auth.token
        return {"response": "User authenticated successfully"}
    
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Bad credentials")

@app.get('/logout')
def logout(response: Response):
    if is_authenticated(settings.user, settings.token):
        settings.user = settings.token = None
        return {"response": "Logged out successfully"}

    return Response(status_code=HTTPStatus.NOT_MODIFIED.value)

@app.get("/get-repos/{username}")
def get_user_repos(username: str):
    return get_repos(username, settings.user, settings.token)


@app.get("/get-info/{username}")
def get_user_info(username: str):
    return get_info(username, settings.user, settings.token)

@app.get("/about")
def about():
    return {
        "app_name": settings.app_name,
        "created_by": settings.author,
        "admin_email": settings.admin_email
    }