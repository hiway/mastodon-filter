import requests
from typing import Optional, Union

from mastodon_filter.config import Config
from mastodon_filter.schema import Keyword
from mastodon_filter.validate import (
    validate_action,
    validate_context,
    validate_keywords,
    validate_title,
    validate_expires_in,
)


class MastodonFilters:
    """
    Mastodon filters API client.
    """

    def __init__(self, config: Config) -> None:
        self.config = config

    def _build_keyword_params(self, keywords: list[Keyword]) -> dict:
        """
        Build keyword params.
        """
        params = {}
        for i, keyword in enumerate(keywords):
            params[f"keywords_attributes[{i}][keyword]"] = keyword.keyword
            params[f"keywords_attributes[{i}][whole_word]"] = keyword.whole_word
            if keyword.id:
                params[f"keywords_attributes[{i}][id]"] = keyword.id
            if keyword.delete:
                params[f"keywords_attributes[{i}][_destroy]"] = True
        return params

    def _call_api(
        self,
        method: str,
        path: str,
        data: Optional[dict] = None,
        params: Optional[dict] = None,
    ) -> dict:
        """
        Call API method.
        """
        response = requests.request(
            method=method,
            url=f"{self.config.api_base_url}{path}",
            headers={
                "Authorization": f"Bearer {self.config.access_token}",
                "Content-Type": "application/json",
            },
            data=data,
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
        title = validate_title(title)
        context = validate_context(context)
        action = validate_action(action)
        keywords = validate_keywords(keywords)
        expires_in = validate_expires_in(expires_in)
        params = {
            "title": title,
            "context[]": context,
            "expires_in": expires_in,
            "filter_action": action,
        }
        params.update(self._build_keyword_params(keywords))
        return self._call_api("post", "/api/v2/filters", params=params)

    def sync(self, title: str, keywords: Union[str, list[str]]) -> dict:
        """
        Sync filter.
        """
        title = validate_title(title)
        keywords = validate_keywords(keywords)
        filter_item = self.filter(title)

        remote_keywords = filter_item["keywords"]
        remote_keywords = [Keyword(**keyword) for keyword in remote_keywords]

        add_keywords = []
        delete_keywords = []
        for keyword in keywords:
            if keyword in remote_keywords:
                continue
            add_keywords.append(keyword)
        for keyword in remote_keywords:
            if keyword in keywords:
                continue
            keyword_to_delete = Keyword(
                keyword=keyword.keyword, id=keyword.id, delete=True
            )
            delete_keywords.append(keyword_to_delete)
        params = {
            "title": title,
            "context[]": filter_item["context"],
            "filter_action": filter_item["filter_action"],
        }
        params.update(self._build_keyword_params(add_keywords))
        params.update(self._build_keyword_params(delete_keywords))
        response = self._call_api(
            "put", f"/api/v2/filters/{filter_item['id']}", params=params
        )
        response["added"] = add_keywords
        response["deleted"] = delete_keywords
        return response

    def delete(self, title: str) -> dict:
        """
        Delete filter.
        """
        if not title:
            raise ValueError("Title must not be empty.")
        filter_item = self.filter(title)
        return self._call_api("delete", f"/api/v2/filters/{filter_item['id']}")
