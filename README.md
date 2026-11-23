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
# 4. (Quản trị viên) Xem và gộp nhánh
.\sac-cli.bat skill branches --fetch
.\sac-cli.bat skill merge skill/minh-tuong-chan
