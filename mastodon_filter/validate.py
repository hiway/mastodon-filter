"""
Validation utilities.
"""
from mastodon_filter.api import FILTER_CONTEXTS


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
