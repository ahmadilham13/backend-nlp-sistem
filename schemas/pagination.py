from typing import Generic, TypeVar, List
from pydantic import BaseModel

# TypeVar memungkinkan schema ini menerima tipe data apapun
T = TypeVar('T')

class PageResponse(BaseModel, Generic[T]):
    items: List[T]
    total_items: int
    page: int
    page_size: int
    total_pages: int

    class Config:
        from_attributes = True