import requests
import json
import os


def get_langs(repo, user: str, token: str):
    link = repo['languages_url']
    langs = requests.get(link, auth=(user, token))
    response = {'langs': None}
    if langs.ok:
        response['langs'] = langs.json()

    return response


def get_repos(username, user, token):
    data = requests.get(f'https://api.github.com/users/{username}/repos', auth=(user, token))

    response = {'repos': []}
    
    if data.ok:
        for repo in data.json():
            repo = {
                'name': repo['name'],
                'langs': get_langs(repo, user, token)['langs']
            }

            response['repos'].append(repo)

    return response


def get_info(username, user, token):
    data = requests.get(f'https://api.github.com/users/{username}', auth=(user, token))

    response = {}

    if data.ok:
        data = data.json()
        response['login'] = (data['login'])
        response['name'] = (data['name'])
        response['bio'] = (data['bio'])
        response['repos'] = get_repos(username, user, token)['repos']

    return response


def save_to_json(filename, res):
    with open(f'{filename}.json', 'w') as f:
        json.dump(res, f, indent=2)


def is_authenticated(user, token):
    
    r = requests.get(f'https://api.github.com/user', auth=(user, token))

    return r.ok


if __name__ == '__main__':
    username = input("Input username to get user's data: ")
    
    user = os.environ.get('GITHUB_USERNAME')
    token = os.environ.get('ALLEGRO_SUMMER_EXPERIENCE_2022')

    print(is_authenticated(user, token))

    res = get_repos(username, user, token)
    save_to_json('repos', res)
    
    general_info = get_info(username, user, token)
    save_to_json('info', general_info)
