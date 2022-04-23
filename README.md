# allegro-summer-experience-2022

## About

This is recruitment task for `Allegro Summer Experience 2022 internship`.

My email in recruitment process: [marcin.jarc@gmail.com](mailto:marcin.jarc@gmail.com)

#### Goal

Task was to create API which returns specific data about github user using [Github REST API](https://docs.github.com/en/rest).
I've used [FastAPI](https://fastapi.tiangolo.com/) to create this project.

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
  uvicorn main:app
```

Server is available at [127.0.0.1:8000](http://127.0.0.1:8000)!

## Usage

To avoid rate limit for unauthorized user from Github API, authenticate using `/auth` or create `credentials.json`. See [creating credentials](#github-api-authorization).

1. One option is to go to [/docs](http://127.0.0.1:8000/docs) and use Swagger UI to use API

2. Other one is to make requests to endpoints in your favourite way

## API Reference

#### Get info

Every response is structured like this:

```json
{
  "response": {},
  "meta": {
    "limit": int,
    "remaining": int,
    "reset": UTC epoch seconds,
    "used": int,
  }
}
```

While endpoints about this API, holds zeros in meta field.

```http
  GET /api/info
```

| Parameter | Type   | Description                 |
| :-------- | :----- | :-------------------------- |
| `None`    | `None` | Returns available endpoints |

#### Check if authenticated

```http
  GET /api/is_auth
```

| Parameter | Type   | Description |
| :-------- | :----- | :---------- |
| `None`    | `None` |             |

#### Get authenticated

```http
  POST /api/auth
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of item to fetch |

### Github API authorization

To increase your rate limit to 5000 requests per hour, authentication is needed. To do so, Github username and [Personal Access Token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) are needed. To be automaticaly authorized create `credentials.json` file structured like this:

```json
{
  "user": "your github username",
  "token": "personal_access_token"
}
```

If at any moment you want to make unauthorized request, call `/logout` endpoint and make wanted request. After that every request will be unauthorized.

## TODO

- [ ] add specification section
- [ ] add examples of usage
- [ ] create authentication endpoint
- [x] add specific error messages (bad authentication, resource not found, exceeding rate limit)
- [ ] add exceeded rate limit error
- [ ] type hinting
- [ ] fix is_authenticated fucntion
- [x] add user authentication
