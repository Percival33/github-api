from pydantic import BaseModel
from typing import Optional


class Authentication(BaseModel):
    user: Optional[str] = None
    token: Optional[str] = None
