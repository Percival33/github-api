from pydantic import BaseModel
from typing import Optional

class Auth(BaseModel):
    user: Optional[str] = None
    token: Optional[str] = None