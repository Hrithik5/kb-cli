import subprocess
import sys


def copy_to_clipboard(text: str) -> bool:
    """Copies text to system clipboard using native tools without external pip dependencies."""
    try:
        if sys.platform == "darwin":
            process = subprocess.Popen(["pbcopy"], stdin=subprocess.PIPE)
            process.communicate(text.encode("utf-8"))
            return process.returncode == 0

        if sys.platform.startswith("linux"):
            # Try Wayland first
            try:
                process = subprocess.Popen(["wl-copy"], stdin=subprocess.PIPE)
                process.communicate(text.encode("utf-8"))
                if process.returncode == 0:
                    return True
            except FileNotFoundError:
                pass

            # Fallback to X11
            process = subprocess.Popen(
                ["xclip", "-selection", "clipboard"],
                stdin=subprocess.PIPE,
            )
            process.communicate(text.encode("utf-8"))
            return process.returncode == 0

        if sys.platform == "win32":
            process = subprocess.Popen(["clip"], stdin=subprocess.PIPE)
            process.communicate(text.encode("utf-8"))
            return process.returncode == 0

    except (FileNotFoundError, OSError):
        return False

    return False
