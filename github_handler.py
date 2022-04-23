from fastapi import HTTPException, status
from typing import Dict, List, Union, Any, Optional
import os
import json
import requests

HEADERS = {
    "Accept": "application/vnd.github.v3+json"
}

def get_langs(repo: Dict[str, Any], user: str = None, token: str = None) -> Dict[str, Optional[Dict[str, int]]]:
    response = {'langs': None}
    
    try:
        link = repo['languages_url']
    except KeyError as err:
        print(err)
        return response 
    
    langs = requests.get(link, auth=(user, token), headers=HEADERS)
    if langs.ok:
        response['langs'] = langs.json()
    
    return response


def get_repos(username: str, user: str = None, token: str = None) -> Dict[str, List[Any]]:
    data = requests.get(f'https://api.github.com/users/{username}/repos', auth=(user, token), headers=HEADERS)

    response = {'repos': []}
    
    if data.ok:
        for repo in data.json():
            repo_dict = {
                'name': repo['name'],
                'langs': get_langs(repo, user, token)['langs']
            }

            response['repos'].append(repo_dict)
        
        response['meta'] = {
            "RateLimit-Limit": data.headers["X-RateLimit-Limit"],
            "RateLimit-Used": data.headers["X-RateLimit-Used"],
            "RateLimit-Remaining": data.headers["X-RateLimit-Remaining"],
            "RateLimit-Reset": data.headers["X-RateLimit-Reset"]
        }

    return response


def get_info(username: str, user: str = None, token: str = None):
    data = requests.get(f'https://api.github.com/users/{username}', auth=(user, token), headers=HEADERS)

    response = {}

    if data.ok:
        response['login'] = data.json()['login']
        response['name'] = data.json()['name']
        response['bio'] = data.json()['bio']
        response['repos'] = get_repos(username, user, token)['repos']

        response['meta'] = {
            "RateLimit-Limit": data.headers["X-RateLimit-Limit"],
            "RateLimit-Used": data.headers["X-RateLimit-Used"],
            "RateLimit-Remaining": data.headers["X-RateLimit-Remaining"],
            "RateLimit-Reset": data.headers["X-RateLimit-Reset"]
        }

    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No such user exists')
    

    return response


def save_to_json(filename: str, res):
    with open(f'{filename}.json', 'w') as f:
        json.dump(res, f, indent=2)


def is_authenticated(user: str = None, token: str = None):
    
    r = requests.get(f'https://api.github.com/user', auth=(user, token), headers=HEADERS)

    if r.ok:
        return True

    else:
        # TODO: raise HTTPException/detailed response
        return False


if __name__ == '__main__':
    username = input("Input username to get user's data: ")
    
    user = os.environ.get('GITHUB_USERNAME')
    token = os.environ.get('ALLEGRO_SUMMER_EXPERIENCE_2022')

    print(is_authenticated(user, token))

    res = get_repos(username, user, token)
    save_to_json('repos', res)
    
    general_info = get_info(username, user, token)
    save_to_json('info', general_info)
