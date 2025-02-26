# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('views/*.py', 'views'),
        ('models/*.py', 'models'),
        ('models/password/*.py', 'models/password'),
        ('models/password_value/*.py', 'models/password_value'),
        ('models/user/*.py', 'models/user'),
        ('state/*.py', 'state'),
        ('utils/*.py', 'utils'),
        ('data.db', '.'),
        ('icon.ico', '.')
    ],
    hiddenimports=[
        'anyio._backends._asyncio',
        'anyio._backends._trio',
        'httpcore.backend.anyio',
        'httpx._transports.anyio',
        'sniffio._impl',
        'cryptography',
        'cryptography.fernet',
        'cryptography.hazmat',
        'cryptography.hazmat.backends',
        'cryptography.hazmat.primitives',
        'cryptography.hazmat.backends.openssl',
        'cryptography.hazmat.bindings._rust',
        'oauthlib.oauth2',
        'oauthlib.oauth1',
        'sqlite3',
        'logs',
        'models',
        'models.password',
        'models.password_value',
        'models.user',
        'state',
        'utils',
        'views'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Añadir archivos estáticos de Flet
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Añadir datos de Flet
flet_data = collect_data_files('flet', subdir='web')
a.datas += flet_data

# Añadir módulos adicionales para AnyIO y Cryptography
a.binaries += [
    ('crypto/cffi/_openssl.abi3.so', '/usr/local/lib/python3.9/site-packages/_cffi_backend.cpython-39-x86_64-linux-gnu.so', 'BINARY')
]

# Configuración de paquetes
a.datas += [('certifi/cacert.pem', '/usr/local/lib/python3.9/site-packages/certifi/cacert.pem', 'DATA')]

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='SePaGen',
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
    icon='icon.ico'
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='SePaGen',
)