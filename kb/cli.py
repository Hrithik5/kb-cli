import argparse
import sqlite3

from kb import __version__
from kb.commands.add_cmd import AddCommand
from kb.commands.clean_cmd import CleanCommand
from kb.commands.completion_cmd import CompletionCommand
from kb.commands.config_cmd import ConfigCommand
from kb.commands.copy_cmd import CopyCommand
from kb.commands.delete_cmd import DeleteCommand
from kb.commands.edit_cmd import EditCommand
from kb.commands.export_cmd import ExportCommand
from kb.commands.favorite_cmd import FavoriteCommand
from kb.commands.find_cmd import FindCommand
from kb.commands.fzf_cmd import FzfCommand
from kb.commands.get_cmd import GetCommand
from kb.commands.import_cmd import ImportCommand
from kb.commands.info_cmd import InfoCommand
from kb.commands.init_cmd import InitCommand
from kb.commands.list_cmd import ListCommand
from kb.commands.recent_cmd import RecentCommand
from kb.commands.stats_cmd import StatsCommand
from kb.config import Config
from kb.database import Database
from kb.repositories.knowledge_repository import KnowledgeRepository
from kb.services.knowledge_service import KnowledgeService
from kb.shell import InteractiveShell

COMMAND_CLASSES = [
    InitCommand,
    AddCommand,
    FindCommand,
    ListCommand,
    EditCommand,
    DeleteCommand,
    ImportCommand,
    ExportCommand,
    StatsCommand,
    FavoriteCommand,
    RecentCommand,
    CopyCommand,
    FzfCommand,
    GetCommand,
    CompletionCommand,
    InfoCommand,
    ConfigCommand,
    CleanCommand,
]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="kb",
        description="kb — Developer Knowledge Engine CLI powered by SQLite FTS5.",
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"kb version {__version__}",
    )

    parser.add_argument(
        "--config-file",
        help="Custom path to config file",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        help="Available kb subcommands",
    )

    for cmd_cls in COMMAND_CLASSES:
        sub_parser = subparsers.add_parser(
            cmd_cls.name,
            help=cmd_cls.help_text,
        )
        cmd_cls.configure_parser(sub_parser)

    return parser


def run_cli(args_list: list[str] | None = None) -> int:
    parser = build_parser()

    try:
        args = parser.parse_args(args_list)
    except SystemExit as exc:
        return exc.code

    cfg = Config.load(
        config_path=args.config_file
        if hasattr(args, "config_file") and args.config_file
        else None
    )

    db = Database(cfg.database_path)

    try:
        db.init_schema()
    except sqlite3.Error:
        # The init command will report database initialization failures.
        pass

    repo = KnowledgeRepository(db)
    service = KnowledgeService(repo)

    # Launch interactive shell if no subcommand was provided.
    if not args.command:
        shell = InteractiveShell(service, cfg)
        return shell.run()

    for cmd_cls in COMMAND_CLASSES:
        if cmd_cls.name == args.command:
            cmd = cmd_cls(service, cfg)
            return cmd.execute(args)

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(run_cli())
