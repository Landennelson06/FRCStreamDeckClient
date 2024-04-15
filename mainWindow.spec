# -*- mode: python ; coding: utf-8 -*-

added_files = [
        ("assets/0.png", "assets"),
        ("assets/1.png", "assets"),
        ("assets/2.png", "assets"),
        ("assets/3.png", "assets"),
        ("assets/4.png", "assets"),
        ("assets/5.png", "assets"),
        ("assets/6.png", "assets"),
        ("assets/7.png", "assets"),
        ("assets/8.png", "assets"),
        ("assets/9.png", "assets"),
        ("assets/10.png", "assets"),
        ("assets/11.png", "assets"),
        ("assets/12.png", "assets"),
        ("assets/13.png", "assets"),
        ("assets/14.png", "assets"),
        ("assets/Roboto-Regular.ttf", "assets"),
        ("dll/hidapi.dll", "."),
        ("ico/FRCStreamDeckIcon.ico","ico")
]
a = Analysis(
    ['mainWindow.py'],
    pathex=[],
    binaries=[('dll/wpinet.dll',"wpinet/lib"),
    ('dll/wpiutil.dll',"wpiutil/lib"),
    ('dll/ntcore.dll',"ntcore/lib")],
    datas=added_files,
    hiddenimports=['tkinter', 'robotpy-wpiutil'],
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
    [],
    exclude_binaries=True,
    name='FRCStreamDeckClient',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon="ico/FRCStreamDeckIcon.ico"
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='FRCStreamDeckClient',
)
