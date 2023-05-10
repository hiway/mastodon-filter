"""
Mastodon filters API client.
"""
import json
from collections import OrderedDict
from pathlib import Path
from typing import Optional, Union

import requests

from mastodon_filter.config import Config
from mastodon_filter.logging import get_logger
from mastodon_filter.schema import Keyword, Context, Status, Filter
from mastodon_filter.validate import (
    validate_action,
    validate_context,
    validate_keywords,
    validate_title,
    validate_expires_in,
)

logger = get_logger(__name__)


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
        params = OrderedDict()
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
        params: Optional[OrderedDict] = None,
    ) -> dict:
        """
        Call API method.
        """
        if not self.config.api_base_url or not self.config.access_token:
            logger.error("API base URL or access token not set.")
            raise ValueError("API base URL or access token not set.")

        logger.debug("Calling API method: %s %s with params: %s", method, path, params)
        response = requests.request(
            method=method,
            url=f"{self.config.api_base_url}{path}",
            headers={
                "Authorization": f"Bearer {self.config.access_token}",
                "Content-Type": "application/json",
            },
            data=data,
            params=params,
            timeout=10,
        )
        logger.debug("Server response: %s", response.text)
        response.raise_for_status()
        return response.json()

    def filters(self) -> dict:
        """
        Get filters.
        """
        response = self._call_api("get", "/api/v2/filters")
        return [
            Filter(
                title=filter_item["title"],
                context=Context.from_list(filter_item["context"]),
                keywords=[Keyword(**keyword) for keyword in filter_item["keywords"]],
                statuses=[Status(**status) for status in filter_item["statuses"]],
                expires_at=filter_item["expires_at"],
                filter_action=filter_item["filter_action"],
                id=filter_item["id"],
            )
            for filter_item in response
        ]

    def filter(self, title: str) -> dict:
        """
        Get filter.
        """
        if not title:
            raise ValueError("Title must not be empty.")
        filters = self.filters()
        for filter_item in filters:
            if filter_item["title"] == title:
                return Filter(
                    title=filter_item["title"],
                    context=Context.from_list(filter_item["context"]),
                    keywords=[
                        Keyword(**keyword) for keyword in filter_item["keywords"]
                    ],
                    statuses=[Status(**status) for status in filter_item["statuses"]],
                    expires_at=filter_item["expires_at"],
                    filter_action=filter_item["filter_action"],
                    id=filter_item["id"],
                )

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
        params = OrderedDict(
            {
                "title": title,
                "context[]": context,
                "expires_in": expires_in,
                "filter_action": action,
            }
        )
        params.update(self._build_keyword_params(keywords))
        filter_item = self._call_api("post", "/api/v2/filters", params=params)
        return Filter(
            title=filter_item["title"],
            context=Context.from_list(filter_item["context"]),
            keywords=[Keyword(**keyword) for keyword in filter_item["keywords"]],
            statuses=[Status(**status) for status in filter_item["statuses"]],
            expires_at=filter_item["expires_at"],
            filter_action=filter_item["filter_action"],
            id=filter_item["id"],
        )

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

        logger.debug("Add keywords: %s", add_keywords)
        logger.debug("Delete keywords: %s", delete_keywords)

        params = OrderedDict(
            {
                "title": title,
                "context[]": filter_item["context"],
                "filter_action": filter_item["filter_action"],
            }
        )
        params.update(self._build_keyword_params(add_keywords + delete_keywords))
        response = self._call_api(
            "put", f"/api/v2/filters/{filter_item['id']}", params=params
        )
        # response["added"] = add_keywords
        # response["deleted"] = delete_keywords
        response = self._call_api("get", "/api/v2/filters")
        return [
            Filter(
                title=filter_item["title"],
                context=Context.from_list(filter_item["context"]),
                keywords=[Keyword(**keyword) for keyword in filter_item["keywords"]],
                statuses=[Status(**status) for status in filter_item["statuses"]],
                expires_at=filter_item["expires_at"],
                filter_action=filter_item["filter_action"],
                id=filter_item["id"],
            )
            for filter_item in response
        ]

    def delete(self, title: str) -> dict:
        """
        Delete filter.
        """
        if not title:
            raise ValueError("Title must not be empty.")
        filter_item = self.filter(title)
        filter_item = self._call_api("delete", f"/api/v2/filters/{filter_item['id']}")
        return Filter(
            title=filter_item["title"],
            context=Context.from_list(filter_item["context"]),
            keywords=[Keyword(**keyword) for keyword in filter_item["keywords"]],
            statuses=[Status(**status) for status in filter_item["statuses"]],
            expires_at=filter_item["expires_at"],
            filter_action=filter_item["filter_action"],
            id=filter_item["id"],
        )

    def export(self, path: Path) -> dict:
        """
        Export filters.
        """
        if not path:
            raise ValueError("Path must not be empty.")
        filters = self.filters()
        path.write_text(json.dumps(filters), encoding="utf-8")
        return filters
