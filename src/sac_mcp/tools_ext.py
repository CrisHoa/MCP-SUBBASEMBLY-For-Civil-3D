"""
Nhóm tool mở rộng cho SAC MCP Server: sửa / xoá node có sẵn và spec khai báo (JSON) của Subassembly.

Server gọi `register(mcp, _mutate_pkt, _safe_tool)` ở cuối server.py để đăng ký 4 tool:
  - remove_node, update_node (sửa file, đi qua khung _mutate_pkt: kiểm định + sao lưu .bak)
  - export_spec, build_from_spec (đọc / tạo mới, bọc bằng _safe_tool)
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Callable, Dict, Literal, Optional

from sac_mcp.core.node_editor import remove_node as _remove_node
from sac_mcp.core.node_editor import update_node as _update_node
from sac_mcp.core.spec_builder import build_from_spec as _build_from_spec
from sac_mcp.core.spec_builder import export_spec as _export_spec
from sac_mcp.models.schemas import MutationResult


def _native_issue_warnings(pkt_path: str) -> list:
    """Chạy kiểm định 3 tầng sau khi dựng và trả các lỗi dưới dạng cảnh báo (tắt bằng SAC_MCP_NATIVE_ON_SAVE=0)."""
    if os.environ.get("SAC_MCP_NATIVE_ON_SAVE", "1") == "0":
        return []
    from sac_mcp.core.validator import PktValidator

    rep = PktValidator.validate_pkt(pkt_path, run_native_test=True)
    return [f"[{i.category}] {i.message}" for i in rep.issues if i.severity == "ERROR"]


def register(mcp: Any, mutate_pkt: Callable[..., str], safe_tool: Callable[[str], Callable]) -> None:
    """Đăng ký các tool mở rộng lên instance MCP server `mcp`."""

    @mcp.tool()
    def remove_node(pkt_path: str, node_id: str, keep_branch: Optional[Literal["True", "False"]] = None) -> str:
        """
        Xoá một node (FlowStep hoặc FlowDecision) khỏi Flowchart và tự NỐI LẠI luồng:
        mọi nhánh đang trỏ vào node bị xoá (kể cả StartNode) sẽ trỏ sang phần luồng phía sau nó.
        Hỗ trợ cả file do SAC lưu (node lồng inline) lẫn file do builder sinh (x:Reference).
        Cảnh báo nếu Point / Link mà node định nghĩa vẫn còn được activity khác tham chiếu.

        Args:
            pkt_path: Đường dẫn tới file .pkt cần chỉnh sửa.
            node_id: reference_id của node cần xoá (VD: '__ReferenceID4'), xem bằng inspect_pkt.
            keep_branch: Chỉ dùng khi xoá FlowDecision có 2 nhánh khác nhau: 'True' hoặc 'False' là nhánh
                         được giữ lại để nối tiếp; nhánh còn lại bị tách khỏi luồng (có cảnh báo).
        """
        def _apply(pkg, engine):
            info = _remove_node(engine, node_id, keep_branch=keep_branch)
            cont = info["continuation_node_id"] or "(trống - cuối luồng)"
            msg = (
                f"Đã xoá {info['node_kind']} '{info['removed_node_id']}'; nối lại {len(info['rewired'])} nhánh "
                f"sang '{cont}'."
            )
            return info, msg, []

        return mutate_pkt("remove_node", pkt_path, _apply)

    @mcp.tool()
    def update_node(
        pkt_path: str,
        node_id: str,
        attributes: Optional[Dict[str, Any]] = None,
        arguments: Optional[Dict[str, Any]] = None,
        rename_references: bool = True,
    ) -> str:
        """
        Sửa một node có sẵn trong Flowchart mà không phải xoá rồi tạo lại.
        - FlowStep: sửa thuộc tính của activity bên trong (VD: CreatePoint: 'FromPoint', 'PointNumber',
          'DisplayName', 'ApplyAOR', 'PointCodes'; CreateLink: 'StartPoint', 'EndPoint', 'LinkCodes'...).
          Tên thuộc tính phải có trong danh mục activity của SAC, nếu không sẽ bị từ chối.
        - FlowDecision: chỉ sửa 'Condition' (biểu thức VB, tự bọc [..]) và 'DisplayName'.

        Args:
            pkt_path: Đường dẫn tới file .pkt cần chỉnh sửa.
            node_id: reference_id của node (VD: '__ReferenceID3'), xem bằng inspect_pkt.
            attributes: (Tùy chọn) {tên thuộc tính: giá trị}. Thuộc tính tên / mã / enum (PointNumber, FromPoint,
                        Links, CreationType, DisplayName...) ghi nguyên văn; thuộc tính số nhận số hoặc biểu thức VB
                        (tự bọc [..], VD {"OffsetDistance": "-W/10"}); null -> {x:Null}; '*Codes' nhận danh sách
                        hoặc chuỗi phân tách dấu phẩy (VD: {"PointCodes": ["Crown", "Top"]}).
                        Đổi CreationType của cung phải truyền kèm đối số tương ứng (ArcGeneral -> CenterPoint,
                        Arc3Points -> ArcPoint2, ParabolaGeneral -> MidOrdinate). Đổi VariableType của biến nội bộ
                        tự cập nhật khai báo biến và các khối Set gán cho biến đó.
            arguments: (Tùy chọn) {x:Key: giá trị} của các InArgument (VD: {"DeltaX1": "B_lan", "DeltaY1": "-t1"},
                       Slope2 / DeltaX2 cho Slope_DeltaX, SurfaceTarget3...). Biểu thức tự bọc [..], số giữ nguyên.
                       Với SetVariableValue / CustomErrorReportActivity dùng tên property: 'VariableValue', 'Message'.
                       Giá trị dạng {"value": "[Targ]", "type": "asw:OffsetTarget"} để chỉ rõ kiểu; null để xoá đối số.
            rename_references: Khi đổi tên PointNumber / LinkNumber / AutoLinkGeometryName...: True (mặc định) tự
                       cập nhật mọi tham chiếu (FromPoint, StartPoint, EndPoint, Links, FirstLink/SecondLink,
                       CenterPoint/ArcPoint2, biểu thức 'P4.X'); False chỉ cảnh báo danh sách chỗ còn dùng tên cũ.
        """
        def _apply(pkg, engine):
            info = _update_node(engine, node_id, attributes, arguments, rename_references=rename_references)
            n = len(info["changed_attributes"]) + len(info["changed_arguments"])
            msg = f"Đã cập nhật {n} giá trị của {info['activity']} trong node '{info['node_id']}'."
            return info, msg, []

        return mutate_pkt("update_node", pkt_path, _apply)

    @mcp.tool()
    @safe_tool("export_spec")
    def export_spec(pkt_path: str, output_json_path: Optional[str] = None) -> str:
        """
        Xuất một file .pkt thành SPEC khai báo dạng JSON: tên, phiên bản Civil 3D, mô tả, danh sách Parameter
        và danh sách 'steps' theo đúng thứ tự dựng (point / link / shape / decision / define_variable /
        set_variable / report ...). Nhánh của FlowDecision ghi bằng 'parent': '<id>:True' (dùng id của bước,
        không dùng __ReferenceID). Activity chưa hỗ trợ được xuất dạng {"type": "raw", ...}.
        Sửa spec rồi gọi build_from_spec để dựng lại file .pkt. Định dạng: docs/spec_format.md.

        Args:
            pkt_path: Đường dẫn tới file .pkt cần xuất.
            output_json_path: (Tùy chọn) Đường dẫn file .json để ghi spec ra đĩa (UTF-8).
        """
        spec = _export_spec(pkt_path)
        written = None
        if output_json_path:
            out = Path(output_json_path).resolve()
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps(spec, ensure_ascii=False, indent=2), encoding="utf-8")
            written = str(out)
        return json.dumps(
            {
                "success": True,
                "action": "export_spec",
                "pkt_path": str(Path(pkt_path).resolve()),
                "output_json_path": written,
                "step_count": len(spec.get("steps", [])),
                "parameter_count": len(spec.get("parameters", [])),
                "spec": spec,
            },
            ensure_ascii=False,
            indent=2,
        )

    @mcp.tool()
    @safe_tool("build_from_spec")
    def build_from_spec(
        spec_json: str,
        output_path: str,
        civil_version: Optional[Literal["2025", "2026", "2027"]] = None,
    ) -> str:
        """
        Dựng một file .pkt hoàn chỉnh từ SPEC khai báo (định dạng của export_spec, xem docs/spec_format.md):
        tạo từ template chuẩn, thêm Parameter, chạy lần lượt các bước qua builder, lưu MỘT lần rồi kiểm định 3 tầng.
        Spec sai được báo lỗi kèm vị trí 'steps[i]' trước khi ghi bất kỳ file nào.

        Args:
            spec_json: Nội dung spec dạng chuỗi JSON, HOẶC đường dẫn tới file .json chứa spec.
            output_path: Đường dẫn file .pkt sẽ tạo (ghi đè nếu đã có, bản cũ sao lưu thành .pkt.bak).
            civil_version: (Tùy chọn) Ghi đè phiên bản Civil 3D trong spec ('2025', '2026', '2027').
        """
        res = _build_from_spec(spec_json, output_path, civil_version=civil_version)
        warnings = list(res["warnings"]) + _native_issue_warnings(res["pkt_path"])
        out = MutationResult(
            success=True,
            pkt_path=res["pkt_path"],
            action="build_from_spec",
            message=(
                f"Đã dựng '{Path(res['pkt_path']).name}' từ spec ({len(res['reference_ids'])} bước, "
                f"Civil 3D {res['civil_version']})."
            ),
            created_reference_ids=list(res["reference_ids"].values()),
            details={"step_reference_ids": res["reference_ids"], "civil_version": res["civil_version"]},
            warnings=warnings,
            backup_path=res.get("backup_path"),
        )
        return json.dumps(out.model_dump(), ensure_ascii=False, indent=2)

    @mcp.tool()
    @safe_tool("skill_start_branch")
    def skill_start_branch(
        branch_name: str,
        author: str = "",
        base_branch: str = "",
    ) -> str:
        """
        Tạo hoặc chuyển sang nhánh Git huấn luyện Skill cộng tác (dạng `skill/<ten-nhanh>`).
        Dùng khi thành viên mới bắt đầu một phiên dạy / đóng góp mẫu cấu kiện hoặc quy tắc mới vào Skill.

        Args:
            branch_name: Tên nhánh huấn luyện (VD: 'minh-cong-hop' -> tự chuẩn hóa thành 'skill/minh-cong-hop').
            author: (Tùy chọn) Tên người huấn luyện / đóng góp.
            base_branch: (Tùy chọn) Nhánh gốc để rẽ nhánh.
        """
        from sac_mcp.core import skill_trainer as _st

        info = _st.start_training_branch(branch_name=branch_name, author=author, base_branch=base_branch)
        return json.dumps({"success": True, "action": "skill_start_branch", **info}, ensure_ascii=False, indent=2)

    @mcp.tool()
    @safe_tool("skill_learn_pkt")
    def skill_learn_pkt(
        pkt_path: str,
        title: str,
        author: str = "",
        notes: str = "",
        category: str = "pattern",
        slug: str = "",
    ) -> str:
        """
        Huấn luyện một file `.pkt` chuẩn vào Skill `sac-subassembly-design`:
        1. Kiểm định 3 tầng file `.pkt` (chặn nếu file lỗi).
        2. Trích xuất Spec JSON (`export_spec`) và lưu bản mẫu vào `examples/skill_contributions/<slug>/`.
        3. Sinh bài học markdown độc lập tại `.claude/skills/sac-subassembly-design/reference/contributions/<slug>.md`
           (mỗi bài học 1 file riêng để nhiều người đẩy nhiều nhánh không bị xung đột Git).
        4. Cập nhật `INDEX.md` và tự động đồng bộ sang `.agents/skills/`.

        Args:
            pkt_path: Đường dẫn tới file .pkt mẫu đã dựng hoặc mở sẵn.
            title: Tiêu đề bài học / mẫu cấu kiện (VD: 'Cống hộp đôi BTCT có đệm đá dăm').
            author: (Tùy chọn) Tên thành viên đóng góp.
            notes: (Tùy chọn) Ghi chú kinh nghiệm thiết kế, quy ước mã code hoặc lưu ý cho AI.
            category: Phân loại mẫu ('pattern', 'drainage', 'wall', 'pavement', 'curb', 'slope').
            slug: (Tùy chọn) Định danh file kebab-case (tự sinh từ title nếu bỏ trống).
        """
        from sac_mcp.core import skill_trainer as _st

        run_native = os.environ.get("SAC_MCP_NATIVE_ON_SAVE", "1") != "0"
        info = _st.learn_from_pkt(
            pkt_path=pkt_path,
            title=title,
            author=author,
            notes=notes,
            category=category,
            slug=slug,
            run_native_test=run_native,
        )
        return json.dumps({"success": True, "action": "skill_learn_pkt", **info}, ensure_ascii=False, indent=2)

    @mcp.tool()
    @safe_tool("skill_add_note")
    def skill_add_note(
        title: str,
        content: str,
        author: str = "",
        category: str = "rule",
        slug: str = "",
    ) -> str:
        """
        Đóng góp bài học lý thuyết, công thức VB, quy ước đặt tên hoặc cách xử lý lỗi vào Skill
        mà không cần file .pkt, tự động cập nhật `INDEX.md` và đồng bộ `.claude/skills` <-> `.agents/skills`.

        Args:
            title: Tiêu đề quy tắc / bài học.
            content: Nội dung chi tiết (Markdown) hướng dẫn AI.
            author: (Tùy chọn) Tên người đóng góp.
            category: Phân loại ('rule', 'formula', 'troubleshooting').
            slug: (Tùy chọn) Định danh file kebab-case.
        """
        from sac_mcp.core import skill_trainer as _st

        info = _st.add_skill_note(title=title, content=content, author=author, category=category, slug=slug)
        return json.dumps({"success": True, "action": "skill_add_note", **info}, ensure_ascii=False, indent=2)

    @mcp.tool()
    @safe_tool("skill_submit_branch")
    def skill_submit_branch(
        message: str = "",
        push: bool = True,
    ) -> str:
        """
        Kiểm định toàn bộ bài học đóng góp, đồng bộ `.claude/skills` <-> `.agents/skills`,
        git commit và `git push -u origin <nhánh>` lên GitHub kèm đường dẫn tạo Pull Request.

        Args:
            message: Nội dung commit message mô tả bài học vừa huấn luyện.
            push: True (mặc định) để đẩy nhánh lên GitHub (`origin`); False nếu chỉ muốn commit cục bộ.
        """
        from sac_mcp.core import skill_trainer as _st

        run_native = os.environ.get("SAC_MCP_NATIVE_ON_SAVE", "1") != "0"
        info = _st.submit_training_branch(message=message, push=push, run_native_test=run_native)
        return json.dumps({"success": True, "action": "skill_submit_branch", **info}, ensure_ascii=False, indent=2)

    @mcp.tool()
    @safe_tool("skill_list_branches")
    def skill_list_branches(fetch: bool = False) -> str:
        """
        Liệt kê các nhánh huấn luyện Skill (`skill/*`, `train/*`) của cả nhóm và danh mục bài học đã đóng góp.

        Args:
            fetch: True để gọi `git fetch origin` cập nhật danh sách nhánh từ GitHub trước khi liệt kê.
        """
        from sac_mcp.core import skill_trainer as _st

        info = _st.list_training_branches(fetch=fetch)
        return json.dumps({"success": True, "action": "skill_list_branches", **info}, ensure_ascii=False, indent=2)
