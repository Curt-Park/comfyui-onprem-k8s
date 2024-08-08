import os


def setup_comfyui_server():
    def _get_env(port: int) -> dict[str, str]:
        return {}

    def _get_icon_path() -> str:
        return os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "icons", "comfyui.svg"
        )

    def _get_cmd(port: int) -> list[str]:
        # required:
        #   - ComfyUI repo in "/home/workspace/ComfyUI"
        #   - ENV PATH="$PATH:/home/workspace/ComfyUI" in Dockerfile
        return [
            "python3.10",
            "/home/workspace/ComfyUI/main.py",
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
