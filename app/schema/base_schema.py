from datetime import datetime
from typing import List, Optional, Union

from pydantic import BaseModel


class ModelBaseInfo(BaseModel):
    id: int



class FindBase(BaseModel):
    ordering: Optional[str]
    page: Optional[int]
    page_size: Optional[Union[int, str]]


class SearchOptions(FindBase):
    total_count: Optional[int]


class FindResult(BaseModel):
    founds: Optional[List]
    search_options: Optional[SearchOptions]





class Blank(BaseModel):
    pass
