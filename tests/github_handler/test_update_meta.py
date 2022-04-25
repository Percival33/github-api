from fastapi import HTTPException, status
from api.github_handler import GithubHandler
import pytest


def test_invalid_update_meta():
    github_handler = GithubHandler()
    res = github_handler.create_response()

    with pytest.raises(HTTPException) as exc:
        github_handler.update_meta(res, {
            "no_meta": ""
        })
    assert exc.type == HTTPException
    assert exc.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert exc.value.detail == "Something went wrong! Please try again."
