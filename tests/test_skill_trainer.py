"""
Kiểm thử toàn diện hệ thống Cộng tác Huấn luyện Skill qua nhánh Git (Collaborative Skill Training via Git Branches).
Bao gồm:
  - Chuẩn hóa slug tiếng Việt và tên nhánh `skill/<slug>`.
  - Cấu hình tự động workspace MCP (`setup_workspace`).
  - Tạo nhánh huấn luyện (`start_training_branch`), học từ file `.pkt` (`learn_from_pkt`), thêm ghi chú (`add_skill_note`).
  - Chặn file `.pkt` lỗi không cho học vào Skill.
  - Nhiều thành viên cùng huấn luyện trên các nhánh `skill/*` khác nhau và gộp nhánh (`merge_training_branch`) không xung đột.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
import pytest

from sac_mcp.core import skill_trainer as st

ROOT_DIR = Path(__file__).resolve().parent.parent


def _init_temp_git_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir(parents=True, exist_ok=True)
    shutil.copytree(ROOT_DIR / ".claude", repo / ".claude")

    subprocess.run(["git", "init", "-b", "Civil3D"], cwd=str(repo), check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=str(repo), check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=str(repo), check=True, capture_output=True)
    st.rebuild_contributions_index(repo)
    st.sync_skills(repo)
    subprocess.run(["git", "add", "."], cwd=str(repo), check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "init repo"], cwd=str(repo), check=True, capture_output=True)
    return repo


def test_slugify_and_normalize_branch():
    assert st.slugify("Minh - Tường Chắn Đôi QL13") == "minh-tuong-chan-doi-ql13"
    assert st.normalize_branch_name("Minh - Bó Vỉa") == "skill/minh-bo-via"
    assert st.normalize_branch_name("skill/hung-taluy") == "skill/hung-taluy"


def test_collaborative_branch_training_and_zero_conflict_merge(tmp_path: Path, monkeypatch):
    repo = _init_temp_git_repo(tmp_path)
    # HOME giả: setup_workspace ghi cấu hình toàn máy (Claude/Antigravity/Codex) - không được đụng máy thật
    fake_home = tmp_path / "home"
    (fake_home / ".gemini" / "antigravity").mkdir(parents=True)
    (fake_home / ".codex").mkdir()
    monkeypatch.setattr(Path, "home", lambda: fake_home)
    sample_pkt = (
        ROOT_DIR
        / "examples"
        / "Sub Assembly"
        / "Bo_7_Subassembly_Chuan"
        / "10_GPC_DUONGQL13_Goc_P10"
        / "GPC_DUONGQL13_Goc_P10.pkt"
    )
    assert sample_pkt.exists()

    # 1. Setup workspace trên máy mới
    setup_info = st.setup_workspace(repo, sync_global=False)
    assert (repo / ".agents" / "mcp_config.json").exists()
    assert (repo / "opencode.json").exists()
    assert setup_info["skill_sync"]["files_synced"] >= 5
    assert "sac" in json.loads((fake_home / ".claude.json").read_text(encoding="utf-8"))["mcpServers"]
    assert "sac" in json.loads(
        (fake_home / ".gemini" / "antigravity" / "mcp_config.json").read_text(encoding="utf-8")
    )["mcpServers"]
    assert "[mcp_servers.sac]" in (fake_home / ".codex" / "config.toml").read_text(encoding="utf-8")
    assert (fake_home / ".agents" / "skills" / "sac-subassembly-design" / "SKILL.md").exists()

    # 2. Thành viên 1 (Minh) tạo nhánh skill/minh-lan-xe và huấn luyện từ file .pkt
    b1 = st.start_training_branch("minh-lan-xe", author="Minh", root_dir=repo)
    assert b1["branch"] == "skill/minh-lan-xe"
    assert st.get_current_branch(repo) == "skill/minh-lan-xe"

    learn1 = st.learn_from_pkt(
        pkt_path=sample_pkt,
        title="Làn xe tiêu chuẩn Minh huấn luyện",
        author="Minh",
        notes="Đặt điểm gốc tại P1 mép trong làn xe.",
        category="pavement",
        root_dir=repo,
    )
    assert learn1["slug"] == "lan-xe-tieu-chuan-minh-huan-luyen"
    assert Path(learn1["lesson_markdown"]).exists()
    assert Path(learn1["saved_pkt"]).exists()
    assert Path(learn1["saved_spec"]).exists()

    sub1 = st.submit_training_branch(message="Minh đóng góp mẫu làn xe", push=False, root_dir=repo)
    assert sub1["committed"] is True
    assert sub1["validation"]["is_valid"] is True

    # 3. Quay về nhánh chính Civil3D, Thành viên 2 (Hùng) tạo nhánh skill/hung-quy-tac
    subprocess.run(["git", "checkout", "Civil3D"], cwd=str(repo), check=True, capture_output=True)
    b2 = st.start_training_branch("hung-quy-tac", author="Hùng", root_dir=repo)
    assert b2["branch"] == "skill/hung-quy-tac"

    note2 = st.add_skill_note(
        title="Quy tắc đặt điểm gốc P10 cho dải phân cách",
        content="Khi bám vào mép phải dải phân cách, chuyển Origin về P10 (0,0) để hướng phát triển sang trái.",
        author="Hùng",
        category="rule",
        root_dir=repo,
    )
    assert Path(note2["lesson_markdown"]).exists()
    sub2 = st.submit_training_branch(message="Hùng đóng góp quy tắc điểm gốc P10", push=False, root_dir=repo)
    assert sub2["committed"] is True

    # 4. Quản trị viên quay về nhánh Civil3D và gộp LẦN LƯỢT cả 2 nhánh của Minh & Hùng (Zero Merge Conflict)
    subprocess.run(["git", "checkout", "Civil3D"], cwd=str(repo), check=True, capture_output=True)
    m1 = st.merge_training_branch("skill/minh-lan-xe", root_dir=repo)
    assert m1["validation"]["is_valid"] is True

    m2 = st.merge_training_branch("skill/hung-quy-tac", root_dir=repo)
    assert m2["validation"]["is_valid"] is True

    branches_info = st.list_training_branches(repo)
    branch_names = {b["branch"] for b in branches_info["training_branches"]}
    assert {"skill/minh-lan-xe", "skill/hung-quy-tac"} <= branch_names
    slugs = {ls["slug"] for ls in branches_info["contributed_lessons"]}
    assert {"lan-xe-tieu-chuan-minh-huan-luyen", "quy-tac-dat-diem-goc-p10-cho-dai-phan-cach"} <= slugs


def test_learn_rejects_invalid_pkt(tmp_path: Path):
    repo = _init_temp_git_repo(tmp_path)
    bad_pkt = tmp_path / "corrupted.pkt"
    bad_pkt.write_bytes(b"not a valid zip package")

    with pytest.raises(ValueError, match="Từ chối huấn luyện"):
        st.learn_from_pkt(pkt_path=bad_pkt, title="Mẫu lỗi", root_dir=repo, run_native_test=False)
