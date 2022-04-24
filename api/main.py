from fastapi import FastAPI
from .github_handler import GithubHandler
from .config import Settings, get_credentials

description = """
Allegro Summer Experience 2022

## Functionality

- Get Repos for specific user with languages and number of bytes written in this language 
- Get login, name, bio and repos for specific user
- See [README](https://github.com/Percival33/allegro-summer-experience-2022#usage) for detailed usage instructions


"""

tags_metadata = [
    {
        "name": "home",
        "description": "`It works!`",
    },
    {
        "name": "info",
        "description": "Get available endpoints."
    },
    {
        "name": "GithubAPI",
        "description": "Get github user related data.",
        "externalDocs": {
            "description": "Github API external docs",
            "url": "https://docs.github.com/en",
        }
    },
    {
        "name": "about",
        "description": "Informations about creator of this API.",
    },
]

app = FastAPI(
    title="Allegro Summer Experience 2022 API",
    description=description,
    version="0.0.1",
    contact={
        "name": "Marcin Jarczewski",
        "email": "marcin.jarc@gmail.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    openapi_tags=tags_metadata
)
settings = Settings()

@app.get("/", tags=["home"])
def home():
    """
        hehe
    """
    return {
        "response": "It works!",
        "meta": {
            "limit": 0,
            "remaining": 0,
            "reset": 0,
            "used": 0,
        }
    }


@app.get("/api/info", tags=["info"])
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
        

@app.get("/api/get-repos/{username}", tags=["GithubAPI"])
def get_user_repos(username: str):
    auth = None
    
    if settings.auth is not None:
        auth = settings.auth

    github_handler = GithubHandler()

    return github_handler.get_repos(username, auth)


@app.get("/api/get-info/{username}", tags=["GithubAPI"])
def get_user_info(username: str):
    auth = None

    if settings.auth is not None:
        auth = settings.auth
        
    github_handler = GithubHandler()    

    return github_handler.get_info(username, auth)


@app.get("/api/about", tags=["about"])
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
