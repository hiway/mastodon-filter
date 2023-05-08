"""
Validation utilities.
"""
from typing import Union
from mastodon_filter.schema import Keyword

FILTER_CONTEXTS = ["home", "notifications", "public", "thread", "account"]
FILTER_ACTIONS = ["warn", "hide"]


def validate_title(title: str) -> str:
    """Validate filter title."""
    if not title:
        raise ValueError("Title must not be empty.")
    return title


def validate_context(context: str) -> list[str]:
    """Validate filter context."""
    if not context:
        raise ValueError("Context must not be empty.")
    if not isinstance(context, (list, str)):
        raise TypeError("Context must be a string or a list.")
    if isinstance(context, str):
        context = [context]
    for context_item in context:
        if context_item not in FILTER_CONTEXTS:
            raise ValueError(
                f"Invalid context: {context_item}, " "must be one of: {valid_contexts}"
            )
    return context


def validate_action(action: str) -> str:
    """Validate filter action."""
    if not action:
        raise ValueError("Filter action must not be empty.")
    if action not in FILTER_ACTIONS:
        raise ValueError(
            f"Invalid filter action: {action}, " "must be one of: {FILTER_ACTIONS}"
        )
    return action


def validate_keywords(keywords: Union[str, list[str]]) -> list[Keyword]:
    """Validate filter keywords."""
    if not keywords:
        raise ValueError("Keywords must not be empty.")
    if not isinstance(keywords, (str, list)):
        raise TypeError("Keywords must be a string or a list.")
    if isinstance(keywords, str):
        keywords = [keywords]

    valid_keywords = []
    for keyword in keywords:
        if not keyword:
            continue
        if keyword.startswith("#"):
            continue
        valid_keywords.append(Keyword(keyword))
    return valid_keywords


def validate_expires_in(expires_in: int) -> int:
    """Validate filter expiration."""
    if expires_in and not isinstance(expires_in, int):
        raise TypeError("Expires in must be an integer (seconds).")
    return expires_in


def validate_context_string(context: str) -> None:
    """
    Validate filter context.
    Converts a comma separated string of contexts into a list of contexts.
    Raises ValueError if context is empty.
    """
    if not context:
        raise ValueError("Context must not be empty.")
    if not isinstance(context, str):
        raise TypeError("Context must be a comma separated string.")
    context = [ctx.strip() for ctx in context.split(",")]
    for context_item in context:
        if context_item not in FILTER_CONTEXTS:
            raise ValueError(
                f"Invalid context: {context_item}, " "must be one of: {valid_contexts}"
            )
    return context
