"""入口：python -m ytdlp_cookies_export 或 ytdlp-cookies-export 命令。"""

# 使用绝对导入，避免 PyInstaller 打包后「relative import with no known parent package」
from ytdlp_cookies_export.app import run_gui


def main() -> None:
    run_gui()


if __name__ == "__main__":
    main()
