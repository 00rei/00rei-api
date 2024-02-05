from pydantic import BaseModel, Field


class QRData(BaseModel):
    url: str = Field(max_length=2000)

