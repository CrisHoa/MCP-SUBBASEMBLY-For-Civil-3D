> **Proprietary software — © 2025-2026 CrisHoa. All rights reserved.** Copying, forking, redistributing or reusing the code, skills or reference content without written permission is prohibited. See [LICENSE](LICENSE).

## 1. Setup

Requires Python 3.10+ on PATH (Git for Windows for the git hooks).

**Automatic (Claude Code):** `git clone`, open Claude Code in the repo folder and trust it. The `SessionStart` hook in `.claude/settings.json` runs `scripts/sac_auto_setup.py`, which installs everything missing (first run ≈ 1 min, later runs ≈ 0.2 s and silent). **Open a second session** to get the `sac` tools — MCP servers load only at session start.

**Manual (any agent):** run once from the repo folder:

```powershell
.\setup.bat
```

**Auto-update after `git pull`:** setup sets `git config core.hooksPath .githooks`, so `post-merge` / `post-rewrite` / `post-checkout` re-run the quick check after every pull or branch switch: changed skills are re-copied, and dependencies are reinstalled only when `pyproject.toml` changed.

Setup creates `.venv`, installs the dependencies, then runs `sac-cli skill setup`, which writes the paths of **this machine** into (`.agents/mcp_config.json` and `opencode.json` are generated per machine and git-ignored):

| Agent | MCP server `sac` | Skills |
| :--- | :--- | :--- |
| **Claude Code** | `~/.claude.json` → `mcpServers.sac` (backup: `~/.claude.json.bak-sac`) | copied to `~/.claude/skills/` (usable from any folder) |
| **Google Antigravity** | `.agents/mcp_config.json` | `.agents/skills/` (+ `~/.gemini/config/skills/` with `--global-skill`) |
| **OpenCode** | `opencode.json` | `.claude/skills/` & `.agents/skills/` |

Options are passed through: `.\setup.bat --global-skill` (also sync to Gemini), `.\setup.bat --no-claude` (skip Claude Code).

Then **open a new Claude Code session** — the `sac` tools and the 4 `sac-*` skills load at session start.

> Do not move or rename the repo folder after setup (the MCP path is absolute). If you do, run `.\setup.bat` again.

## 2. CLI Tool (`sac-cli.bat`)

```powershell
# Run 3-tier validation (add --doc for SubassemblyDocument, --no-native to skip Tier 3)
.\sac-cli.bat validate "path\to\file.pkt"

# Build and auto-validate
.\sac-cli.bat build --giaco                       # Slope Protection Subassembly
.\sac-cli.bat build --sub7                        # Standard 7-Subassembly Suite (parameters only)
.\sac-cli.bat build --all --out "path\to\output"  # Build all to a custom directory

# Run test suite
.\sac-cli.bat test
```

## 3. 3-Tier Validation & Safe Editing

`[.pkt] → Tier 1 (OPC & XML) → Tier 2 (Static XAML) → Tier 3 (Native SAC DLLs)`

- **Tier 1 (OPC & XML)**: Verifies all 6 GUID files (`.atc`, `.cfg`, `.xaml`, `.pvd`, `.emd`, `.cdmd`), `[Content_Types].xml`, and XML syntax.
- **Tier 2 (Static XAML)**: Runs without SAC installed. Checks UTF-8 BOM, VB.NET expressions, activity tags, required attributes, and Point/Link/Flowchart references (`semantic_checks.py`).
- **Tier 3 (Native SAC)**: Runs via `SacHost.exe` (auto-compiled on first run via `csc.exe`, ~10 ms/file). Matches the SAC version from `.cfg` (overridable via `SAC_INSTALL_DIR`) to compile VB expressions and catch undeclared variable/type errors.
- **Safe File Editing**: Writes to a temp file → runs Tier 1–2 validation → backs up original as `.pkt.bak` → atomic swap (`os.replace`). Tier 3 errors on save report as non-blocking warnings (disable via `SAC_MCP_NATIVE_ON_SAVE=0`).

## 4. 32 MCP Tools & 4 Built-in Agent Skills

| Category | Core Tools |
| :--- | :--- |
| **Read & Reference** | `inspect_pkt`, `validate_pkt_native`, `get_sac_reference_and_formulas`, `list_examples_and_split_catalog` |
| **Creation & Spec** | `create_pkt_from_template`, `generate_assembly_recipe`, `export_spec`, `build_from_spec` |
| **Geometry** | `add_point_and_link`, `add_link`, `add_shape`, `add_fillet_arc`, `add_curve`, `add_offset_geometry`, `add_loop_geometry`, `add_intersection_point`, `add_strip_surface`, `add_get_mark_point`, `add_set_mark_point` |
| **Parameters & Logic** | `add_parameter`, `add_define_variable`, `add_set_variable`, `add_set_output_parameter`, `add_flow_decision`, `add_report_message` |
| **Flowchart Editing** | `update_node` (auto-updates references on rename), `remove_node` (auto-reconnects flow) |
| **Collaborative Skill Training** | `skill_start_branch`, `skill_learn_pkt`, `skill_add_note`, `skill_submit_branch`, `skill_list_branches` |

- **Flowchart Wiring (`parent_node_id`)**: Leave empty to converge all open branches; pass `__ReferenceIDn` to insert after a FlowStep; pass `__ReferenceIDn:True` or `:False` for a FlowDecision branch.
- **Object Naming**: Unique by default (pass `allow_duplicate_name=True` for mutually exclusive branches).

### Included Agent Skills (`.claude/skills/` & `.agents/skills/`)

| Skill Name | Purpose |
| :--- | :--- |
| **`sac-subassembly-design`** | Full workflow for designing, editing, and 3-tier validating `.pkt` subassemblies from scratch. |
| **`sac-pkt-refactor`** | Re-anchor Origin (`P1` → `P4`, `P10`, etc.), Mirror Left ↔ Right (`TR` ↔ `PH`), parameterize hardcoded literals, and migrate Civil 3D versions (`2025`/`2026`/`2027`) from existing or currently open SAC `.pkt` files. |
| **`sac-cad-to-pkt`** | Dissect CAD cross-section drawings (`DWG`/`DXF`/`PDF`/screenshots), convert `cm`/`mm` to `m`, split material zones (`Shapes`), and build verified `.pkt` packages. |
| **`sac-assembly-orchestrator`** | Connect multi-subassembly chains into Civil 3D Assemblies via `Origin` / `MarkPoint`, verify `Top` & `Datum` surface continuity, and standardize `Point/Link/Shape Codes` for QTO & 3D Solid BIM. |

## 5. AI Coding Agent Integration

| Tool | Skill Directory | MCP Config |
| :--- | :--- | :--- |
| **Claude Code** | `.claude/skills/` (source of truth) → `~/.claude/skills/` | `~/.claude.json` (written by `setup.bat`) |
| **Google Antigravity** | `.agents/skills/` (mirror) | `.agents/mcp_config.json` |
| **OpenCode** | `.claude/skills/` & `.agents/skills/` | `opencode.json` |

After editing `.claude/skills/`, sync to `.agents/skills/` via:
```powershell
.venv\Scripts\python.exe scripts\sync_agent_skills.py
```

## 6. Collaborative Skill Training (`skill/*`)

Contributors can add `.pkt` templates or design rules on isolated Git branches without merge conflicts (see [CONTRIBUTING_SKILL.md](CONTRIBUTING_SKILL.md)):

```powershell
# 1. Create a training branch (auto-prefixed with skill/)
.\sac-cli.bat skill branch retaining-wall --author "YourName"

# 2a. Learn from a verified .pkt (3-tier validate -> extract Spec -> generate lesson -> sync)
.\sac-cli.bat skill learn "path\to\Component.pkt" --title "RC Retaining Wall" --author "YourName" --notes "Origin at P1"

# 2b. Or add a rule / VB formula / troubleshooting note
.\sac-cli.bat skill note --title "Curb Origin Rule" --content "Place Origin at P4 or P10..." --author "YourName"

# 3. Verify sync & push (prints a ready-to-use PR link)
.\sac-cli.bat skill check
.\sac-cli.bat skill push -m "Train RC retaining wall pattern"

# 4. (Maintainers) List and merge contributor branches
.\sac-cli.bat skill branches --fetch
.\sac-cli.bat skill merge skill/retaining-wall
```

## License

Proprietary — **all rights reserved** (see [LICENSE](LICENSE)). Access is granted only to people invited by the copyright holder, for their own use; copying, sharing, publishing, modifying or using the skills / reference content to build other skills, prompts or AI models requires written permission. Contributions are assigned to the copyright holder.
