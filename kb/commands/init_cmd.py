import argparse
from kb.commands.base import BaseCommand
from kb.utils.formatter import Formatter


class InitCommand(BaseCommand):
    name = "init"
    help_text = "Initialize the kb database and configuration directory."

    @classmethod
    def configure_parser(cls, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("--force", action="store_true", help="Reinitialize database and config.")

    def execute(self, args: argparse.Namespace) -> int:
        config_path = self.config.save_default_config()
        self.service.repo.db.init_schema()
        print(Formatter.color(f"✔ Initialized kb database at {self.config.database_path}", Formatter.GREEN))
        print(Formatter.color(f"✔ Configuration saved at {config_path}", Formatter.CYAN))
        return 0
