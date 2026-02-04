"""GUI：选择浏览器与保存路径，导出 cookies.txt（仅导出，不下载）。"""

from __future__ import annotations

import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import Callable

# yt-dlp 支持的浏览器（与 --cookies-from-browser 一致）
SUPPORTED_BROWSERS = [
    "brave",
    "chrome",
    "chromium",
    "edge",
    "firefox",
    "opera",
    "safari",
    "vivaldi",
    "whale",
]

# 用于触发一次元数据请求的轻量 URL（仅 simulate，不下载）
TRIGGER_URL = "bilibili.com/video/BV1AM4y1M71p/"


def export_cookies(browser: str, cookiefile: str, log_cb: Callable[[str], None]) -> str | None:
    """
    从指定浏览器导出 cookie 到文件（Netscape 格式）。仅导出，不下载视频。

    使用 yt-dlp：load_cookies 从浏览器读取，close() 时 save_cookies() 写入文件。
    通过 simulate + extract_info 触发一次轻量请求后退出，从而写入 cookie。

    :param browser: 浏览器名称，如 'chrome', 'firefox'
    :param cookiefile: 保存路径，如 cookies.txt
    :param log_cb: 日志回调，用于在 GUI 显示进度
    :return: 成功返回 None，失败返回错误信息字符串
    """
    try:
        from yt_dlp import YoutubeDL
    except ImportError as e:
        return f"未安装 yt-dlp: {e}"

    if not browser or not cookiefile:
        return "请选择浏览器和保存路径"

    cookiefile = os.path.abspath(cookiefile)
    log_cb(f"正在从 {browser} 读取 cookie …")

    params = {
        "cookiefile": cookiefile,
        "cookiesfrombrowser": (browser,),
        "simulate": True,
        "quiet": True,
        "no_warnings": True,
    }

    class LogLogger:
        def __init__(self, cb: Callable[[str], None]):
            self._cb = cb

        def debug(self, msg: str) -> None:
            self._cb(msg)

        def info(self, msg: str) -> None:
            self._cb(msg)

        def warning(self, msg: str) -> None:
            self._cb(f"[警告] {msg}")

        def error(self, msg: str) -> None:
            self._cb(f"[错误] {msg}")

    params["logger"] = LogLogger(log_cb)

    ydl = None
    try:
        ydl = YoutubeDL(params)
        # 触发一次元数据请求，使 cookie jar 被使用；simulate=True 不下载
        log_cb("正在执行一次轻量请求以写入 cookie …")
        ydl.extract_info(TRIGGER_URL, download=False)
    except Exception as e:
        err = str(e).strip() or repr(e)
        if "cookie" in err.lower() or "could not copy" in err.lower() or "permission" in err.lower():
            return f"无法读取浏览器 cookie。请先关闭 {browser} 后重试。\n\n{err}"
        return err
    finally:
        if ydl is not None:
            try:
                ydl.close()  # 触发 save_cookies() 写入 cookiefile
            except Exception:
                pass

    log_cb(f"已保存到 {cookiefile}")
    return None


def run_gui() -> None:
    """启动 tkinter GUI。"""
    root = tk.Tk()
    root.title("导出浏览器 cookies.txt")
    root.minsize(400, 280)
    root.resizable(True, True)

    main = ttk.Frame(root, padding=12)
    main.pack(fill=tk.BOTH, expand=True)

    # 浏览器
    ttk.Label(main, text="浏览器:").grid(row=0, column=0, sticky=tk.W, pady=(0, 4))
    browser_var = tk.StringVar(value="chrome")
    browser_combo = ttk.Combobox(
        main,
        textvariable=browser_var,
        values=SUPPORTED_BROWSERS,
        state="readonly",
        width=20,
    )
    browser_combo.grid(row=1, column=0, sticky=tk.EW, pady=(0, 12))

    # 保存路径
    ttk.Label(main, text="保存路径:").grid(row=2, column=0, sticky=tk.W, pady=(0, 4))
    path_var = tk.StringVar(value=os.path.join(os.path.expanduser("~"), "cookies.txt"))
    path_frame = ttk.Frame(main)
    path_frame.grid(row=3, column=0, sticky=tk.EW, pady=(0, 12))
    main.columnconfigure(0, weight=1)
    path_frame.columnconfigure(0, weight=1)

    path_entry = ttk.Entry(path_frame, textvariable=path_var)
    path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))

    def choose_path() -> None:
        p = filedialog.asksaveasfilename(
            title="选择 cookies.txt 保存位置",
            defaultextension=".txt",
            filetypes=[("Netscape cookies", "*.txt"), ("所有文件", "*.*")],
            initialfile="cookies.txt",
            initialdir=os.path.dirname(path_var.get()) or os.path.expanduser("~"),
        )
        if p:
            path_var.set(p)

    ttk.Button(path_frame, text="浏览…", command=choose_path).pack(side=tk.RIGHT)

    # 导出按钮（后台线程执行，不卡 UI）
    export_btn = ttk.Button(main, text="导出 cookies.txt", command=lambda: None)
    export_btn.grid(row=4, column=0, pady=(0, 12))

    def do_export() -> None:
        browser = browser_var.get().strip().lower()
        path = path_var.get().strip()
        if not path:
            messagebox.showwarning("提示", "请选择保存路径。")
            return
        log_area.configure(state=tk.NORMAL)
        log_area.delete("1.0", tk.END)
        log_area.configure(state=tk.DISABLED)
        export_btn.configure(state=tk.DISABLED)

        def log(msg: str) -> None:
            root.after(0, _append_log, msg)

        def _append_log(msg: str) -> None:
            log_area.configure(state=tk.NORMAL)
            log_area.insert(tk.END, msg + "\n")
            log_area.see(tk.END)
            log_area.configure(state=tk.DISABLED)

        def on_done(err: str | None) -> None:
            export_btn.configure(state=tk.NORMAL)
            if err:
                messagebox.showerror("导出失败", err)
            else:
                messagebox.showinfo("完成", f"cookies 已导出到:\n{os.path.abspath(path)}")

        def work() -> None:
            err = export_cookies(browser, path, log)
            root.after(0, on_done, err)

        threading.Thread(target=work, daemon=True).start()

    export_btn.configure(command=do_export)

    # 日志区域
    ttk.Label(main, text="日志:").grid(row=5, column=0, sticky=tk.W, pady=(0, 4))
    log_frame = ttk.Frame(main)
    log_frame.grid(row=6, column=0, sticky=tk.NSEW, pady=(0, 0))
    main.rowconfigure(6, weight=1)
    main.columnconfigure(0, weight=1)
    log_frame.columnconfigure(0, weight=1)
    log_frame.rowconfigure(0, weight=1)

    log_area = tk.Text(log_frame, height=6, wrap=tk.WORD, state=tk.DISABLED, font=("", 10))
    log_area.grid(row=0, column=0, sticky=tk.NSEW)
    scroll = ttk.Scrollbar(log_frame, command=log_area.yview)
    scroll.grid(row=0, column=1, sticky=tk.NS)
    log_area.configure(yscrollcommand=scroll.set)

    root.mainloop()


if __name__ == "__main__":
    run_gui()
