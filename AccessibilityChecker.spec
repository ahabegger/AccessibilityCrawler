# -*- mode: python ; coding: utf-8 -*-

# Add this near the top of the spec file
import os
from PyInstaller.utils.hooks import collect_data_files

# Find the axe_selenium_python package data
axe_data = collect_data_files('axe_selenium_python')


a = Analysis(
    ['AccessibilityChecker.py'],
    pathex=[],
    binaries=[],
    datas=axe_data,
    hiddenimports=['axe_selenium_python'],
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
    name='Main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
