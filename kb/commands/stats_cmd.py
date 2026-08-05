import argparse

from kb.commands.base import BaseCommand
from kb.utils.formatter import Formatter


class StatsCommand(BaseCommand):
    name = "stats"
    help_text = "Display knowledge base statistics, category counts, and top access metrics."

    @classmethod
    def configure_parser(cls, parser: argparse.ArgumentParser) -> None:
        pass

    def execute(self, args: argparse.Namespace) -> int:
        stats = self.service.get_stats()
        print(Formatter.format_stats(stats))
        return 0
