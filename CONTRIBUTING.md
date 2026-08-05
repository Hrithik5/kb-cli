# Contributing to `kb`

Thank you for considering contributing to `kb`! We are building a clean, lightning-fast developer knowledge engine.

## 🛠️ Development Setup

1. Fork and clone the repository:
   ```bash
   git clone https://github.com/your-username/kb-cli.git
   cd kb-cli
   ```

2. Set up virtual environment and install in editable mode:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -e ".[dev]"
   ```

3. Run the test suite:
   ```bash
   python3 tests/run_tests.py
   ```

## 📐 Coding Guidelines

- **Zero Runtime Dependencies**: The core engine must depend only on Python standard libraries (`sqlite3`, `argparse`, `dataclasses`, `pathlib`).
- **Layer Separation**: Commands must not execute raw SQL; repositories must not perform CLI printing.
- **Test Coverage**: Every new command or service method must include tests.

## 🚀 Submitting a Pull Request

1. Create a feature branch: `git checkout -b feature/my-new-feature`
2. Commit your changes: `git commit -am 'Add new feature'`
3. Push to your branch: `git push origin feature/my-new-feature`
4. Open a Pull Request on GitHub.
