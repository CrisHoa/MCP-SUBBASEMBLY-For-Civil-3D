"""
Tự động cài đặt / cập nhật MCP-SUBBASEMBLY trên máy hiện tại (chỉ dùng thư viện chuẩn Python).

Được gọi từ:
  - setup.bat                         (chạy tay, luôn cài đủ: --force)
  - .claude/settings.json SessionStart (khi mở Claude Code trong repo)
  - .githooks/post-merge, post-checkout (sau mỗi lần git pull / đổi nhánh)

Chế độ mặc định: kiểm tra nhanh, nếu máy đã cài đúng thì thoát im lặng (vài chục ms).
Chỉ làm phần còn thiếu:
  1. Tạo .venv nếu chưa có (cần Python >= 3.10).
  2. pip install -e ".[dev]" khi .venv mới tạo hoặc pyproject.toml thay đổi.
  3. `sac_mcp.cli skill setup` khi MCP "sac" / skill trong Claude Code, Antigravity chưa khớp với repo.
  4. Bật git hook của repo: git config core.hooksPath .githooks
"""

from __future__ import annotations

import filecmp
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IS_WIN = os.name == "nt"
VENV_PY = ROOT / ".venv" / ("Scripts/python.exe" if IS_WIN else "bin/python")
HASH_FILE = ROOT / ".venv" / ".sac_pyproject_hash"
SKILLS_SRC = ROOT / ".claude" / "skills"


def _pyproject_hash() -> str:
    return hashlib.sha256((ROOT / "pyproject.toml").read_bytes()).hexdigest()


def _same_tree(a: Path, b: Path) -> bool:
    if not b.is_dir():
        return False
    cmp = filecmp.dircmp(a, b)
    if cmp.left_only or cmp.right_only or cmp.funny_files:
        return False
    _, mismatch, errors = filecmp.cmpfiles(a, b, cmp.common_files, shallow=False)
    if mismatch or errors:
        return False
    return all(_same_tree(a / d, b / d) for d in cmp.common_dirs)


def _load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def _json_mcp_ok(cfg_path: Path, py: str, src: str) -> bool:
    sac = _load_json(cfg_path).get("mcpServers", {}).get("sac", {})
    return sac.get("command") == py and sac.get("env", {}).get("PYTHONPATH") == src


def _skills_ok(dst_root: Path) -> bool:
    return all(_same_tree(s, dst_root / s.name) for s in SKILLS_SRC.iterdir() if s.is_dir())


def _codex_block(py: str, src: str) -> str:
    # Phải giống hệt sac_mcp.core.skill_trainer.codex_mcp_block (script này không import sac_mcp
    # vì có thể chạy bằng Python hệ thống chưa có thư viện).
    return (
        "[mcp_servers.sac]\n"
        f"command = {json.dumps(py)}\n"
        f"args = {json.dumps(['-m', 'sac_mcp.server'])}\n"
        "startup_timeout_sec = 60\n"
        "\n"
        "[mcp_servers.sac.env]\n"
        f"PYTHONPATH = {json.dumps(src)}\n"
        'PYTHONIOENCODING = "utf-8"\n'
    )


def _registration_ok() -> bool:
    py = VENV_PY.as_posix()
    src = (ROOT / "src").as_posix()
    home = Path.home()

    # Claude Code
    if not _json_mcp_ok(home / ".claude.json", py, src) or not _skills_ok(home / ".claude" / "skills"):
        return False

    # Antigravity: cấu hình trong repo + cấu hình toàn máy (nếu máy có cài Antigravity)
    agents = _load_json(ROOT / ".agents" / "mcp_config.json").get("mcpServers", {}).get("sac", {})
    if agents.get("command") != py:
        return False
    if (ROOT / ".agents" / "skills").is_dir() and not _same_tree(SKILLS_SRC, ROOT / ".agents" / "skills"):
        return False
    ag = home / ".gemini" / "antigravity"
    if ag.is_dir() and (not _json_mcp_ok(ag / "mcp_config.json", py, src) or not _skills_ok(ag / "skills")):
        return False

    # Codex (nếu máy có cài Codex)
    cx = home / ".codex"
    if cx.is_dir():
        try:
            toml_text = (cx / "config.toml").read_text(encoding="utf-8")
        except OSError:
            return False
        if _codex_block(py, src) not in toml_text or not _skills_ok(home / ".agents" / "skills"):
            return False

    # OpenCode toàn máy (nếu máy có cài OpenCode; bỏ qua nếu dùng opencode.jsonc - setup không sửa file có chú thích)
    xdg = os.environ.get("XDG_CONFIG_HOME")
    oc = (Path(xdg) if xdg else home / ".config") / "opencode"
    if oc.is_dir() and ((oc / "opencode.json").exists() or not (oc / "opencode.jsonc").exists()):
        sac = _load_json(oc / "opencode.json").get("mcp", {}).get("sac", {})
        if sac.get("command") != [py, "-m", "sac_mcp.server"] or sac.get("environment", {}).get("PYTHONPATH") != src:
            return False
        if not _skills_ok(oc / "skills"):
            return False
    return True


def _git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=str(ROOT), capture_output=True, text=True)


def _hooks_ok() -> bool:
    if not (ROOT / ".git").exists():
        return True
    try:
        return _git("config", "--get", "core.hooksPath").stdout.strip() == ".githooks"
    except OSError:
        return True  # không có git trên PATH -> bỏ qua


def _run(cmd: list, step: str) -> None:
    res = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True, encoding="utf-8", errors="replace")
    if res.returncode != 0:
        sys.stderr.write(f"[SAC setup] LỖI ở bước '{step}':\n{res.stdout[-3000:]}\n{res.stderr[-3000:]}\n")
        sys.exit(1)


def _has_pip() -> bool:
    return subprocess.run([str(VENV_PY), "-m", "pip", "--version"], capture_output=True).returncode == 0


def _install_deps() -> None:
    """Cài thư viện vào .venv. Venv tạo bằng `uv` không có pip -> thử ensurepip, rồi tới uv."""
    if not _has_pip():
        subprocess.run([str(VENV_PY), "-m", "ensurepip", "--upgrade"], capture_output=True)
    if _has_pip():
        pip = [str(VENV_PY), "-m", "pip", "install", "--disable-pip-version-check", "--no-cache-dir", "-q"]
        _run(pip + ["--upgrade", "pip"], "nâng cấp pip")
        _run(pip + ["-e", ".[dev]"], "pip install")
        return
    uv = shutil.which("uv")
    if uv:
        _run([uv, "pip", "install", "--python", str(VENV_PY), "-q", "-e", ".[dev]"], "uv pip install")
        return
    sys.stderr.write("[SAC setup] .venv không có pip và máy không có uv. Xóa thư mục .venv rồi chạy lại setup.bat.\n")
    sys.exit(1)


def main(argv: list) -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    force = "--force" in argv
    passthrough = [a for a in argv if a != "--force"]
    done = []

    # 1) .venv
    venv_created = False
    if not VENV_PY.exists():
        if sys.version_info < (3, 10):
            sys.stderr.write(
                f"[SAC setup] Cần Python >= 3.10 để tạo .venv (đang dùng {sys.version.split()[0]} tại {sys.executable}).\n"
                "Cài Python mới tại https://www.python.org/downloads/ rồi chạy setup.bat.\n"
            )
            return 1
        _run([sys.executable, "-m", "venv", str(ROOT / ".venv")], "tạo .venv")
        venv_created = True
        done.append("tạo .venv")

    # 2) thư viện
    current_hash = _pyproject_hash()
    stored_hash = HASH_FILE.read_text(encoding="utf-8").strip() if HASH_FILE.exists() else ""
    if force or venv_created or stored_hash != current_hash:
        _install_deps()
        HASH_FILE.write_text(current_hash, encoding="utf-8")
        done.append("cài thư viện")

    # 3) đăng ký MCP + skill
    if force or not _registration_ok():
        res = subprocess.run(
            [str(VENV_PY), "-m", "sac_mcp.cli", "skill", "setup", *passthrough],
            cwd=str(ROOT), capture_output=True, text=True, encoding="utf-8", errors="replace",
            env=dict(os.environ, PYTHONIOENCODING="utf-8"),
        )
        if res.returncode != 0:
            sys.stderr.write(f"[SAC setup] LỖI ở bước 'skill setup':\n{res.stdout}\n{res.stderr}\n")
            return 1
        if force:
            print(res.stdout.rstrip())
        if res.stderr.strip():
            sys.stderr.write(res.stderr)
        done.append("đăng ký MCP 'sac' + skill (Claude Code, Antigravity, Codex, OpenCode)")

    # 4) git hook
    if not _hooks_ok():
        _git("config", "core.hooksPath", ".githooks")
        done.append("bật git hook tự cập nhật sau mỗi lần pull (core.hooksPath=.githooks)")

    if done:
        print("[SAC setup] Đã: " + "; ".join(done) + ".")
        if any("MCP" in d for d in done):
            print("[SAC setup] Mở phiên MỚI của Claude Code / Antigravity / Codex / OpenCode để nạp MCP 'sac' và skill mới.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
