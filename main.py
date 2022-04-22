from fastapi import FastAPI, HTTPException
from github_handler import get_info, is_authenticated
app = FastAPI()

@app.get("/")
def home():
    return {"Data": "Test"} 


@app.get("/get-repos/{username}")
def get_repos(username: str):
    return get_info(username)

@app.get("/authenticated")
def authentication():
    return is_authenticated()