@echo off
REM ============================================================
REM  Cai dat MCP-SUBBASEMBLY sau khi clone / pull repo
REM  1. Tao .venv va cai thu vien
REM  2. Dang ky MCP "sac" + skill cho Claude Code, Antigravity, OpenCode
REM  Chay lai bat cu luc nao (vd. sau khi git pull) - an toan.
REM ============================================================
setlocal
chcp 65001 >nul
set "ROOT_DIR=%~dp0"
cd /d "%ROOT_DIR%"

REM --- Tim Python >= 3.10 ---
set "PY="
where py >nul 2>&1 && py -3 -c "import sys; sys.exit(0 if sys.version_info >= (3,10) else 1)" >nul 2>&1 && set "PY=py -3"
if not defined PY (
    where python >nul 2>&1 && python -c "import sys; sys.exit(0 if sys.version_info >= (3,10) else 1)" >nul 2>&1 && set "PY=python"
)
if not defined PY (
    echo [LOI] Khong tim thay Python 3.10 tro len. Cai tai https://www.python.org/downloads/ ^(tick "Add python.exe to PATH"^) roi chay lai.
    exit /b 1
)

REM --- Tao moi truong ao ---
if not exist ".venv\Scripts\python.exe" (
    echo [1/3] Tao moi truong ao .venv ...
    %PY% -m venv .venv || (echo [LOI] Khong tao duoc .venv & exit /b 1)
) else (
    echo [1/3] Da co .venv
)

REM --- Cai thu vien ---
echo [2/3] Cai thu vien ^(mcp, lxml, pydantic, pytest^) ...
".venv\Scripts\python.exe" -m pip install --disable-pip-version-check -q --upgrade pip
".venv\Scripts\python.exe" -m pip install --disable-pip-version-check -q -e ".[dev]" || (echo [LOI] pip install that bai & exit /b 1)

REM --- Dang ky MCP + skill ---
echo [3/3] Dang ky MCP "sac" va skill ...
".venv\Scripts\python.exe" -m sac_mcp.cli skill setup %* || (echo [LOI] skill setup that bai & exit /b 1)

echo.
echo Hoan tat. Mo mot phien Claude Code MOI de su dung.
endlocal
