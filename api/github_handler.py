from fastapi import HTTPException, status
from typing import Dict, Any, Optional
from .models.authentication import Authentication
import json
import requests


class GithubHandler:
    def __init__(self) -> None:
        pass

    def make_request(self, link: str, auth: Optional[Authentication] = None):

        response = self.create_response()
        headers = {
            "Accept": "application/vnd.github.v3+json"
        }

        if auth is None:
            r = requests.get(link, headers=headers)
        else:
            r = requests.get(link, auth=(auth.user, auth.token), headers=headers)

        response["meta"] = {
            "limit": r.headers["X-RateLimit-Limit"],
            "remaining": r.headers["X-RateLimit-Remaining"],
            "reset": r.headers["X-RateLimit-Reset"],
            "used": r.headers["X-RateLimit-Used"]
        }

        if r.ok:
            response["response"] = r.json()
            return response

        # TODO: create custom exception
        if int(r.headers["X-RateLimit-Remaining"]) == 0:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Github API rate limit exceeded")
        if r.status_code == 401:
            # detail = "401"
            if auth is None:
                detail = "Requires authentication"
            else:
                detail = "Bad credentials"

            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)
        if r.status_code == 404:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such user exists")

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def update_meta(res: Dict[str, Any] = None, other_res: Dict[str, Any] = None):
        try:
            res["meta"] = other_res["meta"]
        except KeyError:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Something went wrong! Please try again.")

        return res

    @staticmethod
    def create_response():
        response = {
            "response": "",
            "meta": {
                "limit": 0,
                "remaining": 0,
                "reset": 0,
                "used": 0
            }
        }

        return response

    def get_repos(self, username: str, auth: Optional[Authentication] = None):
        link = f'https://api.github.com/users/{username}/repos'
        r = self.make_request(link, auth)

        response = self.create_response()
        response["response"] = {
            "repos": []
        }

        self.update_meta(response, r)

        for repo in r["response"]:
            langs = self.make_request(repo["languages_url"], auth)
            self.update_meta(response, langs)

            repo_dict = {
                "name": repo["name"],
                "langs": langs["response"]
            }

            response["response"]["repos"].append(repo_dict)

        return response

    def get_info(self, username: str, auth: Optional[Authentication] = None):
        link = f'https://api.github.com/users/{username}'
        r = self.make_request(link, auth)

        response = self.create_response()
        response["response"] = dict()
        self.update_meta(response, r)

        response["response"]["login"] = r["response"]["login"]
        response["response"]["name"] = r["response"]["name"]
        response["response"]["bio"] = r["response"]["bio"]

        tmp = self.get_repos(username, auth)
        response["response"]["repos"] = tmp["response"]["repos"]
        self.update_meta(response, tmp)

        return response

    def is_authenticated(self, auth: Optional[Authentication] = None):
        r = self.make_request(f"https://api.github.com/user", auth)
        response = self.create_response()
        self.update_meta(response, r)
        response["response"] = "User authenticated"

        return response

    @staticmethod
    def save_to_json(filename: str, res):
        with open(f'{filename}.json', 'w') as f:
            json.dump(res, f, indent=2)
