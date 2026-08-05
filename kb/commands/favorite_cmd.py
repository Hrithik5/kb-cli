import argparse
from kb.commands.base import BaseCommand
from kb.utils.formatter import Formatter


class FavoriteCommand(BaseCommand):
    name = "favorite"
    help_text = "Toggle favorite status of an entry or list all favorites."

    @classmethod
    def configure_parser(cls, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("id", type=int, nargs="?", help="Item ID to toggle favorite status")
        parser.add_argument("-l", "--list", action="store_true", help="List all favorite entries")

    def execute(self, args: argparse.Namespace) -> int:
        if args.list or args.id is None:
            favs = self.service.get_favorites()
            print(Formatter.format_items_list(favs))
            return 0

        new_status = self.service.toggle_favorite(args.id)
        if new_status is None:
            print(Formatter.color(f"Error: Item #{args.id} not found.", Formatter.RED))
            return 1
        elif new_status:
            print(Formatter.color(f"★ Marked #{args.id} as favorite.", Formatter.YELLOW))
        else:
            print(Formatter.color(f"Unmarked #{args.id} from favorites.", Formatter.DIM))
        return 0
