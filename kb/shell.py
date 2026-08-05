import atexit
import readline
from pathlib import Path

from kb.services.knowledge_service import KnowledgeService
from kb.shell_commands import ShellCommands
from kb.utils.formatter import Formatter


class InteractiveShell:
    """Interactive REPL for kb."""

    def __init__(self, service: KnowledgeService, config):
        self.commands = ShellCommands(service, config.editor)

        self.history_file = Path.home() / ".kb_history"

        self.command_names = [
            "help",
            "?",
            "list",
            "ls",
            "find",
            "get",
            "stats",
            "recent",
            "favorites",
            "favs",
            "favorite",
            "fav",
            "add",
            "edit",
            "delete",
            "del",
            "exit",
            "quit",
            "q",
        ]

        self._setup_readline()

    # ---------------------------------------------------------
    # Readline
    # ---------------------------------------------------------

    def _setup_readline(self) -> None:
        readline.set_history_length(1000)

        if self.history_file.exists():
            try:
                readline.read_history_file(self.history_file)
            except OSError:
                pass

        readline.parse_and_bind("tab: complete")
        readline.set_completer(self._complete)

        atexit.register(self._save_history)

    def _save_history(self) -> None:
        try:
            readline.write_history_file(self.history_file)
        except OSError:
            pass

    def _complete(self, text: str, state: int):
        matches = [cmd for cmd in self.command_names if cmd.startswith(text)]

        if state < len(matches):
            return matches[state]

        return None

    # ---------------------------------------------------------
    # REPL
    # ---------------------------------------------------------

    def run(self) -> int:
        print(
            Formatter.color(
                "\n⚡ Welcome to kb Interactive Mode",
                Formatter.CYAN + Formatter.BOLD,
            )
        )

        print("Type 'help' for commands.")
        print("Type 'exit' to quit.\n")

        while True:
            try:
                prompt = Formatter.color(
                    "kb",
                    Formatter.CYAN + Formatter.BOLD,
                ) + Formatter.color(
                    " ❯ ",
                    Formatter.GREEN,
                )

                line = input(prompt).strip()

            except (EOFError, KeyboardInterrupt):
                print()
                break

            if not line:
                continue

            parts = line.split(maxsplit=1)

            command = parts[0].lower()
            argument = parts[1] if len(parts) > 1 else ""

            try:
                if command in {"exit", "quit", "q"}:
                    break

                elif command in {"help", "?"}:
                    self.commands.help()

                elif command in {"list", "ls"}:
                    self.commands.list()

                elif command == "recent":
                    self.commands.recent()

                elif command in {"favorites", "favs"}:
                    self.commands.favorites()

                elif command == "stats":
                    self.commands.stats()

                elif command == "find":
                    if not argument:
                        print(
                            Formatter.color(
                                "Usage: find <query>",
                                Formatter.YELLOW,
                            )
                        )
                    else:
                        self.commands.find(argument)

                elif command == "get":
                    if not argument:
                        print(
                            Formatter.color(
                                "Usage: get <id>",
                                Formatter.YELLOW,
                            )
                        )
                    else:
                        self.commands.get(int(argument))

                elif command == "add":
                    self.commands.add()

                elif command == "edit":
                    if not argument:
                        print(
                            Formatter.color(
                                "Usage: edit <id>",
                                Formatter.YELLOW,
                            )
                        )
                    else:
                        self.commands.edit(int(argument))

                elif command in {"favorite", "fav"}:
                    if not argument:
                        print(
                            Formatter.color(
                                "Usage: favorite <id>",
                                Formatter.YELLOW,
                            )
                        )
                    else:
                        self.commands.favorite(int(argument))

                elif command in {"delete", "del"}:
                    if not argument:
                        print(
                            Formatter.color(
                                "Usage: delete <id>",
                                Formatter.YELLOW,
                            )
                        )
                    else:
                        self.commands.delete(int(argument))

                else:
                    print(
                        Formatter.color(
                            "Unknown command. Type 'help'.",
                            Formatter.YELLOW,
                        )
                    )

            except ValueError:
                print(
                    Formatter.color(
                        "Invalid command arguments.",
                        Formatter.RED,
                    )
                )

        print(
            Formatter.color(
                "Goodbye 👋",
                Formatter.GREEN,
            )
        )

        return 0
