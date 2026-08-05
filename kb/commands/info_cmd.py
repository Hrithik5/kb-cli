import argparse

from kb import __version__
from kb.commands.base import BaseCommand
from kb.utils.formatter import Formatter


class InfoCommand(BaseCommand):
    """Display kb runtime information."""

    name = "info"
    help_text = "Show kb runtime information."

    @classmethod
    def configure_parser(cls, parser: argparse.ArgumentParser) -> None:
        parser.description = "Display runtime information about kb."
        # No additional arguments.
        return

    def execute(self, args: argparse.Namespace) -> int:
        stats = self.service.get_stats()

        print(
            Formatter.color(
                f"kb v{__version__}",
                Formatter.CYAN + Formatter.BOLD,
            )
        )
        print()

        print(f"Database : {self.config.database_path}")
        print(f"Editor   : {self.config.editor}")
        print(f"Theme    : {self.config.theme}")
        print(f"Pager    : {self.config.pager}")

        print()

        print(f"Entries  : {stats.get('total_items', 0)}")
        print(f"Favorites: {stats.get('favorites', 0)}")

        return 0
