# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['interfaz.py'],
    pathex=[],
    binaries=[],
    datas=[('resources', 'resources'), ('C:/Users/zoe00/AppData/Local/Packages/PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0/LocalCache/local-packages/Python311/site-packages/escpos/capabilities.json', 'escpos/capabilities')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Punto de Venta Ice&Crepes',
    debug=False,
    icon='C:/Users/zoe00/OneDrive/Escritorio/Punto-de-venta-Ice-Crepes/resources/10222.ico',
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='interfaz',
)
