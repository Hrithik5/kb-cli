# `kb` Development Guide

## Testing

Run tests via Python standard library:

```bash
python3 tests/run_tests.py
```

Or via `pytest`:

```bash
make test
```

## Adding a New Subcommand

1. Create new command class in `kb/commands/mycmd.py` inheriting from `BaseCommand`.
2. Implement `configure_parser()` and `execute()`.
3. Register class in `COMMAND_CLASSES` list in `kb/cli.py`.
4. Add test case in `tests/test_cli.py`.
