"""
CLI Tooling chuyên dụng cho Autodesk Subassembly Composer (.pkt).
Cung cấp các lệnh tức thì:
  - sac-cli validate <file.pkt>   : Kiểm định 3 tầng (OPC, XAML, Native DLL)
  - sac-cli build --giaco         : Tự động dựng và kiểm định mái taluy Phú Yên
  - sac-cli build --sub7          : Tự động dựng và kiểm định bộ 7 subassemblies
  - sac-cli build --all [--out D] : Dựng toàn bộ, kiểm định và xuất ra thư mục D
  - sac-cli test                  : Chạy toàn bộ unit test pytest
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from sac_mcp.paths import OUTPUT_DIR_ENV, get_output_dir

ROOT_DIR = Path(__file__).resolve().parent.parent.parent


def cmd_validate(args: argparse.Namespace) -> int:
    from sac_mcp.core.validator import PktValidator
    target = Path(args.target).resolve()
    if not target.exists():
        print(f"❌ File không tồn tại: {target}")
        return 1

    report = PktValidator.validate_pkt(target, run_native_test=not args.no_native, document_check=args.doc)
    report.print_summary()
    return 0 if report.is_valid else 1


def cmd_build(args: argparse.Namespace) -> int:
    from sac_mcp.core.validator import PktValidator

    out_dir = get_output_dir(args.out)
    # Truyền thư mục xuất cho các script con qua biến môi trường
    child_env = {**os.environ, OUTPUT_DIR_ENV: str(out_dir)}
    built_files = []

    if args.giaco or args.all:
        print("\n🔨 [1/2] Dựng Subassembly: Gia Cố Mái Taluy Phú Yên...")
        script_giaco = ROOT_DIR / "scripts" / "build_giaco_taluy_phuyen.py"
        res = subprocess.run([sys.executable, str(script_giaco)], capture_output=True, text=True, encoding="utf-8", errors="replace", env=child_env)
        if res.returncode != 0:
            print(f"❌ Lỗi khi dựng Gia Cố Mái Taluy:\n{res.stderr}")
            return 1
        if res.stdout:
            print(res.stdout.strip())
        built_files.append(out_dir / "GiaCo_MaiTaluy_PhuYen.pkt")

    if args.sub7 or args.all:
        print("\n🔨 [2/2] Dựng Bộ 7 Subassembly chuẩn (đã xóa chữ visual)...")
        script_sub7 = ROOT_DIR / "scripts" / "rebuild_7_subassemblies.py"
        res = subprocess.run([sys.executable, str(script_sub7)], capture_output=True, text=True, encoding="utf-8", errors="replace", env=child_env)
        if res.returncode != 0:
            print(f"❌ Lỗi khi dựng Bộ 7 Subassembly:\n{res.stderr}")
            return 1
        if res.stdout:
            print(res.stdout.strip())
        sub7_dir = out_dir / "Bo_7_Subassembly"
        built_files.extend(list(sub7_dir.glob("*.pkt")))


    print("\n🔍 [KIỂM ĐỊNH TỰ ĐỘNG BẰNG NATIVE DLL AUTODESK]")
    all_ok = True
    for pkt in built_files:
        if pkt.exists():
            rep = PktValidator.validate_pkt(pkt, run_native_test=True)
            status = "✅ PASS" if rep.is_valid else "❌ FAIL"
            print(f"  [{status}] {pkt.name} ({pkt.stat().st_size} bytes)")
            if not rep.is_valid:
                all_ok = False
                for iss in rep.issues:
                    print(f"      -> {iss.message}")

    print("\n" + ("=" * 60))
    if all_ok:
        print("🎉 TẤT CẢ FILE ĐÃ ĐƯỢC DỰNG & KIỂM ĐỊNH THÀNH CÔNG 100%!")
        print(f"📁 Thư mục xuất: {out_dir}")
    else:
        print("❌ CÓ FILE BỊ LỖI KIỂM ĐỊNH!")
    print("=" * 60 + "\n")
    return 0 if all_ok else 1


def cmd_test(args: argparse.Namespace) -> int:
    print("\n🧪 Chạy toàn bộ kiểm thử pytest...")
    res = subprocess.run([sys.executable, "-m", "pytest", "-v"], cwd=str(ROOT_DIR))
    return res.returncode


def cmd_skill(args: argparse.Namespace) -> int:
    from sac_mcp.core import skill_trainer as st

    action = args.skill_action
    try:
        if action == "setup":
            info = st.setup_workspace(
                ROOT_DIR,
                sync_global=args.global_skill,
                claude_code=not args.no_claude,
                antigravity=not args.no_antigravity,
                codex=not args.no_codex,
                opencode=not args.no_opencode,
            )
            print("✅ Đã cấu hình đường dẫn MCP và đồng bộ Skill cho máy hiện tại:")
            print(f"  - Python       : {info['python_command']}")
            print(f"  - Antigravity (repo): {info['agents_mcp_config']}")
            print(f"  - OpenCode (repo): {info['opencode_config']}")
            print(f"  - Skill Synced : {info['skill_sync']['files_synced']} files (.claude/skills -> .agents/skills)")
            if info["skill_sync"]["global_skill_synced"]:
                print(f"  - Global Skill : {info['skill_sync']['global_skill_synced']}")
            for key, label in (("claude_code", "Claude Code"), ("antigravity", "Antigravity"), ("codex", "Codex"), ("opencode", "OpenCode")):
                agent = info.get(key)
                if not agent:
                    continue
                print(f"  - {label:<12} : MCP 'sac' -> {agent['config']}")
                print(f"  - {label + ' skill':<12} : {', '.join(agent['skills'])} -> {agent['skills_dir']}")
                if agent["removed_duplicates"]:
                    print(f"    (đã gỡ mục trùng server: {', '.join(agent['removed_duplicates'])})")
            print("  => Khởi động lại / mở phiên MỚI của Claude Code, Antigravity, Codex, OpenCode để nạp MCP 'sac' và skill.")
            return 0

        if action == "branch":
            info = st.start_training_branch(
                branch_name=args.name,
                author=args.author or "",
                base_branch=args.base or "",
                root_dir=ROOT_DIR,
            )
            verb = "Tạo mới & chuyển sang" if info["action"] == "created_new" else "Chuyển sang"
            print(f"🌿 {verb} nhánh huấn luyện: {info['branch']}")
            for step in info["next_steps"]:
                print(f"   {step}")
            return 0

        if action == "learn":
            info = st.learn_from_pkt(
                pkt_path=args.pkt,
                title=args.title,
                author=args.author or "",
                notes=args.notes or "",
                category=args.category,
                slug=args.slug or "",
                run_native_test=not args.no_native,
                root_dir=ROOT_DIR,
            )
            print(f"🎓 Đã huấn luyện thành công cấu kiện '{info['subassembly_name']}' vào Skill!")
            print(f"  - Slug bài học : {info['slug']}")
            print(f"  - Nhánh Git    : {info['branch']}")
            print(f"  - File bài học : {info['lesson_markdown']}")
            print(f"  - File mẫu PKT : {info['saved_pkt']}")
            print(f"  - Spec JSON    : {info['saved_spec']}")
            print(f"  - Đồng bộ      : {info['skill_sync']['files_synced']} files (.claude <-> .agents)")
            return 0

        if action == "note":
            info = st.add_skill_note(
                title=args.title,
                content=args.content,
                author=args.author or "",
                category=args.category,
                slug=args.slug or "",
                root_dir=ROOT_DIR,
            )
            print(f"📝 Đã thêm bài học/ghi chú '{info['title']}' ({info['slug']}) vào Skill!")
            print(f"  - File bài học : {info['lesson_markdown']}")
            print(f"  - Đồng bộ      : {info['skill_sync']['files_synced']} files (.claude <-> .agents)")
            return 0

        if action == "check":
            info = st.check_skill_training(ROOT_DIR, run_native_test=not args.no_native)
            if info["is_valid"]:
                print(
                    f"✅ KIỂM ĐỊNH SKILL ĐẠT 100%! "
                    f"(Mirror OK, Frontmatter OK, {info['contributions_pkt_checked']} file .pkt đóng góp đạt chuẩn)"
                )
                return 0
            print(f"❌ PHÁT HIỆN {len(info['issues'])} LỖI KIỂM ĐỊNH SKILL:")
            for iss in info["issues"]:
                print(f"  - {iss}")
            return 1

        if action == "push":
            info = st.submit_training_branch(
                message=args.message or "",
                push=not args.no_push,
                root_dir=ROOT_DIR,
                run_native_test=not args.no_native,
            )
            print(f"🚀 Đã đóng gói nhánh huấn luyện '{info['branch']}':")
            print(f"  - Commit : {info['commit_message']}")
            print(f"  - Pushed : {'Thành công lên origin' if info['pushed'] else 'Chỉ commit cục bộ (--no-push)'}")
            if info["pull_request_url"]:
                print(f"  - Tạo PR : {info['pull_request_url']}")
            return 0

        if action == "branches":
            info = st.list_training_branches(ROOT_DIR, fetch=args.fetch)
            print(f"🌿 Nhánh hiện tại: {info['current_branch']}")
            print(f"\n📌 Các nhánh huấn luyện ({len(info['training_branches'])}):")
            if info["training_branches"]:
                for b in info["training_branches"]:
                    print(f"  - {b['branch']:35s} | {b['date']} | {b['author']:18s} | {b['subject']}")
            else:
                print("  (Chưa có nhánh skill/* nào)")
            print(f"\n📚 Các bài học đã đóng góp ({len(info['contributed_lessons'])}):")
            if info["contributed_lessons"]:
                for ls in info["contributed_lessons"]:
                    print(f"  - [{ls['slug']}] {ls['title']} (bởi {ls['author']}, nhánh {ls['branch']})")
            else:
                print("  (Chưa có bài học đóng góp nào)")
            return 0

        if action == "merge":
            info = st.merge_training_branch(
                branch_name=args.name,
                root_dir=ROOT_DIR,
                run_native_test=not args.no_native,
            )
            print(f"🔀 Đã gộp nhánh '{info['merged_branch']}' vào '{info['into_branch']}' và đồng bộ Skill!")
            if not info["validation"]["is_valid"]:
                print("⚠️ Cảnh báo hậu kiểm:")
                for iss in info["validation"]["issues"]:
                    print(f"  - {iss}")
                return 1
            return 0

    except Exception as exc:
        print(f"❌ Lỗi: {exc}")
        return 1
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="sac-cli",
        description="Bộ công cụ tự động hóa, huấn luyện Skill cộng tác & kiểm định Autodesk Civil 3D Subassembly Composer (.pkt)",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Lệnh validate
    p_val = subparsers.add_parser("validate", help="Kiểm định file .pkt qua 3 tầng (OPC, XAML, Native DLL)")
    p_val.add_argument("target", help="Đường dẫn file .pkt cần kiểm định")
    p_val.add_argument("--no-native", action="store_true", help="Bỏ qua Tầng 3 (DLL gốc của SAC)")
    p_val.add_argument("--doc", action="store_true", help="Tầng 3 mở thêm bằng SubassemblyDocument như SAC GUI (~2 giây)")
    p_val.set_defaults(func=cmd_validate)

    # Lệnh build
    p_build = subparsers.add_parser("build", help="Dựng nhanh subassembly và tự động kiểm định")
    p_build.add_argument("--giaco", action="store_true", help="Dựng riêng GiaCo_MaiTaluy_PhuYen.pkt")
    p_build.add_argument("--sub7", action="store_true", help="Dựng riêng Bộ 7 Subassembly chuẩn")
    p_build.add_argument("--all", action="store_true", help="Dựng toàn bộ tất cả file và kiểm định")
    p_build.add_argument("--out", help=f"Thư mục xuất (mặc định: biến môi trường {OUTPUT_DIR_ENV} hoặc ~/Desktop/SUB PHU YEN)")
    p_build.set_defaults(func=cmd_build)

    # Lệnh test
    p_test = subparsers.add_parser("test", help="Chạy toàn bộ pytest suite")
    p_test.set_defaults(func=cmd_test)

    # Lệnh skill (cộng tác huấn luyện skill qua nhánh Git)
    p_skill = subparsers.add_parser("skill", help="Huấn luyện Skill cộng tác qua nhánh Git (branch, learn, note, check, push, merge)")
    skill_sub = p_skill.add_subparsers(dest="skill_action", required=True)

    p_setup = skill_sub.add_parser("setup", help="Cấu hình đường dẫn MCP và đồng bộ skill cho máy vừa clone repo")
    p_setup.add_argument("--global-skill", action="store_true", help="Đồng bộ luôn vào ~/.gemini/config/skills/")
    p_setup.add_argument("--no-claude", action="store_true", help="Không đăng ký MCP/skill vào Claude Code (~/.claude.json, ~/.claude/skills/)")
    p_setup.add_argument("--no-antigravity", action="store_true", help="Không đăng ký vào Antigravity (~/.gemini/antigravity/mcp_config.json, skills/)")
    p_setup.add_argument("--no-codex", action="store_true", help="Không đăng ký vào Codex (~/.codex/config.toml, ~/.agents/skills/)")
    p_setup.add_argument("--no-opencode", action="store_true", help="Không đăng ký vào OpenCode toàn máy (~/.config/opencode/opencode.json, skills/)")

    p_branch = skill_sub.add_parser("branch", help="Tạo hoặc chuyển sang nhánh huấn luyện skill/<ten-nhanh>")
    p_branch.add_argument("name", help="Tên nhánh (VD: minh-cong-hop hoặc skill/minh-cong-hop)")
    p_branch.add_argument("--author", help="Tên người huấn luyện")
    p_branch.add_argument("--base", help="Nhánh gốc để rẽ nhánh (tùy chọn)")

    p_learn = skill_sub.add_parser("learn", help="Huấn luyện 1 file .pkt chuẩn vào kho bài học của Skill")
    p_learn.add_argument("pkt", help="Đường dẫn tới file .pkt mẫu cần học")
    p_learn.add_argument("--title", required=True, help="Tiêu đề bài học / mẫu cấu kiện")
    p_learn.add_argument("--author", help="Tên người đóng góp")
    p_learn.add_argument("--notes", help="Ghi chú thiết kế / lưu ý đặc biệt cho AI")
    p_learn.add_argument("--category", default="pattern", help="Phân loại (pattern, drainage, wall, pavement...)")
    p_learn.add_argument("--slug", help="Mã định danh bài học (tự sinh từ title nếu bỏ trống)")
    p_learn.add_argument("--no-native", action="store_true", help="Bỏ qua kiểm định Tầng 3 khi máy chưa cài SAC")

    p_note = skill_sub.add_parser("note", help="Thêm bài học quy tắc / công thức VB / kinh nghiệm gỡ lỗi vào Skill")
    p_note.add_argument("--title", required=True, help="Tiêu đề quy tắc / kinh nghiệm")
    p_note.add_argument("--content", required=True, help="Nội dung hướng dẫn chi tiết cho AI")
    p_note.add_argument("--author", help="Tên người đóng góp")
    p_note.add_argument("--category", default="rule", help="Phân loại (rule, formula, troubleshooting...)")
    p_note.add_argument("--slug", help="Mã định danh bài học")

    p_check = skill_sub.add_parser("check", help="Kiểm tra đồng bộ .claude <-> .agents và kiểm định toàn bộ .pkt đóng góp")
    p_check.add_argument("--no-native", action="store_true", help="Bỏ qua Tầng 3 khi máy chưa cài SAC")

    p_push = skill_sub.add_parser("push", help="Kiểm định, commit và đẩy nhánh huấn luyện lên GitHub")
    p_push.add_argument("-m", "--message", help="Nội dung commit message")
    p_push.add_argument("--no-push", action="store_true", help="Chỉ commit cục bộ, không chạy git push")
    p_push.add_argument("--no-native", action="store_true", help="Bỏ qua Tầng 3 khi máy chưa cài SAC")

    p_branches = skill_sub.add_parser("branches", help="Liệt kê các nhánh huấn luyện skill/* và bài học đã đóng góp")
    p_branches.add_argument("--fetch", action="store_true", help="Fetch danh sách nhánh mới nhất từ origin trước khi liệt kê")

    p_merge = skill_sub.add_parser("merge", help="Gộp nhánh huấn luyện của thành viên và đồng bộ lại toàn bộ Skill")
    p_merge.add_argument("name", help="Tên nhánh cần gộp (VD: skill/minh-cong-hop)")
    p_merge.add_argument("--no-native", action="store_true", help="Bỏ qua Tầng 3 khi máy chưa cài SAC")

    p_skill.set_defaults(func=cmd_skill)

    args = parser.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
