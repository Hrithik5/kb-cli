# Bash plugin for interactive kb fzf search with tmux support
# Bind Ctrl+K to open interactive kb snippet picker and insert into prompt

__kb_fzf_select_bash() {
    local selected
    selected=$(kb fzf --print)
    if [ -n "$selected" ]; then
        READLINE_LINE="${READLINE_LINE:0:$READLINE_POINT}${selected}${READLINE_LINE:$READLINE_POINT}"
        READLINE_POINT=$((READLINE_POINT + ${#selected}))
    fi
}

bind -x '"\C-k": __kb_fzf_select_bash'
