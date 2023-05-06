import json
from dataclasses import dataclass, asdict
from pathlib import Path

import click


APP_DIR = Path(click.get_app_dir("mastodon-filter"))
APP_DIR.mkdir(parents=True, exist_ok=True)

CONFIG_FILE = APP_DIR / "config.json"


@dataclass
class Config:
    """
    Config dataclass.
    """

    api_base_url: str
    access_token: str

    def __post_init__(self) -> None:
        self.api_base_url = self.api_base_url.rstrip("/")
        self.access_token = self.access_token.strip()


def get_config() -> Config:
    """
    Get config from file.
    """
    if not CONFIG_FILE.exists():
        return Config("", "")

    with CONFIG_FILE.open() as f:
        return Config(**json.load(f))


def save_config(config: Config) -> None:
    """
    Save config to file.
    """
    with CONFIG_FILE.open("w") as f:
        json.dump(asdict(config), f)


def ensure_config_exists() -> None:
    """
    Ensure config exists.
    """
    config = get_config()
    if not config.api_base_url or not config.access_token:
        click.echo(
            "Config is not set up.\n"
            "Run `mastodon-filter config` to set up the config."
        )
        raise click.Abort()
