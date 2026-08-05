import argparse

from kb.commands.base import BaseCommand
from kb.utils.formatter import Formatter


class ConfigCommand(BaseCommand):
    """Display the current kb configuration."""

    name = "config"
    help_text = "Show the current kb configuration."

    @classmethod
    def configure_parser(cls, parser: argparse.ArgumentParser) -> None:
        # No arguments.
        return

    def execute(self, args: argparse.Namespace) -> int:
        print(
            Formatter.color(
                "Current Configuration",
                Formatter.CYAN + Formatter.BOLD,
            )
        )
        print()

        print(f"Database      : {self.config.database_path}")
        print(f"Editor        : {self.config.editor}")
        print(f"Default Limit : {self.config.default_limit}")
        print(f"Theme         : {self.config.theme}")
        print(f"Pager         : {self.config.pager}")

        return 0
