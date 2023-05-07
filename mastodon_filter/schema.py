from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Keyword:
    keyword: str
    whole_word: bool = True
    delete: bool = False
    id: Optional[str] = None

    def __post_init__(self):
        self.keyword = self.keyword.strip()

    def __str__(self):
        return self.keyword
