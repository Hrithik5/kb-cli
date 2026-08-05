import argparse
from pathlib import Path
from kb.commands.base import BaseCommand
from kb.services.import_export_service import ImportExportService
from kb.utils.formatter import Formatter


class ExportCommand(BaseCommand):
    name = "export"
    help_text = "Export knowledge base entries to JSON, Markdown, or SQLite backup."

    @classmethod
    def configure_parser(cls, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("format", choices=["json", "markdown", "backup"], help="Export output format")
        parser.add_argument("output", help="Target output file path")
        parser.add_argument("-c", "--category", help="Filter export by category")

    def execute(self, args: argparse.Namespace) -> int:
        output_path = Path(args.output)
        import_service = ImportExportService(self.service)

        try:
            if args.format == "json":
                count = import_service.export_json(output_path, category=args.category)
                print(Formatter.color(f"✔ Exported {count} items to {output_path} (JSON)", Formatter.GREEN))
            elif args.format == "markdown":
                count = import_service.export_markdown(output_path, category=args.category)
                print(Formatter.color(f"✔ Exported {count} items to {output_path} (Markdown)", Formatter.GREEN))
            elif args.format == "backup":
                import_service.backup_database(self.config.database_path, output_path)
                print(Formatter.color(f"✔ Backed up database to {output_path}", Formatter.GREEN))
            return 0
        except Exception as e:
            print(Formatter.color(f"Error exporting database: {e}", Formatter.RED))
            return 1
