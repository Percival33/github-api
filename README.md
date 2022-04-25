# allegro-summer-experience-2022

## About

This is recruitment task for `Allegro Summer Experience 2022 internship`.

My email in recruitment process: [marcin.jarc@gmail.com](mailto:marcin.jarc@gmail.com)

#### Goal

Task was to create API which returns specific data about GitHub user using [GitHub REST API](https://docs.github.com/en/rest).
I've used [FastAPI](https://fastapi.tiangolo.com/) to create this project. <br/> I assumed this API will be only used on local machine, so every made request is authorized with Github credentials (if present).

## Installation

You need to have python3 installed on your machine. Firstly, clone the repo:

```bash
  git clone https://github.com/Percival33/allegro-summer-experience-2022.git
```

Change directory to folder with code. Then create new virtual environment `env` and activate it. If you don't have this package use this [link](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/) to install it.

```bash
 cd allegro-summer-experience-2022-main
 python3 -m venv env
 source env/bin/activate
```

Now you should see (env) next to prompt symbol (usually `$` sign for normal user).

Install dependencies and you're ready to go!

```bash
  pip install -r requirements.txt
```

Now you just need to run server locally.

```bash
  uvicorn api.main:app
```

Server is available at [127.0.0.1:8000](http://127.0.0.1:8000)!

After using API, turn off `virtualenv` using:

```bash
deactivate
```

## Usage

To avoid rate limit for unauthorized user from GitHub API, authenticate by creating `credentials.json`. See [creating credentials](#github-api-authorization).

1. One option is to go to [/docs](http://127.0.0.1:8000/docs) and use Swagger UI to use API

2. Other one is to make requests to endpoints in your favourite way

## API Reference

Every correct endpoint returns JSON response structured like this:

```json
{
  "response": {},
  "meta": {
    "limit": "[int]",
    "remaining": "[int]",
    "reset": "[UTC epoch seconds]",
    "used": "[int]"
  }
}
```

While endpoints which do not make request to GitHub API, holds zeros in meta fields.

| Status code | Description                                         |
| :---------: | :-------------------------------------------------- |
|    `304`    | Returned when logged out as unauthorized user       |
|    `401`    | Returned when no credentials or invalid are passed  |
|    `403`    | Returned when Github API rate limit is hit          |
|    `404`    | Returned when no data is found                      |
|    `500`    | Returned when api or Github API has internal errors |
|    `200`    | Returned in all other situations                    |

To take a look on full documentation about API, you can get it at [/docs](http://127.0.0.1:8000/docs)

## GitHub API authorization

To increase your rate limit to 5000 requests per hour, authentication is needed. To do so, GitHub username and [Personal Access Token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) are needed. To be automatically authorized create `credentials.json` file structured like this:

```json
{
  "user": "your_github_username",
  "token": "personal_access_token"
}
```

and restart server.

### Running tests and checks

To run tests, make sure you are in main directory and just type

```bash
  pytest
```

to run linter `flake8` type:

```bash
  flake8
```

## TODO (in future)

- [ ] add more sophisticated tests
