import argparse
import os
import shlex
import shutil
import subprocess
import sys

from kb.commands.base import BaseCommand
from kb.utils.clipboard import copy_to_clipboard
from kb.utils.formatter import Formatter


class FzfCommand(BaseCommand):
    name = "fzf"
    help_text = "Interactive fuzzy finder for the knowledge base."

    @classmethod
    def configure_parser(cls, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "query",
            nargs="?",
            default="",
            help="Initial search query",
        )

        parser.add_argument(
            "-c",
            "--category",
            help="Filter by category",
        )

        parser.add_argument(
            "--copy",
            action="store_true",
            help="Copy selected snippet to clipboard",
        )

        parser.add_argument(
            "--print",
            action="store_true",
            default=True,
            help="Print selected snippet",
        )

    def execute(self, args: argparse.Namespace) -> int:
        in_tmux = "TMUX" in os.environ

        if in_tmux and shutil.which("fzf-tmux"):
            fzf_cmd = ["fzf-tmux", "-p", "90%,80%"]
        elif shutil.which("fzf"):
            fzf_cmd = ["fzf"]
        else:
            print(
                Formatter.color(
                    "Error: fzf is not installed.",
                    Formatter.RED,
                )
            )
            print(
                Formatter.color(
                    "Install it with: brew install fzf",
                    Formatter.YELLOW,
                )
            )
            return 1

        items = self.service.list_items(
            limit=10000,
            category=args.category,
        )

        if not items:
            print(
                Formatter.color(
                    "Knowledge base is empty.",
                    Formatter.YELLOW,
                )
            )
            return 0

        rows = []

        for item in items:
            star = "★" if item.favorite else " "

            tags = f"[{item.tags_str}]" if item.tags else ""

            rows.append(
                f"{item.id}\t"
                f"{star}\t"
                f"{item.category.upper():<10}\t"
                f"{item.title:<40}\t"
                f"{tags}"
            )
        input_text = "\n".join(rows)

        python_cmd = shlex.quote(sys.executable)

        preview_cmd = (
            "if command -v bat >/dev/null 2>&1; "
            f"then {python_cmd} -m kb.cli get {{1}} "
            "| bat --paging=never --style=plain --language=markdown; "
            f"else {python_cmd} -m kb.cli get {{1}}; "
            "fi"
        )

        cmd = fzf_cmd + [
            "--ansi",
            "--layout=reverse-list",
            "--info=inline-right",
            "--cycle",
            "--scrollbar=▌",
            "--bind=ctrl-u:preview-half-page-up",
            "--bind=ctrl-d:preview-half-page-down",
            "--height=100%",
            "--border=rounded",
            "--delimiter=\t",
            "--with-nth=2,3,4",
            "--pointer=▶",
            "--marker=✓",
            "--prompt=kb ❯ ",
            "--preview=" + preview_cmd,
            "--preview-window=right,60%,border-rounded,wrap",
            "--expect=ctrl-y",
            "--header=Enter: View │ Ctrl-Y: Copy │ Ctrl-E: Edit │ Esc: Quit",
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

            stdout, _ = process.communicate(input=input_text)

            if process.returncode != 0 or not stdout.strip():
                return 1

            lines = stdout.strip().splitlines()

            key = ""

            if len(lines) == 1:
                selected_line = lines[0]
            else:
                key = lines[0]
                selected_line = lines[1]

            selected_id = int(selected_line.split("\t")[0])

            item = self.service.get_item(
                selected_id,
                track_access=True,
            )

            if item is None:
                return 1

            if key == "ctrl-y" or args.copy:
                if copy_to_clipboard(item.content):
                    print(
                        Formatter.color(
                            f"✔ Copied snippet #{item.id} to clipboard.",
                            Formatter.GREEN,
                        ),
                        file=sys.stderr,
                    )
                else:
                    print(
                        Formatter.color(
                            "Failed to copy to clipboard.",
                            Formatter.RED,
                        ),
                        file=sys.stderr,
                    )
                    return 1
            else:
                print(item.content)

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
