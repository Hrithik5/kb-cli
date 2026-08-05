import argparse

from kb.commands.base import BaseCommand
from kb.database import Database
from kb.utils.formatter import Formatter


class CleanCommand(BaseCommand):
    """Reset the knowledge base."""

    name = "clean"
    help_text = "Delete all knowledge items and recreate a fresh database."

    @classmethod
    def configure_parser(cls, parser: argparse.ArgumentParser) -> None:
        parser.description = (
            "Delete all knowledge items and recreate an empty database."
        )
        parser.add_argument(
            "-y",
            "--yes",
            action="store_true",
            help="Skip confirmation prompt",
        )

    def execute(self, args: argparse.Namespace) -> int:
        db_path = self.config.database_path

        if not args.yes:
            print(
                Formatter.color(
                    "⚠ WARNING",
                    Formatter.YELLOW + Formatter.BOLD,
                )
            )
            print()
            print("This will permanently delete ALL knowledge entries.")
            print(f"Database : {db_path}")
            print()

            confirm = input("Continue? [y/N]: ").strip().lower()

            if confirm != "y":
                print(
                    Formatter.color(
                        "Cancelled.",
                        Formatter.YELLOW,
                    )
                )
                return 0

        try:
            if db_path.exists():
                db_path.unlink()

            db = Database(db_path)
            db.init_schema()

            print(
                Formatter.color(
                    "✔ Knowledge base has been reset.",
                    Formatter.GREEN,
                )
            )

            print(
                Formatter.color(
                    f"New database created at:\n{db_path}",
                    Formatter.DIM,
                )
            )

            return 0

        except OSError as exc:
            print(
                Formatter.color(
                    f"Error: {exc}",
                    Formatter.RED,
                )
            )
            return 1
