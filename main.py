import requests
import json
import os

def get_repos(username):
    data = requests.get(f'https://api.github.com/users/{username}/repos')

    response = []

    if data.ok:
        for repo in data.json():
            link = repo['languages_url']
            langs = requests.get(link)
            # print(repo['name'], langs.json())
            response.append({repo['name']: langs.json()})

    return response


def save_to_json(filename, res):
    with open(f'{filename}.json', 'w') as f:
        json.dump(res, f, indent=2)

def authenticate_user():
    username = os.environ.get('GITHUB_USERNAME')
    PAT = os.environ.get('ALLEGRO_SUMMER_EXPERIENCE_2022')
    # with open('credentials.json', 'r') as f:
    #     credentials = json.load(f)

    #     username = credentials['username']
    #     PAT = credentials['token']

    r = requests.get(f'https://api.github.com/user', auth=(username, PAT))

    print(f'auth: {r.json()}')


if __name__ == '__main__':
    # username, token = authenticate_user()
    # print(r.text)
    username = input()
    res = get_repos(username)
    save_to_json('repos', res)
