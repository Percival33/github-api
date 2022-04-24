from fastapi import HTTPException
from api.github_handler import GithubHandler
import pytest


@pytest.mark.xfail
def test_is_authenticated():
    github_handler = GithubHandler()
    response = github_handler.is_authenticated(None)
