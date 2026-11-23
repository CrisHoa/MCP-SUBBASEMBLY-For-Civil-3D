# Hướng Dẫn Cộng Tác Huấn Luyện Skill Qua Nhánh Git (`skill/*`)

Tài liệu này hướng dẫn các thành viên trong nhóm cùng tham gia huấn luyện, dạy thêm mẫu cấu kiện (`.pkt`) và kinh nghiệm thiết kế cho AI Skill **`sac-subassembly-design`** thông qua quy trình nhánh Git (**Branch-based Collaborative Skill Training**).

---

## 1. Kiến Trúc Chống Xung Đột (Zero Merge Conflict)

Khi nhiều người cùng huấn luyện một Skill trên nhiều nhánh khác nhau, nếu tất cả cùng sửa trực tiếp vào 1 file `SKILL.md` sẽ gây xung đột (`Git Merge Conflict`). Vì vậy hệ thống được thiết kế theo cơ chế **Mỗi bài học là 1 file độc lập**:

- **Bài học & Mẫu `.pkt` của từng thành viên** được tự động trích xuất và lưu tại:
  - `.claude/skills/sac-subassembly-design/reference/contributions/<slug>.md`
  - `examples/skill_contributions/<slug>/<slug>.pkt` & `<slug>.spec.json`
- **Mục lục tự động**: File `reference/contributions/INDEX.md` được tool tự động tổng hợp lại từ các file `.md`.
- **Tự động đồng bộ đa Agent**: Mọi thay đổi ở `.claude/skills/` (Claude Code) được tự động chép sang `.agents/skills/` (Google Antigravity & OpenCode).

---

## 2. Cài Đặt Lần Đầu Cho Máy Mới Clone Repo

Sau khi `git clone` repo về máy tính cá nhân, mở PowerShell tại thư mục dự án và chạy:

```powershell
# 1. Tạo môi trường ảo Python (nếu chưa có)
python -m venv .venv
.\.venv\Scripts\pip install -e ".[dev]"

# 2. Tự động cập nhật đường dẫn MCP (.agents/mcp_config.json, opencode.json) theo máy của bạn
.\sac-cli.bat skill setup --global-skill
```

---

## 3. Quy Trình 3 Bước Huấn Luyện Skill Bằng Nhánh Git

### Cách A: Ra lệnh trực tiếp cho AI trong khung Chat (Claude Code / Antigravity / OpenCode)

Bạn chỉ cần mở khung chat AI trong dự án và nói:
> *"Tạo cho tôi nhánh huấn luyện `skill/minh-tuong-chan`, học file `C:\duong_dan\TuongChan.pkt` với tiêu đề 'Tường chắn trọng lực QL13', sau đó kiểm định và đẩy nhánh lên Git."*

AI sẽ tự động gọi chuỗi MCP tools:
1. `skill_start_branch(branch_name="minh-tuong-chan", author="Minh")`
2. `skill_learn_pkt(pkt_path="...", title="Tường chắn trọng lực QL13", notes="...")`
3. `skill_submit_branch(message="Thêm mẫu tường chắn trọng lực QL13", push=True)`

---

### Cách B: Dùng dòng lệnh `sac-cli.bat`

#### Bước 1: Tạo nhánh huấn luyện riêng
```powershell
.\sac-cli.bat skill branch minh-tuong-chan --author "Minh"
```
*(Hệ thống sẽ tự động tạo và chuyển sang nhánh `skill/minh-tuong-chan`)*.

#### Bước 2: Dạy cho Skill từ file `.pkt` hoặc thêm quy tắc kinh nghiệm
- **Huấn luyện từ một file `.pkt` chuẩn** (tự động kiểm định 3 tầng, trích xuất bảng Point/Link/Shape/Parameter và Spec JSON):
  ```powershell
  .\sac-cli.bat skill learn "C:\Path\To\CauKien.pkt" --title "Tường chắn BTCT mở rộng đáy" --author "Minh" --notes "Điểm gốc đặt tại đỉnh trái P1, dùng Decision kiểm tra chiều cao H > 2m"
  ```
- **Hoặc dạy thêm một quy tắc / công thức VB / cách gỡ lỗi**:
  ```powershell
  .\sac-cli.bat skill note --title "Quy tắc đặt điểm gốc bó vỉa dải phân cách" --content "Khi gắn bó vỉa vào mép trong dải phân cách, đặt Origin tại P10 hoặc P4 để bám trực tiếp vào cao độ thiết kế..." --author "Minh"
  ```

#### Bước 3: Kiểm định và đẩy nhánh lên GitHub
```powershell
# Kiểm tra đồng bộ .claude <-> .agents và kiểm định 3 tầng toàn bộ file .pkt
.\sac-cli.bat skill check

# Commit và đẩy nhánh lên GitHub (kèm link mở Pull Request)
.\sac-cli.bat skill push -m "Huấn luyện mẫu tường chắn BTCT mở rộng đáy"
```

---

## 4. Dành Cho Quản Trị Viên Repo (Xem & Gộp Nhánh Huấn Luyện)

Khi các thành viên đã đẩy nhánh `skill/*` lên GitHub:

1. **Xem danh sách tất cả các nhánh huấn luyện và bài học**:
   ```powershell
   .\sac-cli.bat skill branches --fetch
   ```
2. **Gộp (Merge) nhánh của thành viên vào nhánh chính, tự động tổng hợp lại `INDEX.md` và hậu kiểm 3 tầng**:
   ```powershell
   git checkout Civil3D
   .\sac-cli.bat skill merge skill/minh-tuong-chan
   git push origin Civil3D
   ```
