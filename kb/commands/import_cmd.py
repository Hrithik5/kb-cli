import argparse
from pathlib import Path

from kb.commands.base import BaseCommand
from kb.services.import_export_service import ImportExportService
from kb.utils.formatter import Formatter


class ImportCommand(BaseCommand):
    name = "import"
    help_text = "Import notes or snippets from markdown/txt files."

    @classmethod
    def configure_parser(cls, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "format",
            choices=["markdown", "txt"],
            help="Import file format",
        )
        parser.add_argument("file", help="Path to input file")
        parser.add_argument(
            "-c",
            "--category",
            help="Category for imported item(s)",
        )

    def execute(self, args: argparse.Namespace) -> int:
        file_path = Path(args.file)
        import_service = ImportExportService(self.service)

        try:
            if args.format == "markdown":
                items = import_service.import_markdown_file(
                    file_path,
                    category=args.category,
                )
                print(
                    Formatter.color(
                        f"✔ Imported {len(items)} item(s) from {file_path}",
                        Formatter.GREEN,
                    )
                )

            else:  # txt
                item = import_service.import_txt_file(
                    file_path,
                    category=args.category,
                )
                print(
                    Formatter.color(
                        f"✔ Imported #{item.id} [{item.category}] {item.title}",
                        Formatter.GREEN,
                    )
                )

            return 0

        except (OSError, ValueError) as exc:
            print(
                Formatter.color(
                    f"Error importing file: {exc}",
                    Formatter.RED,
                )
            )
            return 1
