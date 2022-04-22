from fastapi import HTTPException
from typing import Dict, List, Union, Any, Optional
import os
import json
import requests

def get_langs(repo: Dict[str, Any], user: str = None, token: str = None) -> Dict[str, Optional[Dict[str, int]]]:
    response = {'langs': None}
    
    try:
        link = repo['languages_url']
    except KeyError as err:
        print(err)
        return response 
    
    langs = requests.get(link, auth=(user, token))
    if langs.ok:
        response['langs'] = langs.json()

    return response


def get_repos(username: str, user: str = None, token: str = None) -> Dict[str, List[Any]]:
    data = requests.get(f'https://api.github.com/users/{username}/repos', auth=(user, token))

    response = {'repos': []}
    
    if data.ok:
        for repo in data.json():
            print(repo)
            repo_dict = {
                'name': repo['name'],
                'langs': get_langs(repo, user, token)['langs']
            }

            response['repos'].append(repo_dict)

    print(response)

    return response


def get_info(username: str, user: str = None, token: str = None):
    data = requests.get(f'https://api.github.com/users/{username}', auth=(user, token))

    response = {}

    if data.ok:
        data = data.json()
        response['login'] = (data['login'])
        response['name'] = (data['name'])
        response['bio'] = (data['bio'])
        response['repos'] = get_repos(username, user, token)['repos']
    else:
        response = {"Error": "No such user exists"}
        raise HTTPException(status_code=404)
    return response


def save_to_json(filename: str, res: str):
    with open(f'{filename}.json', 'w') as f:
        json.dump(res, f, indent=2)


def is_authenticated(user: str = None, token: str = None):
    
    r = requests.get(f'https://api.github.com/user', auth=(user, token))

    return {"Response": "User not authenticated"}


if __name__ == '__main__':
    username = input("Input username to get user's data: ")
    
    user = os.environ.get('GITHUB_USERNAME')
    token = os.environ.get('ALLEGRO_SUMMER_EXPERIENCE_2022')

    print(is_authenticated(user, token))

    res = get_repos(username, user, token)
    save_to_json('repos', res)
    
    general_info = get_info(username, user, token)
    save_to_json('info', general_info)
