"""
Command-line interface.
"""
from pathlib import Path

import click
from click_default_group import DefaultGroup

from mastodon_filter.api import MastodonFilters
from mastodon_filter.config import Config, ensure_config_exists, get_config, save_config
from mastodon_filter.errors import extract_error_message
from mastodon_filter.templates import list_templates, load_template
from mastodon_filter.validate import validate_context_string, FILTER_ACTIONS


@click.group(cls=DefaultGroup, default="gui", default_if_no_args=True)
def main() -> None:
    """
    Manage keyword filters on Mastodon from command-line.
    """


@main.command("gui")
def main_gui() -> None:
    """
    Run the GUI.
    """
    from mastodon_filter.gui import run_gui  # pylint: disable=import-outside-toplevel

    run_gui()


@main.command("newgui")
def main_newgui() -> None:
    """
    Run the new GUI.
    """
    from mastodon_filter.newgui.app import MastodonFilterGUI

    app = MastodonFilterGUI()
    app.mainloop()


@main.command("config")
def main_config() -> None:
    """
    Configure Mastodon API access.
    """
    config = get_config()
    api_base_url = click.prompt(
        "Instance URL", default=config.api_base_url or "https://example.social"
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
        click.echo(f"Could not list filters, got response: {error_message}")


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
    context = validate_context_string(context)
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


@main.command("sync")
@click.argument("title")
@click.argument("wordlist", type=click.File("rb", encoding="utf-8"))
def main_sync(
    title: str,
    wordlist: click.File,
) -> None:
    """
    Sync filter.
    """
    ensure_config_exists()
    config = get_config()
    filters = MastodonFilters(config)
    keywords = wordlist.read().decode("utf-8").splitlines()
    try:
        response = filters.sync(title, keywords)
        added = len(response["added"])
        deleted = len(response["deleted"])
        if added == 0 and deleted == 0:
            click.echo(f"Filter synced: {title}. No changes.")
            return
        if added > 0:
            click.echo("Added:")
            click.echo("  " + "\n  ".join(kw.keyword for kw in response["added"]))
        if deleted > 0:
            click.echo("Deleted:")
            click.echo("  " + "\n  ".join([kw.keyword for kw in response["deleted"]]))
        click.echo(
            f"Filter synced: {title}. Added {added}, deleted {deleted} keywords."
        )
    except Exception as error:
        error_message = extract_error_message(error)
        click.echo(f"Could not sync filter: {title}, got response: {error_message}")


@main.command("export")
@click.argument("path", type=click.Path(exists=False))
def main_export(path) -> None:
    """
    Export all filters.
    """
    path = Path(path)
    ensure_config_exists()
    config = get_config()
    filters = MastodonFilters(config)
    path.parent.mkdir(parents=True, exist_ok=True)
    filters.cache(path)


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


@main.group()
def template() -> None:
    """
    Filter templates.
    """


@template.command("list")
def template_list() -> None:
    """
    List templates.
    """
    for template in list_templates():
        click.echo(template)


@template.command("show")
@click.argument("name")
def template_show(name: str) -> None:
    """
    Show template.
    """
    keywords = load_template(name)
    for keyword in keywords:
        click.echo(keyword)


@template.command("use")
@click.argument("name")
@click.argument("title")
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
def main_use(
    name: str,
    title: str,
    context: list[str],
    action: str,
    expires_in: int,
) -> None:
    """
    Use template to create a new filter.
    """
    ensure_config_exists()
    config = get_config()
    filters = MastodonFilters(config)
    context = validate_context_string(context)
    keywords = load_template(name)
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
