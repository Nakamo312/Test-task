from datetime import datetime
from typing import Union

from pydantic import BaseModel


class Text(BaseModel):
    datetime: Union[datetime | str]
    title: str
    text: str


class ReadStringXCount(BaseModel):
    id: int
    datetime: datetime
    title: str
    x_avg_count_in_line: float
