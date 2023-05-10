from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Keyword:
    """
    Keyword.
    """

    keyword: str
    whole_word: bool = True
    delete: bool = False
    id: Optional[str] = None  # pylint: disable=invalid-name

    def __post_init__(self):
        self.keyword = self.keyword.strip()

    def __str__(self):
        return self.keyword

    def __eq__(self, o):
        return self.keyword == o.keyword


@dataclass
class Context:
    """
    Context.
    """

    home: bool = False
    notifications: bool = False
    public: bool = False
    thread: bool = False
    account: bool = False

    @classmethod
    def from_list(cls, context):
        """
        Create context from list.
        """
        return cls(
            home="home" in context,
            notifications="notifications" in context,
            public="public" in context,
            thread="thread" in context,
            account="account" in context,
        )

    def to_list(self):
        """
        Create context from list.
        """
        return [
            key
            for key, value in asdict(self).items()
            if value is True and key != "account"
        ]

    def __str__(self):
        return ",".join(
            [
                key
                for key, value in asdict(self).items()
                if value is True and key != "account"
            ]
        )


@dataclass
class Status:
    """
    Status.
    """

    id: str  # pylint: disable=invalid-name
    status_id: str


@dataclass
class Filter:
    """
    Filter.
    """

    title: str
    context: Context
    keywords: list[Keyword]
    statuses: list[Status]
    expires_at: Optional[int] = None
    filter_action: str = "hide"
    id: Optional[str] = None  # pylint: disable=invalid-name

    def __post_init__(self):
        self.title = self.title.strip()

    def __str__(self):
        return self.title

    def __eq__(self, o):
        return self.title == o.title
