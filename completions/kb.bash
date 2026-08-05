# bash completion for kb

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
