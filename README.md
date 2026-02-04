# ytdlp-cookies-export

从浏览器导出 **Netscape 格式** 的 `cookies.txt`，供 [yt-dlp](https://github.com/yt-dlp/yt-dlp) 使用。**仅做导出，不下载任何视频。**

## 功能

- GUI 选择浏览器（Chrome、Firefox、Edge、Brave 等）
- 选择保存路径（默认 `cookies.txt`）
- 一键导出：使用 yt-dlp 的 `--cookies-from-browser` 与 `--cookies` 逻辑，将浏览器 cookie 写入指定文件

## 支持的浏览器

与 yt-dlp 一致：`brave`, `chrome`, `chromium`, `edge`, `firefox`, `opera`, `safari`, `vivaldi`, `whale`。

## 安装与运行

在项目目录下（或从 monorepo 根目录进入 `vendor/ytdlp-cookies-export`）：

```bash
# 使用 uv（推荐）
uv pip install -e .
python -m ytdlp_cookies_export

# 或直接运行
uv run python -m ytdlp_cookies_export
```

若已安装为可执行包：

```bash
ytdlp-cookies-export
```

## 打包为单可执行文件

依赖 [PyInstaller](https://pyinstaller.org/)。在 **各目标平台** 上分别构建：

```bash
uv pip install pyinstaller
pyinstaller --onefile -n ytdlp-cookies-export src/ytdlp_cookies_export/__main__.py
```

产物在 `dist/ytdlp-cookies-export`（Windows 为 `dist/ytdlp-cookies-export.exe`）。

- 无控制台窗口（仅 GUI）：加 `--windowed`（Windows）/ `--noconsole`（macOS）。
- 若需包含 yt-dlp 的 EJS/Deno 等可选依赖，可先 `uv pip install "yt-dlp[default]"` 再打包。

## 注意事项

- 会读取本地浏览器 Cookie，涉及敏感数据，请仅在本机使用，勿将导出的 `cookies.txt` 分发给他人。
- 若提示无法读取 cookie，请先**关闭对应浏览器**后重试（浏览器会锁定 Cookie 数据库）。
- 导出时会执行一次轻量元数据请求以触发 yt-dlp 的保存逻辑，不会下载视频。
