import argparse
import os
import shutil
import subprocess
import sys

from kb.commands.base import BaseCommand
from kb.utils.clipboard import copy_to_clipboard
from kb.utils.formatter import Formatter


class FzfCommand(BaseCommand):
    name = "fzf"
    help_text = "Interactive fuzzy search interface using fzf (supports tmux popups)."

    @classmethod
    def configure_parser(cls, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "query", nargs="?", default="", help="Initial search filter"
        )
        parser.add_argument("-c", "--category", help="Filter by category")
        parser.add_argument(
            "--copy",
            action="store_true",
            help="Copy selected snippet directly to clipboard",
        )
        parser.add_argument(
            "--print",
            action="store_true",
            default=True,
            help="Print selected snippet raw to stdout",
        )

    def execute(self, args: argparse.Namespace) -> int:
        in_tmux = "TMUX" in os.environ

        if in_tmux and shutil.which("fzf-tmux"):
            fzf_cmd = ["fzf-tmux", "-p", "85%,70%"]
        elif shutil.which("fzf"):
            fzf_cmd = ["fzf"]
        else:
            fzf_cmd = None

        if fzf_cmd is None:
            print(
                Formatter.color(
                    "Error: 'fzf' is not installed or not found on PATH.",
                    Formatter.RED,
                )
            )
            print(
                Formatter.color(
                    "Please install fzf via: brew install fzf (or apt install fzf)",
                    Formatter.YELLOW,
                )
            )
            return 1

        items = self.service.list_items(limit=10000, category=args.category)

        if not items:
            print(
                Formatter.color(
                    "No knowledge base items available.",
                    Formatter.YELLOW,
                )
            )
            return 0

        input_lines = []
        for item in items:
            tags_part = f" ({item.tags_str})" if item.tags else ""
            input_lines.append(
                f"{item.id}\t[{item.category.upper()}]\t{item.title}{tags_part}"
            )

        input_str = "\n".join(input_lines)

        cmd = fzf_cmd + [
            "--delimiter=\t",
            "--with-nth=2,3",
            "--preview=kb get {1}",
            "--preview-window=right:55%:wrap",
            "--header=Select snippet (Enter to insert/copy, Esc to cancel)",
        ]

        if args.query:
            cmd.extend(["-q", args.query])

        try:
            process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            stdout, _ = process.communicate(input=input_str)

            if process.returncode != 0 or not stdout.strip():
                return 1

            selected_id = int(stdout.strip().split("\t")[0])

            selected_item = self.service.get_item(
                selected_id,
                track_access=True,
            )

            if selected_item is None:
                return 1

            if args.copy:
                copy_to_clipboard(selected_item.content)
                print(
                    Formatter.color(
                        f"✔ Copied snippet #{selected_item.id} to clipboard!",
                        Formatter.GREEN,
                    ),
                    file=sys.stderr,
                )
            else:
                print(selected_item.content)

            return 0

        except (OSError, ValueError, subprocess.SubprocessError) as exc:
            print(
                Formatter.color(
                    f"Error launching fzf: {exc}",
                    Formatter.RED,
                ),
                file=sys.stderr,
            )
            return 1
