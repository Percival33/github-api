from fastapi import HTTPException
from api.github_handler import GithubHandler
from api.config import Settings
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
    settings = Settings()
    settings.auth.token = ""

    with pytest.raises(HTTPException) as exc:
        github_handler.is_authenticated(settings.auth)
    assert exc.type == HTTPException
    assert exc.value.status_code == 401
    assert exc.value.detail == "Bad credentials"
