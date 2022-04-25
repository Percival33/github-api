from api.models.authentication import Authentication
from fastapi import HTTPException
from api.github_handler import GithubHandler
import pytest


def test_no_credentials():
    github_handler = GithubHandler()
    with pytest.raises(HTTPException) as exc:
        github_handler.is_authenticated(None)
    assert exc.type == HTTPException
    assert exc.value.status_code == 401
    assert exc.value.detail == "Requires authentication"


def test_bad_credentials():
    github_handler = GithubHandler()
    auth = Authentication()

    auth.user = "percival33"
    auth.token = ""

    with pytest.raises(HTTPException) as exc:
        github_handler.is_authenticated(auth)
    assert exc.type == HTTPException
    assert exc.value.status_code == 401
    assert exc.value.detail == "Bad credentials"
