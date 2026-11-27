#!/bin/sh
# Dùng chung cho các git hook: chạy kiểm tra / cập nhật nhanh MCP-SUBBASEMBLY.
# Không bao giờ làm hỏng lệnh git: lỗi chỉ in cảnh báo.
cd "$(git rev-parse --show-toplevel)" || exit 0
if [ -x ".venv/Scripts/python.exe" ]; then PY=".venv/Scripts/python.exe"
elif [ -x ".venv/bin/python" ]; then PY=".venv/bin/python"
elif command -v python >/dev/null 2>&1; then PY="python"
elif command -v py >/dev/null 2>&1; then PY="py -3"
else echo "[SAC setup] Không tìm thấy Python - bỏ qua tự cập nhật." >&2; exit 0
fi
PYTHONIOENCODING=utf-8 $PY scripts/sac_auto_setup.py || echo "[SAC setup] Tự cập nhật lỗi - chạy setup.bat để xem chi tiết." >&2
exit 0
