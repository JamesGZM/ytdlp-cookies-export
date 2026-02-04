# ytdlp-cookies-export

从浏览器导出 **Netscape 格式** 的 `cookies.txt`，供 [yt-dlp](https://github.com/yt-dlp/yt-dlp) 使用。**仅做导出，不下载任何视频。**

**[📦 下载 Windows / macOS / Linux 可执行文件](https://github.com/JamesGZM/ytdlp-cookies-export/releases)**（进入 Release 页的 Assets 即可下载，无需安装 Python）

### 各平台可执行文件使用步骤

| 平台   | 文件名                         | 操作步骤 |
|--------|--------------------------------|----------|
| Windows | `ytdlp-cookies-export.exe`     | 1. 下载后放到任意目录<br>2. 双击运行，或在资源管理器中选中后回车；若遇「无法验证发布者」可点「更多信息」→「仍要运行」 |
| macOS   | `ytdlp-cookies-export-macos`   | 1. 下载后放到任意目录（如 `~/Downloads`）<br>2. 终端执行：`chmod +x ytdlp-cookies-export-macos` 赋予执行权限<br>3. 运行：`./ytdlp-cookies-export-macos`；若提示「无法打开」可到 系统设置 → 隐私与安全性 → 仍要打开 |
| Linux   | `ytdlp-cookies-export-linux`   | 1. 下载后放到任意目录<br>2. 终端执行：`chmod +x ytdlp-cookies-export-linux` 赋予执行权限<br>3. 运行：`./ytdlp-cookies-export-linux` |

运行后会弹出 GUI 窗口，选择浏览器与保存路径后点击「导出 cookies.txt」即可。

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
