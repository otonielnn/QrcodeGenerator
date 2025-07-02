from pydantic import BaseModel, HttpUrl
from typing import Optional

class QRCodeRequest(BaseModel):
    url: HttpUrl
    filename: Optional[str]