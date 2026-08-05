import sys

from kb.cli import run_cli


def main() -> None:
    try:
        sys.exit(run_cli())
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
        raise SystemExit(130)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
