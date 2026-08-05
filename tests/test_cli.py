from kb.cli import run_cli


def test_cli_help(capsys):
    status = run_cli(["--help"])
    assert status == 0
    captured = capsys.readouterr()
    assert "kb — Developer Knowledge Engine CLI" in captured.out


def test_cli_crud_flow(tmp_path, capsys):
    config_file = tmp_path / "config.toml"
    db_file = tmp_path / "kb_test.db"
    config_file.write_text(f'database = "{db_file}"\n', encoding="utf-8")

    # init
    ret = run_cli(["--config-file", str(config_file), "init"])
    assert ret == 0

    # add
    ret = run_cli(["--config-file", str(config_file), "add", "git", "git status", "-t", "Status", "--tags", "git,status"])
    assert ret == 0

    # find
    ret = run_cli(["--config-file", str(config_file), "find", "status"])
    assert ret == 0
    captured = capsys.readouterr()
    assert "Status" in captured.out

    # stats
    ret = run_cli(["--config-file", str(config_file), "stats"])
    assert ret == 0

    # get
    ret = run_cli(["--config-file", str(config_file), "get", "1"])
    assert ret == 0

    # completion
    ret = run_cli(["--config-file", str(config_file), "completion", "zsh"])
    assert ret == 0

    # delete
    ret = run_cli(["--config-file", str(config_file), "delete", "1"])
    assert ret == 0
