import os
import sys
from dataclasses import dataclass
from pathlib import Path

if sys.version_info >= (3, 11):
    import tomllib

    TOMLDecodeError = tomllib.TOMLDecodeError
else:
    try:
        import tomllib  # type: ignore

        TOMLDecodeError = tomllib.TOMLDecodeError
    except ImportError:
        tomllib = None  # Handled via fallback parser

        class TOMLDecodeError(Exception):
            """Fallback TOML decode error."""


@dataclass
class Config:
    database_path: Path
    editor: str = "nvim"
    default_limit: int = 10
    theme: str = "default"
    pager: str = "less"

    @classmethod
    def get_config_dir(cls) -> Path:
        config_home = os.environ.get("XDG_CONFIG_HOME")
        if config_home:
            return Path(config_home) / "kb"
        return Path.home() / ".config" / "kb"

    @classmethod
    def get_data_dir(cls) -> Path:
        data_home = os.environ.get("XDG_DATA_HOME")
        if data_home:
            return Path(data_home) / "kb"
        return Path.home() / ".local" / "share" / "kb"

    @classmethod
    def load(cls, config_path: Path | None = None) -> "Config":
        if isinstance(config_path, str):
            config_path = Path(config_path)

        if config_path is None:
            config_path = cls.get_config_dir() / "config.toml"

        data_dir = cls.get_data_dir()
        default_db = data_dir / "kb.db"
        editor = os.environ.get("EDITOR", os.environ.get("VISUAL", "vim"))

        cfg = cls(database_path=default_db, editor=editor)

        if not config_path.exists():
            return cfg

        try:
            content = config_path.read_text(encoding="utf-8")

            if tomllib:
                data = tomllib.loads(content)
            else:
                data = cls._parse_simple_toml(content)

            if "database" in data:
                db_str = os.path.expanduser(str(data["database"]))
                cfg.database_path = Path(db_str)

            if "editor" in data:
                cfg.editor = str(data["editor"])

            if "default_limit" in data:
                cfg.default_limit = int(data["default_limit"])

            if "theme" in data:
                cfg.theme = str(data["theme"])

            if "pager" in data:
                cfg.pager = str(data["pager"])

        except (OSError, TOMLDecodeError):
            # Fall back to default configuration.
            return cfg

        return cfg

    @staticmethod
    def _parse_simple_toml(content: str) -> dict:
        """Fallback key-value parser for simple config when tomllib is missing on Python 3.10."""
        result = {}

        for line in content.splitlines():
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            if "=" in line:
                key, val = line.split("=", 1)
                key = key.strip()
                val = val.strip().strip('"').strip("'")
                result[key] = val

        return result

    def save_default_config(self, config_path: Path | None = None) -> Path:
        if config_path is None:
            config_path = self.get_config_dir() / "config.toml"

        config_path.parent.mkdir(parents=True, exist_ok=True)

        if not config_path.exists():
            content = (
                "# kb configuration file\n"
                f'database = "{self.database_path}"\n'
                f'editor = "{self.editor}"\n'
                f"default_limit = {self.default_limit}\n"
                f'theme = "{self.theme}"\n'
                f'pager = "{self.pager}"\n'
            )

            config_path.write_text(content, encoding="utf-8")

        return config_path
