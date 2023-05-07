from pathlib import Path


def list_templates() -> list:
    """
    List templates.
    """
    templates_path = Path(__file__).parent / "templates"
    return [
        template.name.removesuffix(".txt")
        for template in templates_path.iterdir()
        if template.is_file()
    ]


def load_template(template_name: str) -> list[str]:
    """
    Load template.
    """
    templates_path = Path(__file__).parent / "templates"
    template_path = templates_path / (template_name + ".txt")
    if not template_path.exists():
        raise ValueError(f"Template not found: {template_name}")
    with template_path.open("rb") as template_file:
        return template_file.read().decode("utf-8").splitlines()
