import click

from mastodon_filter.api import MastodonFilters, FILTER_ACTIONS, FILTER_CONTEXTS
from mastodon_filter.config import Config, ensure_config_exists, get_config, save_config
from mastodon_filter.errors import extract_error_message


def validate_context(context: str) -> None:
    if not context:
        raise ValueError("Context must not be empty.")
    if not isinstance(context, str):
        raise TypeError("Context must be a comma separated string.")
    context = [ctx.strip() for ctx in context.split(",")]
    for context_item in context:
        if context_item not in FILTER_CONTEXTS:
            click.echo(
                f"Invalid context: {context_item}, " "must be one of: {valid_contexts}"
            )
            raise click.Abort()
    return context


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
        error_message = extract_error_message(error)
        click.echo(f"Could not list filters: {title}, got response: {error_message}")


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
        error_message = extract_error_message(error)
        click.echo(f"Could not show filter: {title}, got response: {error_message}")


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
    context = validate_context(context)
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
        error_message = extract_error_message(error)
        click.echo(f"Could not create filter: {title}, got response: {error_message}")


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
        error_message = extract_error_message(error)
        click.echo(f"Could not delete filter: {title}, got response: {error_message}")
