class Kb < Formula
  desc "Lightning-fast offline developer knowledge engine powered by SQLite FTS5"
  homepage "https://github.com/hrithikchauhan/kb-cli"
  url "https://github.com/hrithikchauhan/kb-cli/archive/refs/tags/v0.1.0.tar.gz"
  sha256 "0000000000000000000000000000000000000000000000000000000000000000" # Updated on release
  license "MIT"

  depends_on "python@3.12"
  depends_on "fzf" => :recommended

  def install
    virtualenv_install_with_resources

    # Install shell completions
    bash_completion.install "completions/kb.bash" => "kb"
    zsh_completion.install "completions/_kb" => "_kb"
    fish_completion.install "completions/kb.fish" => "kb.fish"
  end

  test do
    assert_match "kb version", shell_output("#{bin}/kb --version")
    assert_match "Initialized kb database", shell_output("#{bin}/kb init")
  end
end
