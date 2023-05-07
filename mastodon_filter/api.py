import requests
from typing import Optional, Union

from mastodon_filter.config import Config

FILTER_CONTEXTS = ["home", "notifications", "public", "thread", "account"]
FILTER_ACTIONS = ["warn", "hide"]


def validate_title(title: str) -> None:
    if not title:
        raise ValueError("Title must not be empty.")


def validate_context(context: str) -> None:
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


def validate_action(action: str) -> None:
    if not action:
        raise ValueError("Filter action must not be empty.")
    if action not in FILTER_ACTIONS:
        raise ValueError(
            f"Invalid filter action: {action}, " "must be one of: {FILTER_ACTIONS}"
        )


def validate_keywords(keywords: Union[str, list[str]]) -> None:
    if not keywords:
        raise ValueError("Keywords must not be empty.")
    if not isinstance(keywords, (str, list)):
        raise TypeError("Keywords must be a string or a list.")


def validate_expires_in(expires_in: int) -> None:
    if expires_in and not isinstance(expires_in, int):
        raise TypeError("Expires in must be an integer (seconds).")


class MastodonFilters:
    """
    Mastodon filters API client.
    """

    def __init__(self, config: Config) -> None:
        self.config = config

    def _keyword_params(self, keywords: list[str]) -> dict:
        """
        Get keyword params.
        """
        params = {}
        for i, keyword in enumerate(keywords):
            if not keyword:
                continue
            if keyword.startswith("#"):
                continue
            params[f"keywords_attributes[{i}][keyword]"] = keyword
            params[f"keywords_attributes[{i}][whole_word]"] = True
        return params

    def _call_api(self, method: str, path: str, params: Optional[dict] = None) -> dict:
        """
        Call API method.
        """
        response = requests.request(
            method=method,
            url=f"{self.config.api_base_url}{path}",
            headers={"Authorization": f"Bearer {self.config.access_token}"},
            params=params,
        )
        response.raise_for_status()
        return response.json()

    def filters(self) -> dict:
        """
        Get filters.
        """
        return self._call_api("get", "/api/v2/filters")

    def filter(self, title: str) -> dict:
        """
        Get filter.
        """
        if not title:
            raise ValueError("Title must not be empty.")
        filters = self.filters()
        for filter_item in filters:
            if filter_item["title"] == title:
                return filter_item
        raise ValueError(f"Filter not found: {title}")

    def create(
        self,
        title: str,
        context: str,
        action: str,
        keywords: Union[str, list[str]],
        expires_in: int = None,
    ) -> dict:
        """
        Create filter.
        """
        validate_title(title)
        validate_context(context)
        validate_action(action)
        validate_keywords(keywords)
        validate_expires_in(expires_in)
        params = {
            "title": title,
            "context[]": context,
            "expires_in": expires_in,
            "filter_action": action,
        }
        params.update(self._keyword_params(keywords))
        return self._call_api("post", "/api/v2/filters", params)

    def delete(self, title: str) -> dict:
        """
        Delete filter.
        """
        if not title:
            raise ValueError("Title must not be empty.")
        filter_item = self.filter(title)
        return self._call_api("delete", f"/api/v2/filters/{filter_item['id']}")
