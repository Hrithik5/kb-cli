# fish completion for kb

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
