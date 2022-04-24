from fastapi import status
from typing import Dict, Any
import json
import requests

HEADERS = {
    "Accept": "application/vnd.github.v3+json"
}


def get_langs(repo: Dict[str, Any], user: str = None, token: str = None):
    response = {
        "response": None,
        "meta": {
            "limit": 0,
            "remaining": 0,
            "reset": 0,
            "used": 0
        }
    }
    
    link = repo["languages_url"]   
    langs = requests.get(link, auth=(user, token), headers=HEADERS)

    response["meta"] = {
        "limit": langs.headers["X-RateLimit-Limit"],
        "remaining": langs.headers["X-RateLimit-Remaining"],
        "reset": langs.headers["X-RateLimit-Reset"],
        "used": langs.headers["X-RateLimit-Used"]
    }

    if langs.ok:
        response["response"] = langs.json()      

    return response, langs.status_code


def get_repos(username: str, user: str = None, token: str = None):
    data = requests.get(f'https://api.github.com/users/{username}/repos', auth=(user, token), headers=HEADERS)

    response_code = 200

    response = {
        "response": {"repos": []},
        "meta": {
            "limit": data.headers["X-RateLimit-Limit"],
            "remaining": data.headers["X-RateLimit-Remaining"],
            "reset": data.headers["X-RateLimit-Reset"],
            "used": data.headers["X-RateLimit-Used"]
        }
    }

    if data.ok:
        for repo in data.json():
            tmp, tmp_code = get_langs(repo, user, token)
            meta = tmp["meta"]

            if tmp_code != 200:
                break 

            repo_dict = {
                "name": repo["name"],
                "langs": tmp["response"]
            }

            response["response"]["repos"].append(repo_dict)
            response["meta"] = meta  
        return response, response_code
    
    if int(response['meta']['remaining']) == 0:
        response_code = status.HTTP_403_FORBIDDEN
        response["response"] = "Github API rate limit exceeded"    
    else:
        response_code = status.HTTP_404_NOT_FOUND
        response["response"] = "No such user exists"    

    return response, response_code


def get_info(username: str, user: str = None, token: str = None):
    data = requests.get(f'https://api.github.com/users/{username}', auth=(user, token), headers=HEADERS)
    response_code = 200

    meta = {
        "limit": data.headers["X-RateLimit-Limit"],
        "remaining": data.headers["X-RateLimit-Remaining"],
        "reset": data.headers["X-RateLimit-Reset"],
        "used": data.headers["X-RateLimit-Used"]
    }

    response = {"response": {}, "meta": meta}

    if data.ok:
        response["response"]["login"] = data.json()["login"]
        response["response"]["name"] = data.json()["name"]
        response["response"]["bio"] = data.json()["bio"]

        tmp = get_repos(username, user, token)
      
        response["response"]["repos"] = tmp["response"]["repos"]
        response["meta"] = tmp["meta"]

    else:
        if int(response['meta']['remaining']) == 0:
            response_code = status.HTTP_403_FORBIDDEN
            response["response"] = "Github API rate limit exceeded"    
        else:
            response_code = status.HTTP_404_NOT_FOUND
            response["response"] = "No such user exists"        

    return response, response_code


def save_to_json(filename: str, res):
    with open(f'{filename}.json', 'w') as f:
        json.dump(res, f, indent=2)


def is_authenticated(user: str = None, token: str = None):
    
    r = requests.get(f"https://api.github.com/user", auth=(user, token), headers=HEADERS)

    meta = {
        "limit": r.headers["X-RateLimit-Limit"],
        "remaining": r.headers["X-RateLimit-Remaining"],
        "reset": r.headers["X-RateLimit-Reset"],
        "used": r.headers["X-RateLimit-Used"]
    }

    if r.ok:
        return True, meta

    else:
        return False, meta
