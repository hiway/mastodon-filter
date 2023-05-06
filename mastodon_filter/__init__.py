"""
Manage keyword filters on Mastodon from command-line.
"""
import click
import requests

from mastodon_filter.config import Config, ensure_config_exists, get_config, save_config


FILTER_CONTEXTS = ["home", "notifications", "public", "thread", "account"]
FILTER_ACTIONS = ["warn", "hide"]


class MastodonFilters:
    """
    Mastodon filters API client.
    """

    def __init__(self, config: Config) -> None:
        self.config = config

    def __keyword_params(self, keywords: list[str]) -> dict:
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

    def _get(self, path: str) -> dict:
        """
        Make a GET request.
        """
        response = requests.get(
            f"{self.config.api_base_url}{path}",
            headers={"Authorization": f"Bearer {self.config.access_token}"},
        )
        response.raise_for_status()
        return response.json()

    def _post(self, path: str, params: dict) -> dict:
        """
        Make a POST request.
        """
        response = requests.post(
            f"{self.config.api_base_url}{path}",
            headers={"Authorization": f"Bearer {self.config.access_token}"},
            params=params,
        )
        response.raise_for_status()
        return response.json()

    def _delete(self, path: str, params: dict) -> dict:
        """
        Make a DELETE request.
        """
        response = requests.delete(
            f"{self.config.api_base_url}{path}",
            headers={"Authorization": f"Bearer {self.config.access_token}"},
            params=params,
        )
        response.raise_for_status()
        return response.json()

    def filters(self) -> dict:
        """
        Get filters.
        """
        return self._get("/api/v2/filters")

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
        keywords: list[str],
        expires_in: int = None,
    ) -> dict:
        """
        Create filter.
        """
        if not title:
            raise ValueError("Title must not be empty.")
        if not context:
            raise ValueError("Context must not be empty.")
        if not isinstance(context, (list, str)):
            raise TypeError("Context must be a string or a list.")
        if isinstance(context, str):
            context = [context]
        for context_item in context:
            if context_item not in FILTER_CONTEXTS:
                raise ValueError(
                    f"Invalid context: {context_item}, "
                    "must be one of: {valid_contexts}"
                )
        if not action:
            raise ValueError("Filter action must not be empty.")
        if action not in FILTER_ACTIONS:
            raise ValueError(
                f"Invalid filter action: {action}, " "must be one of: {FILTER_ACTIONS}"
            )
        if not keywords:
            raise ValueError("Keywords must not be empty.")
        if not isinstance(keywords, (str, list)):
            raise TypeError("Keywords must be a string or a list.")
        if expires_in and not isinstance(expires_in, int):
            raise TypeError("Expires in must be an integer (seconds).")
        params = {
            "title": title,
            "context[]": context,
            "expires_in": expires_in,
            "filter_action": action,
        }
        params.update(self.__keyword_params(keywords))
        return self._post("/api/v2/filters", params)

    def delete(self, title: str) -> dict:
        """
        Delete filter.
        """
        if not title:
            raise ValueError("Title must not be empty.")
        filter_item = self.filter(title)
        return self._delete(f"/api/v2/filters/{filter_item['id']}", {})


@click.group()
def main() -> None:
    """
    Manage keyword filters on Mastodon from command-line.
    """


@main.command("config")
def main_config() -> None:
    """
    Configure Mastodon API access.
    """
    config = get_config()
    api_base_url = click.prompt(
        "Instance URL", default=config.api_base_url or "https://mastodon.social"
    )
    access_token = click.prompt("Access token", default=config.access_token)
    config = Config(api_base_url, access_token)
    save_config(config)


@main.command("list")
def main_list() -> None:
    """
    List filters.
    """
    ensure_config_exists()
    config = get_config()
    try:
        filters = MastodonFilters(config)
        for filter_item in filters.filters():
            click.echo(f"{filter_item['title']}: {len(filter_item['keywords'])}")
    except Exception as error:
        click.echo(error)


@main.command("show")
@click.argument("title")
def main_show(title: str) -> None:
    """
    Show filter.
    """
    ensure_config_exists()
    config = get_config()
    filters = MastodonFilters(config)
    try:
        filter_item = filters.filter(title)
        for keyword in filter_item["keywords"]:
            click.echo(keyword["keyword"])
    except Exception as error:
        click.echo(error)


@main.command("create")
@click.argument("title")
@click.argument("wordlist", type=click.File("rb", encoding="utf-8"))
@click.option(
    "--context",
    "-c",
    default="home,public,thread",
    prompt=True,
)
@click.option(
    "--action", "-a", default="warn", prompt=True, type=click.Choice(FILTER_ACTIONS)
)
@click.option("--expires-in", "-e", type=int)
def main_create(
    title: str,
    wordlist: click.File,
    context: list[str],
    action: str,
    expires_in: int,
) -> None:
    """
    Create filter.
    """
    context = context.split(",")
    for context_item in context:
        if context_item not in FILTER_CONTEXTS:
            click.echo(
                f"Invalid context: {context_item}, " "must be one of: {valid_contexts}"
            )
            raise click.Abort()
    ensure_config_exists()
    config = get_config()
    filters = MastodonFilters(config)
    keywords = wordlist.read().decode("utf-8").splitlines()
    try:
        for filter_item in filters.filters():
            if filter_item["title"] == title:
                raise ValueError(f"Filter already exists: {title}")

        response = filters.create(
            title=title,
            context=context,
            action=action,
            keywords=keywords,
            expires_in=expires_in,
        )
        click.echo(
            f"Filter created: {response['title']} with {len(keywords)} keywords."
        )
    except Exception as error:
        click.echo(error)


@main.command("delete")
@click.argument("title")
def main_delete(title: str) -> None:
    """
    Delete filter.
    """
    ensure_config_exists()
    config = get_config()
    filters = MastodonFilters(config)
    try:
        filters.delete(title)
        click.echo(f"Filter deleted: {title}")
    except Exception as error:
        click.echo(error)
