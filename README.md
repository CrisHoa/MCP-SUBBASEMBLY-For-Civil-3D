AC MCP Server & Toolchain (sac-mcp-server)A dedicated MCP Server & CLI Toolchain for reading, designing, validating, and automatically generating Subassembly (.pkt) files for Autodesk Civil 3D Subassembly Composer.Create / Edit: Civil 3D 2025, 2026, 2027.Read / Validate: Also supports Civil 3D 2024.1. Quick StartPowerShell# 1. Clone the repository
git clone https://github.com/CrisHoa/MCP-SUBBASEMBLY-For-Civil-3D.git
cd "MCP-SUBBASEMBLY-For-Civil-3D"

# 2. Set up the Python environment & auto-configure MCP + Skill paths
python -m venv .venv
.\.venv\Scripts\pip install -e ".[dev]"
.\sac-cli.bat skill setup --global-skill
2. CLI Tool (sac-cli.bat)PowerShell# Run 3-tier validation on a .pkt file (add --doc to open via SubassemblyDocument, --no-native to skip Tier 3)
.\sac-cli.bat validate "D:\path\to\file.pkt"

# Quick build and auto-validate
.\sac-cli.bat build --giaco                            # Slope Protection Subassembly (Gia Cố Mái Taluy)
.\sac-cli.bat build --sub7                             # Standard 7-Subassembly Suite (parameters only)
.\sac-cli.bat build --all --out "D:\Export\SUB PHU YEN" # Build all to a specified output directory

# Run test suite
.\sac-cli.bat test
Output directory priority: --out → SAC_OUTPUT_DIR environment variable → default ~/Desktop/SUB PHU YEN.3. 3-Tier Validation & Safety MechanismsPlaintext[.pkt] ──> Tier 1: OPC & XML ──> Tier 2: Static XAML & Semantics ──> Tier 3: Native SAC DLLs
Tier 1 (OPC & XML): Verifies all 6 GUID-named files (.atc, .cfg, .xaml, .pvd, .emd, .cdmd), [Content_Types].xml, and XML syntax.Tier 2 (Static XAML): Runs even without SAC installed. Checks UTF-8 BOM, VB.NET expressions, activity tags, required attributes, and Point/Link/Flowchart references (semantic_checks.py).Tier 3 (Native SAC): Runs via SacHost.exe (auto-compiled on first run using csc.exe, kept alive as a background process at ~10 ms/file). Automatically selects the matching SAC version from .cfg (overridable via SAC_INSTALL_DIR) to compile VB expressions and catch undeclared variable or type errors.Safe File Editing: Every .pkt editing tool writes to a temporary file → runs Tier 1–2 validation → backs up the original as .pkt.bak → performs an atomic swap (os.replace). Tier 3 errors on save are reported as warnings without blocking (disable via SAC_MCP_NATIVE_ON_SAVE=0).4. 27 MCP ToolsCategoryCore ToolsRead & Referenceinspect_pkt, validate_pkt_native, get_sac_reference_and_formulas, list_examples_and_split_catalogCreation & Speccreate_pkt_from_template, generate_assembly_recipe, export_spec, build_from_specGeometryadd_point_and_link, add_link, add_shape, add_fillet_arc, add_curve, add_offset_geometry, add_loop_geometry, add_intersection_point, add_strip_surface, add_get_mark_point / add_set_mark_pointParameters & Logicadd_parameter, add_define_variable / add_set_variable, add_set_output_parameter, add_flow_decision, add_report_messageFlowchart Editingupdate_node (auto-updates references on rename), remove_node (auto-reconnects flow)Flowchart Wiring (parent_node_id): Leave empty to converge all open branches into the new node; pass __ReferenceIDn to insert directly after a FlowStep; pass __ReferenceIDn:True / :False to insert into a FlowDecision branch.Object Naming: Names must be unique by default (pass allow_duplicate_name=True when reusing a name across mutually exclusive branches).5. AI Coding Agent IntegrationThe sac-subassembly-design skill (following the open Agent Skills standard) includes design workflows and verified patterns (reference/patterns.md).ToolSkill Directorysac MCP ConfigurationClaude Code.claude/skills/ (source of truth)Claude Code MCP configGoogle Antigravity.agents/skills/ (mirror).agents/mcp_config.jsonOpenCode.claude/skills/ & .agents/skills/opencode.jsonAfter editing skills in .claude/skills/, run .venv\Scripts\python.exe scripts\sync_agent_skills.py to mirror changes to .agents/skills/.6. Collaborative Skill Training (skill/*)Allows multiple contributors to add new .pkt templates or design rules on isolated Git branches with zero merge conflicts (see CONTRIBUTING_SKILL.md for details):PowerShell# 1. Create a dedicated training branch (automatically prefixed with skill/)
.\sac-cli.bat skill branch minh-retaining-wall --author "Minh"

# 2a. Learn from a verified .pkt file (3-tier validate -> extract Spec -> generate lesson -> sync)
.\sac-cli.bat skill learn "C:\Path\To\Component.pkt" --title "RC Retaining Wall" --author "Minh" --notes "Origin at P1"

# 2b. Or add a rule / VB formula / troubleshooting note
.\sac-cli.bat skill note --title "Curb Origin Rule" --content "Place Origin at P4 or P10..." --author "Minh"

# 3. Verify sync & push to GitHub (prints a ready-to-use PR link)
.\sac-cli.bat skill check
.\sac-cli.bat skill push -m "Train RC retaining wall pattern"

# 4. (Maintainers) List and merge contributor branches
.\sac-cli.bat skill branches --fetch
.\sac-cli.bat skill merge skill/minh-retaining-wall
SAC MCP Server & Toolchain (sac-mcp-server)MCP Server & CLI Toolchain chuyên biệt để đọc, thiết kế, kiểm định và tự động tạo file Subassembly (.pkt) cho Autodesk Civil 3D Subassembly Composer.Tạo / sửa: Civil 3D 2025, 2026, 2027.Đọc / kiểm định: Hỗ trợ thêm Civil 3D 2024.1. Cài Đặt NhanhPowerShell# 1. Clone repo
git clone https://github.com/CrisHoa/MCP-SUBBASEMBLY-For-Civil-3D.git
cd "MCP-SUBBASEMBLY-For-Civil-3D"

# 2. Cài môi trường Python & tự cấu hình đường dẫn MCP + Skill
python -m venv .venv
.\.venv\Scripts\pip install -e ".[dev]"
.\sac-cli.bat skill setup --global-skill
2. Công Cụ CLI (sac-cli.bat)PowerShell# Kiểm định 3 tầng một file .pkt (thêm --doc để mở bằng SubassemblyDocument, --no-native để bỏ Tầng 3)
.\sac-cli.bat validate "D:\duong\dan\file.pkt"

# Dựng nhanh và tự động kiểm định
.\sac-cli.bat build --giaco                            # Sub Gia Cố Mái Taluy
.\sac-cli.bat build --sub7                             # Bộ 7 Subassembly chuẩn (chỉ tham số)
.\sac-cli.bat build --all --out "D:\Xuat\SUB PHU YEN"  # Dựng tất cả ra thư mục chỉ định

# Chạy kiểm thử
.\sac-cli.bat test
Thứ tự ưu tiên thư mục xuất: --out → biến môi trường SAC_OUTPUT_DIR → mặc định ~/Desktop/SUB PHU YEN.3. Kiểm Định 3 Tầng & Cơ Chế An ToànPlaintext[.pkt] ──> Tầng 1: OPC & XML ──> Tầng 2: XAML tĩnh & Ngữ nghĩa ──> Tầng 3: DLL gốc của SAC
Tầng 1 (OPC & XML): Kiểm tra đủ 6 file GUID (.atc, .cfg, .xaml, .pvd, .emd, .cdmd), [Content_Types].xml và cú pháp XML.Tầng 2 (XAML tĩnh): Chạy được khi máy không cài SAC. Kiểm tra UTF-8 BOM, biểu thức VB.NET, thẻ activity, thuộc tính bắt buộc và tham chiếu Point/Link/Flowchart (semantic_checks.py).Tầng 3 (Native SAC): Chạy qua SacHost.exe (tự biên dịch lần đầu bằng csc.exe, giữ tiến trình nền ~10 ms/file). Tự chọn đúng bản SAC theo .cfg (ghi đè qua SAC_INSTALL_DIR) để biên dịch biểu thức VB và bắt lỗi biến/kiểu dữ liệu.Sửa file an toàn: Mọi tool sửa .pkt đều ghi ra file tạm → kiểm định Tầng 1–2 → tự sao lưu .pkt.bak → thay thế nguyên tử (os.replace). Lỗi Tầng 3 khi lưu chỉ báo warnings (tắt bằng SAC_MCP_NATIVE_ON_SAVE=0).4. Bộ 27 Công Cụ MCPNhómCác công cụ chínhĐọc & Tra cứuinspect_pkt, validate_pkt_native, get_sac_reference_and_formulas, list_examples_and_split_catalogKhởi tạo & Speccreate_pkt_from_template, generate_assembly_recipe, export_spec, build_from_specHình họcadd_point_and_link, add_link, add_shape, add_fillet_arc, add_curve, add_offset_geometry, add_loop_geometry, add_intersection_point, add_strip_surface, add_get_mark_point / add_set_mark_pointTham số & Logicadd_parameter, add_define_variable / add_set_variable, add_set_output_parameter, add_flow_decision, add_report_messageChỉnh sửa luồngupdate_node (tự cập nhật tham chiếu khi đổi tên), remove_node (tự nối lại luồng)Nối node (parent_node_id): Bỏ trống để nối mọi nhánh mở hội tụ về node mới; truyền __ReferenceIDn để chèn ngay sau FlowStep; truyền __ReferenceIDn:True / :False để chèn vào nhánh FlowDecision.Tên đối tượng: Mặc định không được trùng (truyền allow_duplicate_name=True nếu dùng lại tên ở hai nhánh loại trừ nhau).5. Tích Hợp AI Coding AgentsSkill sac-subassembly-design (chuẩn Agent Skills) đi kèm quy trình thiết kế và các mẫu đã kiểm chứng (reference/patterns.md).Công cụThư mục SkillCấu hình MCP sacClaude Code.claude/skills/ (bản gốc)Cấu hình MCP của Claude CodeGoogle Antigravity.agents/skills/ (bản sao).agents/mcp_config.jsonOpenCode.claude/skills/ & .agents/skills/opencode.jsonSau khi sửa skill ở .claude/skills/, chạy .venv\Scripts\python.exe scripts\sync_agent_skills.py để đồng bộ sang .agents/skills/.6. Cộng Tác Huấn Luyện Skill (skill/*)Hỗ trợ nhiều thành viên đóng góp mẫu .pkt hoặc quy tắc mới trên nhánh Git riêng mà không xung đột (chi tiết xem CONTRIBUTING_SKILL.md):PowerShell# 1. Tạo nhánh huấn luyện riêng (tự thêm tiền tố skill/)
.\sac-cli.bat skill branch minh-tuong-chan --author "Minh"

# 2a. Học từ file .pkt chuẩn (kiểm định 3 tầng -> trích Spec -> sinh bài học -> đồng bộ)
.\sac-cli.bat skill learn "C:\Path\To\CauKien.pkt" --title "Tường chắn BTCT" --author "Minh" --notes "Gốc tại P1"

# 2b. Hoặc ghi chú quy tắc / công thức VB
.\sac-cli.bat skill note --title "Quy tắc gốc bó vỉa" --content "Đặt Origin tại P4 hoặc P10..." --author "Minh"

# 3. Kiểm tra đồng bộ & đẩy lên GitHub (tự in link tạo PR)
.\sac-cli.bat skill check
.\sac-cli.bat skill push -m "Huấn luyện mẫu tường chắn BTCT"

# 4. (Quản trị viên) Xem và gộp nhánh
.\sac-cli.bat skill branches --fetch
.\sac-cli.bat skill merge skill/minh-tuong-chan
