from dataclasses import dataclass
from .pagination import Pagination
from typing import Generic, TypeVar


T = TypeVar("T")


@dataclass(slots=True)
class PaginationResult(Generic[T]):

    items: list[T]
    pagination: Pagination
