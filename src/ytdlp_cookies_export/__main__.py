"""入口：python -m ytdlp_cookies_export 或 ytdlp-cookies-export 命令。"""

from .app import run_gui


def main() -> None:
    run_gui()


if __name__ == "__main__":
    main()
