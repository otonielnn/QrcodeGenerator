from typing import Optional

from pydantic import BaseModel, HttpUrl


class QRCodeRequest(BaseModel):
    url: HttpUrl
    filename: Optional[str]
