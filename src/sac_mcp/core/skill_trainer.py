"""
Hệ thống huấn luyện Skill cộng tác qua nhánh Git (Collaborative Skill Training via Git Branches).

Cho phép nhiều thành viên cùng huấn luyện và mở rộng skill `sac-subassembly-design` mà không xung đột (Zero Merge Conflict):
  1. `setup_workspace`       : Tự động cấu hình đường dẫn MCP (.agents/mcp_config.json, opencode.json) theo máy người dùng.
  2. `start_training_branch` : Tạo và chuyển sang nhánh huấn luyện riêng (`skill/<ten-nhanh>`).
  3. `learn_from_pkt`        : Kiểm định 3 tầng file .pkt mẫu, trích xuất Spec JSON + bảng điểm/tham số/luồng thành bài học
                               markdown độc lập trong `.claude/skills/sac-subassembly-design/reference/contributions/<slug>.md`,
                               cập nhật `INDEX.md` và tự động đồng bộ sang `.agents/skills/`.
  4. `add_skill_note`        : Đóng góp quy tắc, công thức VB, kinh nghiệm xử lý lỗi vào kho bài học của skill.
  5. `check_skill_training`  : Kiểm tra đồng bộ `.claude` <-> `.agents`, frontmatter và kiểm định toàn bộ `.pkt` đóng góp.
  6. `submit_training_branch`: Kiểm định, commit và `git push -u origin skill/<ten-nhanh>` kèm link tạo Pull Request.
  7. `list_training_branches`: Liệt kê các nhánh huấn luyện (`skill/*`) và danh sách bài học đã đóng góp.
  8. `merge_training_branch` : Gộp nhánh huấn luyện của thành viên, tái tạo `INDEX.md`, đồng bộ skill và hậu kiểm 3 tầng.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from sac_mcp.core.spec_builder import export_spec
from sac_mcp.core.validator import PktValidator

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
SKILL_NAME = "sac-subassembly-design"


def slugify(text: str) -> str:
    """Chuyển chuỗi tiếng Việt / ký tự bất kỳ thành slug kebab-case chuẩn ASCII."""
    raw = str(text or "").strip().replace("Đ", "D").replace("đ", "d")
    norm = unicodedata.normalize("NFKD", raw).encode("ascii", "ignore").decode("ascii").lower()
    slug = re.sub(r"[^a-z0-9]+", "-", norm).strip("-")
    return slug or "lesson"


def normalize_branch_name(branch_name: str, prefix: str = "skill") -> str:
    """Chuẩn hóa tên nhánh về dạng `skill/<slug>`."""
    raw = str(branch_name or "").strip()
    if not raw:
        raise ValueError("Tên nhánh không được để trống.")
    for p in ("skill/", "train/", "feature/"):
        if raw.lower().startswith(p):
            raw = raw[len(p):]
            break
    parts = [slugify(part) for part in raw.split("/") if part.strip()]
    clean = "/".join(p for p in parts if p)
    if not clean:
        raise ValueError(f"Tên nhánh không hợp lệ: '{branch_name}'")
    return f"{prefix}/{clean}"


def _run_git(args: List[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args],
        cwd=str(cwd),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def get_current_branch(root_dir: Path = ROOT_DIR) -> str:
    res = _run_git(["rev-parse", "--abbrev-ref", "HEAD"], cwd=root_dir)
    if res.returncode == 0 and res.stdout.strip():
        return res.stdout.strip()
    return "unknown"


def get_remote_repo_url(root_dir: Path = ROOT_DIR) -> str:
    res = _run_git(["remote", "get-url", "origin"], cwd=root_dir)
    if res.returncode == 0 and res.stdout.strip():
        url = res.stdout.strip()
        if url.endswith(".git"):
            url = url[:-4]
        if url.startswith("git@github.com:"):
            url = "https://github.com/" + url[len("git@github.com:"):]
        return url
    return ""


def sync_skills(root_dir: Path = ROOT_DIR, sync_global: bool = False) -> Dict[str, Any]:
    """Đồng bộ `.claude/skills` (bản gốc) sang `.agents/skills` (và global skill nếu có)."""
    src = root_dir / ".claude" / "skills"
    dst = root_dir / ".agents" / "skills"
    if not src.exists():
        raise FileNotFoundError(f"Không tìm thấy thư mục skill gốc: {src}")

    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)

    copied = sum(1 for p in dst.rglob("*") if p.is_file())
    global_synced_dirs: List[str] = []
    global_skills_root = Path.home() / ".gemini" / "config" / "skills"
    for src_skill in sorted(src.iterdir()):
        if not src_skill.is_dir():
            continue
        target_global = global_skills_root / src_skill.name
        if sync_global or target_global.exists():
            if target_global.exists():
                shutil.rmtree(target_global)
            target_global.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(src_skill, target_global)
            global_synced_dirs.append(str(target_global))

    return {
        "source": str(src),
        "mirror": str(dst),
        "files_synced": copied,
        "global_skill_synced": ", ".join(global_synced_dirs) if global_synced_dirs else None,
    }


def setup_workspace(root_dir: Path = ROOT_DIR, sync_global: bool = False) -> Dict[str, Any]:
    """
    Cấu hình đường dẫn tuyệt đối của máy hiện tại cho `.agents/mcp_config.json` và `opencode.json`,
    giúp người mới clone repo về máy bất kỳ đều chạy được ngay MCP server và Skill.
    """
    root_dir = Path(root_dir).resolve()
    venv_py_win = root_dir / ".venv" / "Scripts" / "python.exe"
    venv_py_unix = root_dir / ".venv" / "bin" / "python"
    if venv_py_win.exists():
        py_exec = venv_py_win.as_posix()
    elif venv_py_unix.exists():
        py_exec = venv_py_unix.as_posix()
    else:
        py_exec = Path(sys.executable).resolve().as_posix()

    src_dir = (root_dir / "src").as_posix()

    agents_cfg_path = root_dir / ".agents" / "mcp_config.json"
    agents_cfg_path.parent.mkdir(parents=True, exist_ok=True)
    agents_cfg = {
        "mcpServers": {
            "sac": {
                "command": py_exec,
                "args": ["-m", "sac_mcp.server"],
                "env": {"PYTHONPATH": src_dir},
            }
        }
    }
    agents_cfg_path.write_text(json.dumps(agents_cfg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    opencode_cfg_path = root_dir / "opencode.json"
    opencode_cfg = {
        "$schema": "https://opencode.ai/config.json",
        "mcp": {
            "sac": {
                "type": "local",
                "command": [py_exec, "-m", "sac_mcp.server"],
                "environment": {"PYTHONPATH": src_dir},
                "enabled": True,
            }
        },
    }
    opencode_cfg_path.write_text(json.dumps(opencode_cfg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    sync_info = sync_skills(root_dir=root_dir, sync_global=sync_global)
    return {
        "root_dir": root_dir.as_posix(),
        "python_command": py_exec,
        "agents_mcp_config": str(agents_cfg_path),
        "opencode_config": str(opencode_cfg_path),
        "skill_sync": sync_info,
    }


def _contributions_dir(root_dir: Path) -> Path:
    d = root_dir / ".claude" / "skills" / SKILL_NAME / "reference" / "contributions"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _parse_frontmatter(md_text: str) -> Dict[str, str]:
    m = re.match(r"^---\n(.*?)\n---\n", md_text, re.DOTALL)
    if not m:
        return {}
    out: Dict[str, str] = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip().strip('"').strip("'")
    return out


def rebuild_contributions_index(root_dir: Path = ROOT_DIR) -> Path:
    """Tái tạo file `reference/contributions/INDEX.md` từ các bài học `.md` độc lập."""
    c_dir = _contributions_dir(root_dir)
    items: List[Dict[str, str]] = []
    for md_file in sorted(c_dir.glob("*.md")):
        if md_file.name.upper() == "INDEX.MD":
            continue
        meta = _parse_frontmatter(md_file.read_text(encoding="utf-8"))
        items.append(
            {
                "slug": meta.get("slug", md_file.stem),
                "title": meta.get("title", md_file.stem),
                "author": meta.get("author", "Community"),
                "category": meta.get("category", "pattern"),
                "subassembly": meta.get("subassembly_name", "-"),
                "file": md_file.name,
            }
        )

    lines = [
        "# Danh Mục Bài Học & Mẫu Cấu Kiện Cộng Đồng Đóng Góp (Skill Contributions)",
        "",
        "Thư mục này chứa các mẫu mặt cắt (`.pkt` / `spec.json`) và kinh nghiệm thiết kế do các thành viên huấn luyện",
        "trên từng nhánh Git (`skill/<ten-nhanh>`). Mỗi bài học nằm trên 1 file độc lập để tránh xung đột khi gộp nhánh.",
        "",
        "| Slug | Tiêu đề bài học | Cấu kiện | Loại | Người đóng góp | File chi tiết |",
        "| :--- | :--- | :--- | :---: | :---: | :--- |",
    ]
    if items:
        for it in items:
            lines.append(
                f"| `{it['slug']}` | {it['title']} | `{it['subassembly']}` | `{it['category']}` | "
                f"{it['author']} | [{it['file']}]({it['file']}) |"
            )
    else:
        lines.append("| *(Chưa có)* | Dùng `sac-cli skill learn <file.pkt> --title ...` để thêm bài học đầu tiên | - | - | - | - |")

    lines.append("")
    index_path = c_dir / "INDEX.md"
    index_path.write_text("\n".join(lines), encoding="utf-8")
    return index_path


def start_training_branch(
    branch_name: str,
    author: str = "",
    base_branch: str = "",
    root_dir: Path = ROOT_DIR,
) -> Dict[str, Any]:
    """Tạo và chuyển sang nhánh huấn luyện skill mới (`skill/<slug>`)."""
    root_dir = Path(root_dir).resolve()
    target_branch = normalize_branch_name(branch_name)

    # Kiểm tra nhánh đã tồn tại chưa
    check_res = _run_git(["rev-parse", "--verify", target_branch], cwd=root_dir)
    if check_res.returncode == 0:
        co_res = _run_git(["checkout", target_branch], cwd=root_dir)
        if co_res.returncode != 0:
            raise RuntimeError(f"Không thể chuyển sang nhánh '{target_branch}': {co_res.stderr.strip()}")
        action = "switched_existing"
    else:
        cmd = ["checkout", "-b", target_branch]
        if base_branch and base_branch.strip():
            cmd.append(base_branch.strip())
        co_res = _run_git(cmd, cwd=root_dir)
        if co_res.returncode != 0:
            raise RuntimeError(f"Không thể tạo nhánh '{target_branch}': {co_res.stderr.strip()}")
        action = "created_new"

    rebuild_contributions_index(root_dir)
    sync_info = sync_skills(root_dir)

    return {
        "branch": target_branch,
        "action": action,
        "author": author or "Contributor",
        "current_branch": get_current_branch(root_dir),
        "skill_sync": sync_info,
        "next_steps": [
            f"1. Huấn luyện từ file .pkt: sac-cli skill learn <duong_dan.pkt> --title \"Tên bài học\" --author \"{author or 'TenBan'}\"",
            "2. Hoặc thêm ghi chú kinh nghiệm: sac-cli skill note --title \"Tiêu đề\" --content \"Nội dung\"",
            "3. Kiểm tra & đẩy nhánh lên Git: sac-cli skill push -m \"Mô tả kỹ năng mới\"",
        ],
    }


def _format_step_summary(step: Dict[str, Any]) -> Dict[str, str]:
    stype = step.get("type", "unknown")
    sid = step.get("id", "-")
    parent = step.get("parent", "") or "-"
    codes = ""
    if stype == "point":
        pt_type = step.get("point_type", "DeltaX_DeltaY")
        fp = step.get("from_point") or "(Origin)"
        p1 = step.get("param_1", "0")
        p2 = step.get("param_2", "0")
        ln = f", Link={step.get('link_name')}" if step.get("add_link") and step.get("link_name") else ""
        detail = f"`{pt_type}` từ `{fp}` (`p1={p1}`, `p2={p2}`{ln})"
        codes = ", ".join(step.get("point_codes", []) + step.get("link_codes", []))
    elif stype == "link":
        detail = f"Nối `{step.get('start_point')}` -> `{step.get('end_point')}`"
        codes = ", ".join(step.get("link_codes", []))
    elif stype == "shape":
        links = ", ".join(step.get("link_names", []))
        detail = f"Khép miền từ Links: `[{links}]`"
        codes = ", ".join(step.get("shape_codes", []))
    elif stype == "decision":
        detail = f"Điều kiện: `{step.get('condition')}` ({step.get('true_label', 'True')} / {step.get('false_label', 'False')})"
    elif stype == "define_variable":
        detail = f"Khai báo biến `{step.get('name')}` ({step.get('variable_type')}) = `{step.get('default_value')}`"
    elif stype == "set_variable":
        detail = f"Gán `{step.get('name')}` = `{step.get('value_expr')}`"
    else:
        detail = json.dumps({k: v for k, v in step.items() if k not in ("id", "type", "parent")}, ensure_ascii=False)
    return {"id": str(sid), "type": str(stype), "detail": detail, "codes": codes or "-", "parent": str(parent)}


def learn_from_pkt(
    pkt_path: str | Path,
    title: str,
    author: str = "",
    notes: str = "",
    category: str = "pattern",
    slug: str = "",
    run_native_test: bool = True,
    root_dir: Path = ROOT_DIR,
) -> Dict[str, Any]:
    """
    Huấn luyện skill từ một file `.pkt` chuẩn:
      1. Kiểm định 3 tầng file `.pkt` (chặn ngay nếu file lỗi).
      2. Trích xuất Spec JSON (`export_spec`) và lưu bản mẫu vào `examples/skill_contributions/<slug>/`.
      3. Sinh tài liệu bài học markdown chuẩn hóa vào `.claude/skills/sac-subassembly-design/reference/contributions/<slug>.md`.
      4. Cập nhật `INDEX.md` và đồng bộ sang `.agents/skills/`.
    """
    root_dir = Path(root_dir).resolve()
    src_pkt = Path(pkt_path).resolve()
    if not src_pkt.exists():
        raise FileNotFoundError(f"Không tìm thấy file .pkt: {src_pkt}")

    # 1. Kiểm định chất lượng trước khi học
    rep = PktValidator.validate_pkt(src_pkt, run_native_test=run_native_test)
    errors = [f"[{i.category}] {i.message}" for i in rep.issues if i.severity == "ERROR"]
    if not rep.is_valid:
        raise ValueError(
            f"Từ chối huấn luyện: File '{src_pkt.name}' chưa đạt kiểm định ({len(errors)} lỗi): "
            + "; ".join(errors[:5])
        )

    # 2. Trích xuất Spec
    spec = export_spec(str(src_pkt))
    sub_name = spec.get("subassembly_name") or src_pkt.stem
    lesson_slug = slugify(slug or title or sub_name)
    author_name = (author or "").strip() or "Contributor"
    branch_name = get_current_branch(root_dir)

    # Lưu bản sao .pkt và .spec.json vào examples/skill_contributions/<slug>/
    contrib_ex_dir = root_dir / "examples" / "skill_contributions" / lesson_slug
    contrib_ex_dir.mkdir(parents=True, exist_ok=True)
    saved_pkt = contrib_ex_dir / f"{lesson_slug}.pkt"
    saved_spec = contrib_ex_dir / f"{lesson_slug}.spec.json"
    if src_pkt != saved_pkt.resolve():
        shutil.copy2(src_pkt, saved_pkt)
    saved_spec.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    # 3. Sinh bài học Markdown độc lập
    params = spec.get("parameters", [])
    steps = spec.get("steps", [])
    n_points = sum(1 for s in steps if s.get("type") == "point")
    n_links = sum(1 for s in steps if s.get("type") == "link") + sum(
        1 for s in steps if s.get("type") == "point" and s.get("add_link")
    )
    n_shapes = sum(1 for s in steps if s.get("type") == "shape")
    n_decisions = sum(1 for s in steps if s.get("type") == "decision")

    md_lines = [
        "---",
        f"slug: {lesson_slug}",
        f'title: "{title.replace(chr(34), chr(39))}"',
        f'author: "{author_name.replace(chr(34), chr(39))}"',
        f"category: {category}",
        f"subassembly_name: {sub_name}",
        f"civil_version: {spec.get('civil_version', '2026')}",
        f"branch: {branch_name}",
        f"updated_at: {datetime.now(timezone.utc).strftime('%Y-%m-%d')}",
        "---",
        "",
        f"# {title}",
        "",
        f"- **Cấu kiện (`subassembly_name`)**: `{sub_name}` (Civil 3D `{spec.get('civil_version', '2026')}`)",
        f"- **Người huấn luyện**: `{author_name}` (Nhánh: `{branch_name}`)",
        f"- **Thống kê hình học**: `{len(params)}` Parameters, `{n_points}` Points, `{n_links}` Links, `{n_shapes}` Shapes, `{n_decisions}` Decisions",
        f"- **File mẫu & Spec JSON**: `examples/skill_contributions/{lesson_slug}/{lesson_slug}.pkt` | `{lesson_slug}.spec.json`",
        "",
    ]

    if notes and notes.strip():
        md_lines.extend(
            [
                "## 1. Ghi Chú Thiết Kế & Kinh Nghiệm Huấn Luyện",
                "",
                notes.strip(),
                "",
            ]
        )

    md_lines.extend(
        [
            "## 2. Danh Sách Tham Số (Parameters)",
            "",
            "| Tên (`name`) | Nhóm (`category`) | Kiểu (`data_type`) | Mặc định (`default_value`) | Tên hiển thị (`display_name`) |",
            "| :--- | :---: | :---: | :---: | :--- |",
        ]
    )
    if params:
        for p in params:
            md_lines.append(
                f"| `{p.get('name')}` | `{p.get('category', 'Input')}` | `{p.get('data_type')}` | "
                f"`{p.get('default_value')}` | {p.get('display_name', '')} |"
            )
    else:
        md_lines.append("| *(Không có tham số tuỳ chỉnh)* | - | - | - | - |")

    md_lines.extend(
        [
            "",
            "## 3. Trình Tự Dựng Luồng (Flowchart Steps)",
            "",
            "| # | ID Bước | Loại Activity | Công thức / Định vị chi tiết | Codes | Node Cha / Nhánh |",
            "| :---: | :---: | :---: | :--- | :--- | :---: |",
        ]
    )
    for idx, st in enumerate(steps, start=1):
        row = _format_step_summary(st)
        md_lines.append(
            f"| {idx} | `{row['id']}` | `{row['type']}` | {row['detail']} | `{row['codes']}` | `{row['parent']}` |"
        )

    md_lines.extend(
        [
            "",
            "## 4. Tái Dựng Nhanh Bằng `build_from_spec`",
            "",
            "Agent có thể dựng lại nguyên bản hoặc lấy spec này làm mẫu chỉnh sửa bằng cách đọc file:",
            f"`examples/skill_contributions/{lesson_slug}/{lesson_slug}.spec.json` và gọi tool `build_from_spec`.",
            "",
        ]
    )

    lesson_md_path = _contributions_dir(root_dir) / f"{lesson_slug}.md"
    lesson_md_path.write_text("\n".join(md_lines), encoding="utf-8")

    index_path = rebuild_contributions_index(root_dir)
    sync_info = sync_skills(root_dir)

    return {
        "slug": lesson_slug,
        "title": title,
        "author": author_name,
        "branch": branch_name,
        "subassembly_name": sub_name,
        "lesson_markdown": str(lesson_md_path),
        "index_markdown": str(index_path),
        "saved_pkt": str(saved_pkt),
        "saved_spec": str(saved_spec),
        "validation": {
            "is_valid": rep.is_valid,
            "tier1_opc_ok": rep.tier1_opc_ok,
            "tier2_xaml_ok": rep.tier2_xaml_ok,
            "tier3_native_ok": rep.tier3_native_ok,
        },
        "skill_sync": sync_info,
    }


def add_skill_note(
    title: str,
    content: str,
    author: str = "",
    category: str = "rule",
    slug: str = "",
    root_dir: Path = ROOT_DIR,
) -> Dict[str, Any]:
    """Thêm bài học lý thuyết / quy tắc / công thức VB / cách gỡ lỗi vào kho đóng góp của skill."""
    root_dir = Path(root_dir).resolve()
    if not title or not title.strip():
        raise ValueError("Tiêu đề bài học (`title`) không được để trống.")
    if not content or not content.strip():
        raise ValueError("Nội dung bài học (`content`) không được để trống.")

    lesson_slug = slugify(slug or title)
    author_name = (author or "").strip() or "Contributor"
    branch_name = get_current_branch(root_dir)

    md_lines = [
        "---",
        f"slug: {lesson_slug}",
        f'title: "{title.replace(chr(34), chr(39))}"',
        f'author: "{author_name.replace(chr(34), chr(39))}"',
        f"category: {category}",
        "subassembly_name: general",
        f"branch: {branch_name}",
        f"updated_at: {datetime.now(timezone.utc).strftime('%Y-%m-%d')}",
        "---",
        "",
        f"# {title}",
        "",
        f"- **Phân loại**: `{category}`",
        f"- **Người đóng góp**: `{author_name}` (Nhánh: `{branch_name}`)",
        "",
        "## Nội Dung Hướng Dẫn",
        "",
        content.strip(),
        "",
    ]

    lesson_md_path = _contributions_dir(root_dir) / f"{lesson_slug}.md"
    lesson_md_path.write_text("\n".join(md_lines), encoding="utf-8")
    index_path = rebuild_contributions_index(root_dir)
    sync_info = sync_skills(root_dir)

    return {
        "slug": lesson_slug,
        "title": title,
        "author": author_name,
        "category": category,
        "branch": branch_name,
        "lesson_markdown": str(lesson_md_path),
        "index_markdown": str(index_path),
        "skill_sync": sync_info,
    }


def check_skill_training(root_dir: Path = ROOT_DIR, run_native_test: bool = True) -> Dict[str, Any]:
    """Kiểm định toàn bộ trạng thái đồng bộ skill, frontmatter và các file `.pkt` đóng góp."""
    root_dir = Path(root_dir).resolve()
    issues: List[str] = []

    # 1. Kiểm tra đồng bộ giữa .claude/skills và .agents/skills
    src_base = root_dir / ".claude" / "skills"
    dst_base = root_dir / ".agents" / "skills"
    src_files = (
        {p.relative_to(src_base).as_posix(): p.read_bytes() for p in sorted(src_base.rglob("*")) if p.is_file()}
        if src_base.exists()
        else {}
    )
    dst_files = (
        {p.relative_to(dst_base).as_posix(): p.read_bytes() for p in sorted(dst_base.rglob("*")) if p.is_file()}
        if dst_base.exists()
        else {}
    )
    mirror_diffs: List[str] = []
    for k in src_files:
        if k not in dst_files:
            mirror_diffs.append(f"Thiếu trong .agents/skills: {k}")
        elif src_files[k] != dst_files[k]:
            mirror_diffs.append(f"Khác nội dung giữa .claude và .agents: {k}")
    for k in dst_files:
        if k not in src_files:
            mirror_diffs.append(f"Thừa trong .agents/skills: {k}")
    issues.extend(mirror_diffs)

    # 2. Kiểm tra frontmatter chuẩn Agent Skills
    frontmatter_ok = True
    for skill_md in src_base.glob("*/SKILL.md"):
        text = skill_md.read_text(encoding="utf-8")
        meta = _parse_frontmatter(text)
        name = meta.get("name", "")
        desc = meta.get("description", "")
        if not (re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name) and name == skill_md.parent.name):
            frontmatter_ok = False
            issues.append(f"{skill_md}: name='{name}' không hợp chuẩn kebab-case hoặc khác tên thư mục.")
        if not (0 < len(desc) <= 1024):
            frontmatter_ok = False
            issues.append(f"{skill_md}: description dài {len(desc)} ký tự (yêu cầu 1..1024).")

    # 3. Kiểm định các file .pkt đóng góp trong examples/skill_contributions/
    contrib_dir = root_dir / "examples" / "skill_contributions"
    pkts_checked = 0
    if contrib_dir.exists():
        for pkt_file in sorted(contrib_dir.rglob("*.pkt")):
            pkts_checked += 1
            rep = PktValidator.validate_pkt(pkt_file, run_native_test=run_native_test)
            if not rep.is_valid:
                errs = "; ".join(i.message for i in rep.issues if i.severity == "ERROR")
                issues.append(f"File đóng góp '{pkt_file.name}' lỗi kiểm định: {errs}")

    return {
        "is_valid": len(issues) == 0,
        "mirror_ok": len(mirror_diffs) == 0,
        "frontmatter_ok": frontmatter_ok,
        "contributions_pkt_checked": pkts_checked,
        "issues": issues,
    }


def submit_training_branch(
    message: str = "",
    push: bool = True,
    root_dir: Path = ROOT_DIR,
    run_native_test: bool = True,
) -> Dict[str, Any]:
    """Đồng bộ, kiểm định, commit các bài học mới và đẩy nhánh huấn luyện lên Git (`origin`)."""
    root_dir = Path(root_dir).resolve()
    rebuild_contributions_index(root_dir)
    sync_skills(root_dir)

    check = check_skill_training(root_dir, run_native_test=run_native_test)
    if not check["is_valid"]:
        raise ValueError("Chưa thể đẩy nhánh do lỗi kiểm định skill:\n- " + "\n- ".join(check["issues"]))

    branch = get_current_branch(root_dir)
    paths_to_stage = [".claude/skills", ".agents/skills"]
    if (root_dir / "examples" / "skill_contributions").exists():
        paths_to_stage.append("examples/skill_contributions")

    _run_git(["add", *paths_to_stage], cwd=root_dir)

    status_res = _run_git(["status", "--porcelain", *paths_to_stage], cwd=root_dir)
    committed = False
    commit_msg = (message or "").strip() or f"feat(skill): train sac-subassembly-design on {branch}"
    if not commit_msg.startswith(("feat", "fix", "docs", "chore")):
        commit_msg = f"feat(skill): {commit_msg}"

    if status_res.stdout.strip():
        c_res = _run_git(["commit", "-m", commit_msg], cwd=root_dir)
        if c_res.returncode != 0:
            raise RuntimeError(f"Lỗi khi git commit: {c_res.stderr.strip()}")
        committed = True

    pushed = False
    push_output = ""
    if push:
        p_res = _run_git(["push", "-u", "origin", branch], cwd=root_dir)
        if p_res.returncode != 0:
            raise RuntimeError(f"Lỗi khi git push nhánh '{branch}': {p_res.stderr.strip()}")
        pushed = True
        push_output = (p_res.stdout + "\n" + p_res.stderr).strip()

    repo_url = get_remote_repo_url(root_dir)
    pr_url = f"{repo_url}/compare/Civil3D...{branch}?expand=1" if repo_url else ""

    return {
        "branch": branch,
        "committed": committed,
        "commit_message": commit_msg if committed else "(Không có thay đổi mới cần commit)",
        "pushed": pushed,
        "push_output": push_output,
        "pull_request_url": pr_url,
        "validation": check,
    }


def list_training_branches(root_dir: Path = ROOT_DIR, fetch: bool = False) -> Dict[str, Any]:
    """Liệt kê tất cả các nhánh huấn luyện (`skill/*`, `train/*`) và danh sách bài học hiện có."""
    root_dir = Path(root_dir).resolve()
    if fetch:
        _run_git(["fetch", "origin", "--prune"], cwd=root_dir)

    res = _run_git(
        [
            "for-each-ref",
            "--sort=-committerdate",
            "--format=%(refname:short)|%(committerdate:short)|%(authorname)|%(subject)",
            "refs/heads/skill/",
            "refs/heads/train/",
            "refs/remotes/origin/skill/",
            "refs/remotes/origin/train/",
        ],
        cwd=root_dir,
    )
    branches: List[Dict[str, str]] = []
    if res.returncode == 0:
        for line in res.stdout.splitlines():
            parts = line.strip().split("|", 3)
            if len(parts) == 4:
                branches.append(
                    {
                        "branch": parts[0],
                        "date": parts[1],
                        "author": parts[2],
                        "subject": parts[3],
                    }
                )

    c_dir = _contributions_dir(root_dir)
    lessons: List[Dict[str, str]] = []
    for md_file in sorted(c_dir.glob("*.md")):
        if md_file.name.upper() == "INDEX.MD":
            continue
        meta = _parse_frontmatter(md_file.read_text(encoding="utf-8"))
        lessons.append(
            {
                "slug": meta.get("slug", md_file.stem),
                "title": meta.get("title", md_file.stem),
                "author": meta.get("author", "Community"),
                "category": meta.get("category", "pattern"),
                "branch": meta.get("branch", "-"),
            }
        )

    return {
        "current_branch": get_current_branch(root_dir),
        "training_branches": branches,
        "contributed_lessons": lessons,
    }


def merge_training_branch(
    branch_name: str,
    root_dir: Path = ROOT_DIR,
    run_native_test: bool = True,
) -> Dict[str, Any]:
    """Gộp một nhánh huấn luyện (`skill/...`) vào nhánh hiện tại, tái tạo INDEX và đồng bộ skill."""
    root_dir = Path(root_dir).resolve()
    target = branch_name.strip()
    if not target:
        raise ValueError("Tên nhánh cần gộp không được để trống.")

    # Nếu truyền tên ngắn thì chuẩn hóa sang skill/<slug>
    candidates = [target]
    if not target.startswith(("skill/", "train/", "origin/")):
        norm = normalize_branch_name(target)
        candidates = [norm, f"origin/{norm}", f"origin/{target}"]
    else:
        candidates.append(f"origin/{target}")

    resolved_ref = None
    for cand in candidates:
        chk = _run_git(["rev-parse", "--verify", cand], cwd=root_dir)
        if chk.returncode == 0:
            resolved_ref = cand
            break

    if not resolved_ref:
        raise ValueError(f"Không tìm thấy nhánh huấn luyện '{branch_name}' (đã thử: {', '.join(candidates)}).")

    m_res = _run_git(["merge", "--no-commit", "--no-ff", resolved_ref], cwd=root_dir)
    # Nếu chỉ xung đột ở INDEX.md (do nhiều nhánh cùng thêm bài học), tự động tái tạo INDEX.md và hoàn tất merge
    if m_res.returncode != 0:
        unmerged = _run_git(["diff", "--name-only", "--diff-filter=U"], cwd=root_dir).stdout.splitlines()
        only_index_conflict = bool(unmerged) and all(
            p.replace("\\", "/").endswith("reference/contributions/INDEX.md") for p in unmerged
        )
        if not only_index_conflict:
            _run_git(["merge", "--abort"], cwd=root_dir)
            raise RuntimeError(
                f"Lỗi xung đột khi gộp nhánh '{resolved_ref}': {m_res.stderr.strip() or m_res.stdout.strip()}"
            )

    rebuild_contributions_index(root_dir)
    sync_info = sync_skills(root_dir)
    _run_git(["add", ".claude/skills", ".agents/skills"], cwd=root_dir)
    if (root_dir / "examples" / "skill_contributions").exists():
        _run_git(["add", "examples/skill_contributions"], cwd=root_dir)

    # Hoàn tất commit merge nếu đang trong trạng thái MERGE_HEAD
    merge_head = root_dir / ".git" / "MERGE_HEAD"
    if merge_head.exists():
        _run_git(["commit", "-m", f"Merge skill training branch '{resolved_ref}'"], cwd=root_dir)

    check = check_skill_training(root_dir, run_native_test=run_native_test)

    return {
        "merged_branch": resolved_ref,
        "into_branch": get_current_branch(root_dir),
        "merge_output": m_res.stdout.strip(),
        "skill_sync": sync_info,
        "validation": check,
    }
