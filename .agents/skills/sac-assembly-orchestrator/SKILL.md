---
name: sac-assembly-orchestrator
description: Ghép nối tổ hợp nhiều Subassembly (.pkt) thành mặt cắt ngang hoàn chỉnh (Assembly) trong Civil 3D, đồng bộ điểm nối MarkPoint (SetMarkPoint/GetMarkPoint), kiểm tra tính liên tục của bề mặt Top/Datum và lập bảng chuẩn hóa mã Code (Point/Link/Shape Codes) phục vụ tính khối lượng QTO và xuất 3D Solid BIM.
---

> **Bản quyền © 2025-2026 CrisHoa. Bảo lưu mọi quyền.** Skill này là tài sản độc quyền, chỉ dành cho người được cấp phép. Cấm sao chép, chia sẻ, đăng lại, chỉnh sửa hoặc dùng để tạo skill / prompt / mô hình AI khác khi chưa được phép bằng văn bản. Xem file `LICENSE` trong kho mã. *Copyright © 2025-2026 CrisHoa. All rights reserved. Proprietary - do not copy or redistribute.*

# Ghép Nối Tổ Hợp Subassembly, Chuẩn Hóa Bề Mặt & Khối Lượng (`sac-assembly-orchestrator`)

Skill này điều phối việc **kết hợp nhiều file `.pkt` độc lập** thành một **Tổ hợp Mặt cắt ngang hoàn chỉnh (Civil 3D Assembly)**, đảm bảo khi chạy **Corridor** không bị đứt gãy điểm nối, không bị thủng bề mặt `Top` / `Datum` và bóc tách chính xác 100% khối lượng đào đắp, kết cấu áo đường cũng như xuất mô hình 3D Solid BIM.

---

## 1. Khi Nào Sử Dụng Skill Này

- Người dùng muốn ghép nhiều cấu kiện `.pkt` lại với nhau trên một mặt cắt ngang đường (VD: *Kết cấu mặt đường mới + Mở rộng nâng cấp + Bó vỉa / Gờ phân cách + Rãnh biên / Phui đào cống + Tường chắn + Gia cố mái taluy + Vét hữu cơ & Đánh cấp*).
- Người dùng cần kiểm tra xem các file `.pkt` trong bộ thư viện có khớp điểm nối (`Origin` / `MarkPoint`) và đồng nhất bộ mã `Point/Link/Shape Codes` hay chưa.
- Người dùng muốn lập bảng **Code Set Style** và danh mục vật liệu **Compute Materials (QTO)** cho Civil 3D từ bộ file `.pkt` hiện có.

---

## 2. Quy Tắc Ghép Nối Chuỗi Cấu Kiện Trên Mặt Cắt Ngang (Assembly Chain)

Một mặt cắt ngang đường tiêu chuẩn đi từ **Tim tuyến (Baseline)** ra **Ranh giải phóng mặt bằng (Daylight)** theo thứ tự ghép nối sau:

```text
[Tim đường (Baseline)]
   ├── 1. Dải phân cách giữa (GPC_DUONGQL13) ──(Gốc P1 hoặc P10)
   ├── 2. Kết cấu mặt đường mới (07_KetCauMatDuongMoi) / Đường cũ cải tạo (04, 06)
   ├── 3. Bó vỉa & Đan rãnh (BV_QL13_PHAI / TRAI) ──(Gốc P1 giáp mặt đường, hoặc Gốc P4 giáp vỉa hè)
   ├── 4. Phui đào cống dọc / Hố ga (01_PhuiDaoCong)
   ├── 5. Tường chắn / Gờ chắn (09_TuongChan_Cat_III_III)
   └── 6. Taluy đào đắp / Gia cố mái taluy (05_TaluyDaoDapDayDu / 08_GiaCoMaiTaluy_GiatCo)
          └── 7. Vét hữu cơ & Đánh cấp dưới chân đắp (02_VetHuuCo_DanhCap)
```

### Hai phương pháp truyền điểm nối giữa các Subassembly:
1. **Ghép trực tiếp qua Điểm Gốc (`Origin Attachment`)**:
   - Subassembly sau được gắn (Attach) trực tiếp vào một Point cụ thể ở mép ngoài của Subassembly trước.
   - Nếu cần gắn ngược từ mép trong ra mép ngoài (như gắn Bó vỉa từ mép vỉa hè vào mặt đường, hoặc gắn GPC từ mép đất giữa ra làn xe), dùng skill `sac-pkt-refactor` để dời `Origin` của `.pkt` về đúng điểm tiếp giáp (`P4` hoặc `P10`).
2. **Ghép qua Điểm Đánh Dấu (`SetMarkPoint` $\rightarrow$ `GetMarkPoint`)**:
   - Subassembly phía trước gọi `add_set_mark_point(point_number="P_Mep", mark_name="MARK_TALUY")`.
   - Subassembly phía sau gọi `add_get_mark_point(point_number="P_BatDau", mark_name="MARK_TALUY")`.
   - **Quy tắc bắt buộc**: Trong Assembly của Civil 3D, Subassembly chứa `SetMarkPoint` phải nằm **trước** Subassembly chứa `GetMarkPoint` trong cây Construction thứ tự thực thi của Assembly.

---

## 3. Kiểm Định Tính Liên Tục Của Bề Mặt Corridor (`Top` & `Datum`)

Khi dùng `inspect_pkt` rà soát một nhóm file `.pkt` sẽ ghép chung vào 1 Assembly, luôn kiểm tra 3 tiêu chí sống còn sau:

1. **Tính liên tục của đường `Top` (Bề mặt hoàn thiện)**:
   - Mọi `Link` nằm trên bề mặt trên cùng tiếp xúc không khí (mặt bê tông nhựa, mặt đan rãnh, mặt vát bó vỉa, đỉnh tường chắn, mặt mái taluy) phải được gán mã `"Top"`.
   - **Cấm gán `"Top"` cho cạnh vách đứng bên trong** (như vách tiếp giáp giữa mặt đường và lưng bó vỉa) để tránh bề mặt TIN của Civil 3D bị dựng vách đứng giả hoặc lỗi tam giác chồng đè.
2. **Tính liên tục của đường `Datum` (Bề mặt đáy đào nền)**:
   - Mọi `Link` nằm ở đáy dưới cùng của kết cấu tiếp giáp với nền đất tự nhiên/đất đắp (`Đáy móng cấp phối`, `Đáy bê tông lót`, `Lớp giấy dầu`, `Đáy phui đào`) phải có mã `"Datum"`.
   - Khi tạo `Corridor Surface -> Datum` trong Civil 3D với `Overhang Correction = Bottom Links`, mặt `Datum` sẽ chạy mượt qua đáy mọi kết cấu để tính đúng khối lượng đào nền.
3. **Tính khép kín và phân biệt mã `Shape Codes` (Bóc tách khối lượng QTO)**:
   - Không để 2 vật liệu khác mác dùng chung 1 `Shape Code`.

---

## 4. Bảng Quy Chuẩn Mã Code Chuẩn Hóa Cho Civil 3D & BIM (QĐ 258 / IFC 4x3)

Khi thiết kế mới hoặc chuẩn hóa bộ `.pkt` cho dự án, sử dụng bảng mã thống nhất sau để phối hợp mượt mà với các skill `civil-corridor-engineer`, `civil-section-engineer` và `civil-bim-engineer`:

| Nhóm Cấu Kiện | Shape Code (Tính thể tích $m^3$) | Link Code (Tính diện tích $m^2$ / Tạo Surface) | Point Code (Tạo Feature Line / Nhãn trắc ngang) |
| :--- | :--- | :--- | :--- |
| **Áo đường mới** | `BTN_C12.5`, `BTN_C19`, `CPDD_Dmax25`, `CPDD_Dmax37.5`, `K98` | `Top`, `Pave`, `Base`, `Subbase`, `Datum` | `Crown`, `ETW`, `EPS`, `Subgrade` |
| **Bó vỉa & Đan rãnh** | `BV` (Bê tông bó vỉa), `BV.BTL` (Bê tông lót bó vỉa) | `Top`, `Curb`, `Gutter`, `Datum` | `BV.1` .. `BV.9`, `Flange`, `Flowline_Gutter` |
| **Gờ phân cách (GPC)** | `BN1.M250` (Thân gờ M250), `BN1.M150` (Lót gờ M150) | `Top`, `Barrier`, `Datum` | `BN1.P1` .. `BN1.P10` |
| **Tường chắn trọng lực** | `BT_M300`, `ThanTuong`, `BTCT_M300`, `BanMong`, `BT_M150`, `BTLot` | `Top`, `Chamfer`, `Wall_Front`, `Wall_Back`, `FootingBottom`, `GiayDau`, `Membrane`, `Datum` | `Top_Left`, `Chamfer_Top`, `Chamfer_Side`, `FootingTop_L`, `FootingTop_R`, `BeddingBottom_L`, `BeddingBottom_R` |
| **Gia cố mái taluy** | `S_TamGiaCo`, `S_LopLot`, `S_ChanKhayGC`, `S_GoChanDinh` | `Top`, `Daylight`, `MaiTaluy`, `MatCo`, `ChanKhay`, `Day_Lot` | `DinhTaluy`, `DinhCo`, `MatCo`, `ChanTaluy` |
| **Phui đào & Đánh cấp** | `Dao_Cong`, `Dem_Cong`, `Vet_Huu_Co`, `Danh_Cap` | `Datum`, `Trench_Bottom`, `Link_VHC`, `Bench` | `Trench_L`, `Trench_R`, `Daylight_Cut`, `Daylight_Fill` |

---

## 5. Quy Trình Lập Hồ Sơ Bàn Giao Bộ Subassembly Cho Dự Án

Khi người dùng yêu cầu kiểm tra hoặc bàn giao một bộ nhiều file `.pkt`:
1. Chạy `inspect_pkt` và `validate_pkt_native` cho từng file `.pkt` trong bộ.
2. Tổng hợp **Bảng Ma Trận Mã Code (Master Code Matrix)** liệt kê tất cả `Shape Codes`, `Link Codes`, `Point Codes` và `Target Parameters` của toàn bộ các file `.pkt`.
3. Hướng dẫn thứ tự gắn từng `.pkt` vào `Assembly` trong Civil 3D (gắn điểm nào vào điểm nào, gán `Surface Target` vào đâu) để kỹ sư Civil 3D lắp ráp không sai sót.
