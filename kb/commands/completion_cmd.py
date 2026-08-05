import argparse
from kb.commands.base import BaseCommand


ZSH_COMPLETION = """#compdef kb

_kb_subcommands=(
    'init:Initialize database and configuration'
    'add:Add a new knowledge entry or snippet'
    'find:Search knowledge base entries using FTS5'
    'list:List knowledge base items'
    'edit:Edit an existing entry by ID'
    'delete:Delete an entry by ID'
    'import:Import notes from markdown or txt files'
    'export:Export entries to JSON, Markdown, or backup'
    'stats:Display knowledge base statistics'
    'favorite:Toggle favorite status or list favorites'
    'recent:Show recently added or updated entries'
    'copy:Copy snippet content to system clipboard'
    'fzf:Interactive fuzzy search interface (supports tmux)'
    'get:Get raw snippet content by ID'
    'completion:Generate shell autocompletion script'
)

_kb() {
    local curcontext="$curcontext" state line
    typeset -A opt_args

    _arguments -C \\
        '(-v --version)'{-v,--version}'[Show version]' \\
        '--config-file[Specify path to custom config file]:file:_files' \\
        '1: :->command' \\
        '*: :->args'

    case $state in
        command)
            _describe -t commands 'kb command' _kb_subcommands
            ;;
        args)
            case $line[1] in
                add|find|list|import|export|fzf)
                    _arguments '-c[Category]:category:' '--category[Category]:category:'
                    ;;
                completion)
                    _values 'shell' bash zsh fish
                    ;;
            esac
            ;;
    esac
}

_kb "$@"
"""

BASH_COMPLETION = """# bash completion for kb

_kb_completions() {
    local cur prev opts commands
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"

    commands="init add find list edit delete import export stats favorite recent copy fzf get completion"

    if [ $COMP_CWORD -eq 1 ]; then
        COMPREPLY=( $(compgen -W "${commands}" -- ${cur}) )
        return 0
    fi

    case "${prev}" in
        import)
            COMPREPLY=( $(compgen -W "markdown txt" -- ${cur}) )
            return 0
            ;;
        export)
            COMPREPLY=( $(compgen -W "json markdown backup" -- ${cur}) )
            return 0
            ;;
        completion)
            COMPREPLY=( $(compgen -W "bash zsh fish" -- ${cur}) )
            return 0
            ;;
        -c|--category)
            return 0
            ;;
    esac
}

complete -F _kb_completions kb
"""

FISH_COMPLETION = """# fish completion for kb

set -l commands init add find list edit delete import export stats favorite recent copy fzf get completion

complete -c kb -f

# Subcommands
complete -c kb -n "not __fish_seen_subcommand_from $commands" -a init -d "Initialize database"
complete -c kb -n "not __fish_seen_subcommand_from $commands" -a add -d "Add snippet or note"
complete -c kb -n "not __fish_seen_subcommand_from $commands" -a find -d "Search entries via FTS5"
complete -c kb -n "not __fish_seen_subcommand_from $commands" -a list -d "List entries"
complete -c kb -n "not __fish_seen_subcommand_from $commands" -a edit -d "Edit entry"
complete -c kb -n "not __fish_seen_subcommand_from $commands" -a delete -d "Delete entry"
complete -c kb -n "not __fish_seen_subcommand_from $commands" -a import -d "Import files"
complete -c kb -n "not __fish_seen_subcommand_from $commands" -a export -d "Export database"
complete -c kb -n "not __fish_seen_subcommand_from $commands" -a stats -d "View statistics"
complete -c kb -n "not __fish_seen_subcommand_from $commands" -a favorite -d "Manage favorites"
complete -c kb -n "not __fish_seen_subcommand_from $commands" -a recent -d "View recent items"
complete -c kb -n "not __fish_seen_subcommand_from $commands" -a copy -d "Copy to clipboard"
complete -c kb -n "not __fish_seen_subcommand_from $commands" -a fzf -d "Interactive fzf interface"
complete -c kb -n "not __fish_seen_subcommand_from $commands" -a completion -d "Generate completion script"

# Options
complete -c kb -s c -l category -d "Category filter" -r
complete -c kb -s v -l version -d "Show version"
"""


class CompletionCommand(BaseCommand):
    name = "completion"
    help_text = "Generate shell autocompletion scripts (bash, zsh, fish)."

    @classmethod
    def configure_parser(cls, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("shell", choices=["bash", "zsh", "fish"], help="Target shell language")

    def execute(self, args: argparse.Namespace) -> int:
        if args.shell == "zsh":
            print(ZSH_COMPLETION.strip())
        elif args.shell == "bash":
            print(BASH_COMPLETION.strip())
        elif args.shell == "fish":
            print(FISH_COMPLETION.strip())
        return 0
