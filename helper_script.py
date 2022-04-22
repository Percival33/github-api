import json
filename = 'repos'

with open(f'{filename}.json', 'r') as f:
    file = json.load(f)

repos = file['repos']

for repo in repos:
    for lang, bites in repo['langs'].items():
        print(lang, bites)