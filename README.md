# allegro-summer-experience-2022

## About

This is recruitment task for `Allegro Summer Experience 2022 internship`.

My email in recruitment process: [marcin.jarc@gmail.com](mailto:marcin.jarc@gmail.com)

#### Goal

Task was to create API which returns specific data about github user.
I've used [FastAPI](https://fastapi.tiangolo.com/) to create this project.

## Installation

You need to have python3 installed on your machine. Firstly, clone the repo:

```bash
$ git clone https://github.com/Percival33/allegro-summer-experience-2022.git
```

Then create new virtualenv `env` and activate it.

```bash
$ python3 -m virtualenv env
$ source env/bin/activate
```

Install dependencies and you're ready to go!

```bash
(env)$ pip install -r requirements.txt
```

Now you just need to run server locally

```bash
(env)$ uvicorn main:app
```

### TODO

- [ ] add specification section
- [ ] add examples of usage
- [ ] create authentication endpoint
- [x] add specific error messages (bad authentication, resource not found, exceeding rate limit)
- [ ] add exceeded rate limit error
- [ ] type hinting
- [ ] fix is_authenticated fucntion
- [x] add user authentication
