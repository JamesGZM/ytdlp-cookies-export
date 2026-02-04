# PyInstaller spec：打包为单可执行文件
# 使用：pyinstaller ytdlp_cookies_export.spec

a = Analysis(
    ["src/ytdlp_cookies_export/__main__.py"],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=["yt_dlp"],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="ytdlp-cookies-export",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # 设为 False 可隐藏控制台（仅 GUI）
)
