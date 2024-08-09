import os
import logging


def setup_comfyui_server():
    def _get_env(port: int) -> dict[str, str]:
        return {}

    def _get_icon_path() -> str:
        return os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "icons", "comfyui.svg"
        )

    def _get_cmd(port: int) -> list[str]:
        # required (in Dockerfile):
        #   - $PYTHON
        #   - $COMFYUI_PATH
        #   - PATH=$PATH:$COMFYUI_PATH
        PYTHON = os.getenv("PYTHON", "python3.10")
        COMFYUI_PATH = os.getenv("COMFYUI_PATH", os.path.join("home", "workspace", "ComfyUI"))
        logging.info("PYTHON: %s, COMFYUI_PATH: %s", PYTHON, COMFYUI_PATH)
        return [
            PYTHON,
            os.path.join(COMFYUI_PATH, "main.py"),
            "--listen=0.0.0.0",
            f"--port={port}",
        ]

    def _get_timeout(default: int = 30) -> float:
        try:
            return float(os.getenv("COMFYUI_SESSION_TIMEOUT", default))
        except Exception:
            return default

    return {
        "command": _get_cmd,
        "timeout": _get_timeout(),
        "environment": _get_env,
        "new_browser_tab": True,
        "launcher_entry": {"title": "ComfyUI", "icon_path": _get_icon_path()},
    }
