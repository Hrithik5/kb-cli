# Zsh plugin for interactive kb fzf search with tmux support
# Bind Ctrl+K to open interactive kb snippet picker and insert into prompt

__kb_fzf_select() {
    local selected
    selected=$(kb fzf --print)
    if [ -n "$selected" ]; then
        LBUFFER="${LBUFFER}${selected}"
    fi
    zle reset-prompt
}

zle -N __kb_fzf_select
bindkey '^K' __kb_fzf_select
