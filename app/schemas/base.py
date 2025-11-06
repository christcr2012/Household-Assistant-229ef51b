from datetime import datetime

from pydantic import BaseModel


class ORMBase(BaseModel):
    """Base schema enabling ORM mode."""

    class Config:
        from_attributes = True
        json_encoders = {datetime: lambda dt: dt.isoformat()}
