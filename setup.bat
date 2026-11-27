@echo off
REM ============================================================
REM  Cai dat MCP-SUBBASEMBLY sau khi clone repo
REM  - Tao .venv, cai thu vien
REM  - Dang ky MCP "sac" + skill cho Claude Code, Antigravity, OpenCode
REM  - Bat git hook tu cap nhat sau moi lan git pull
REM  Logic nam o scripts\sac_auto_setup.py (dung chung voi hook).
REM  Tuy chon: --global-skill, --no-claude
REM ============================================================
setlocal
chcp 65001 >nul
cd /d "%~dp0"

set "PY="
if exist ".venv\Scripts\python.exe" set "PY=.venv\Scripts\python.exe"
if not defined PY (
    where py >nul 2>&1 && py -3 -c "import sys; sys.exit(0 if sys.version_info >= (3,10) else 1)" >nul 2>&1 && set "PY=py -3"
)
if not defined PY (
    where python >nul 2>&1 && python -c "import sys; sys.exit(0 if sys.version_info >= (3,10) else 1)" >nul 2>&1 && set "PY=python"
)
if not defined PY (
    echo [LOI] Khong tim thay Python 3.10 tro len. Cai tai https://www.python.org/downloads/ ^(tick "Add python.exe to PATH"^) roi chay lai.
    exit /b 1
)

echo Dang cai dat, vui long doi ^(lan dau mat khoang 1 phut^) ...
%PY% scripts\sac_auto_setup.py --force %* || exit /b 1
echo.
echo Hoan tat. Mo mot phien Claude Code MOI de su dung.
endlocal
