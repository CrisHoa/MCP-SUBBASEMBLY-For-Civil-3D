---
name: sac-cad-to-pkt
description: Giải phẫu bản vẽ mặt cắt ngang kỹ thuật từ AutoCAD (DWG/DXF), PDF hoặc ảnh chụp màn hình mặt cắt (tỷ lệ 1/10, 1/20, 1/25, 1/50...) để tự động phân tích miền vật liệu, lập bảng tọa độ điểm, thiết kế tham số động và xuất ra file Subassembly Composer (.pkt) đạt chuẩn kiểm định 3 tầng.
---

# Giải Phẫu Bản Vẽ Mặt Cắt CAD / Ảnh Sang Subassembly (`sac-cad-to-pkt`)

Skill này hướng dẫn quy trình chuyển hóa **một bản vẽ mặt cắt ngang kết cấu hoặc đường giao thông** (từ ảnh chụp CAD, file `.dwg`/`.dxf` hoặc `.pdf`) thành **cấu kiện Subassembly `.pkt` tham số hóa 100%** cho Autodesk Civil 3D.

---

## 1. Khi Nào Sử Dụng Skill Này

- Người dùng gửi **ảnh chụp màn hình AutoCAD** một mặt cắt chi tiết (VD: *CẮT III-III TỶ LỆ 1/25*, tường chắn bê tông, gờ chắn bánh, bó vỉa, đan rãnh, rãnh biên, cống hộp, phui đào, kết cấu áo đường).
- Người dùng chỉ định một file `.dwg`/`.dxf` hoặc `.pdf` chứa chi tiết mặt cắt ngang và yêu cầu tạo file `.pkt`.

---

## 2. Quy Trình 5 Bước Giải Phẫu Mặt Cắt Sang `.pkt`

### Bước 1: Đọc Kích Thước & Quy Đổi Đơn Vị Chuẩn Mét (m)
1. **Nếu đầu vào là file `.dwg`/`.dxf`**: Kết hợp skill `doc-ban-ve-cad` để lấy toàn bộ đường bao (`LWPOLYLINE`, `LINE`, `HATCH`), kích thước (`DIMENSION`) và ghi chú vật liệu (`TEXT`, `MTEXT` giải mã TCVN3 `.VnTime`).
2. **Nếu đầu vào là ảnh chụp CAD hoặc PDF**: Đọc kỹ tất cả các đường gióng kích thước (Dim ngang, Dim đứng, Dim vát xiên, độ dốc `%` hoặc `1:m`) và các mũi tên chỉ dẫn vật liệu (Leader).
3. **Quy tắc quy đổi đơn vị sang Mét (`Units = m`)**:
   - Bản vẽ chi tiết kết cấu Việt Nam (tỷ lệ `1/10`, `1/20`, `1/25`, `1/50`) thường ghi kích thước theo **cm** (VD: `30`, `80`, `100`, `7`) hoặc **mm** (VD: `300`, `800`, `1000`, `70`).
   - Subassembly Composer trong dự án luôn dùng đơn vị **Mét (`m`)**:
     - `30 cm` (hoặc `300 mm`) $\rightarrow$ `0.30`
     - `7 cm` (hoặc `70 mm`) $\rightarrow$ `0.07`
     - `100 cm` (hoặc `1000 mm`) $\rightarrow$ `1.00`

### Bước 2: Phân Tách Các Miền Vật Liệu Khép Kín (`Shapes`) & Lớp Đáy (`Links`)
Mỗi vùng Hatch khác nhau trên bản vẽ tương ứng với **1 `Shape` riêng biệt** để Civil 3D tính khối lượng (QTO) theo đúng mác vật liệu:
- **Thân kết cấu chính** (VD: `BT M300`, `BTCT M250`): `Shape S1`
- **Bản móng / Đế kết cấu** (VD: `BTCT M300`): `Shape S2`
- **Lớp đệm / Bê tông lót** (VD: `BT lót M150`, `Đệm đá dăm`): `Shape S3`
- **Lớp màng / Giấy dầu lót móng / Vải địa kỹ thuật**: Không tạo Shape dày mà gán **`Link Code` riêng trên cạnh đáy dưới cùng** (VD: `"GiayDau", "Membrane", "Datum"`) để Civil 3D bóc diện tích trải mặt ($m^2$).

### Bước 3: Chọn Điểm Gốc Chèn (`Origin`) & Thiết Kế Bộ Tham Số (`Parameters`)
1. **Chọn Điểm Gốc (`Origin`)**:
   - Tường chắn / Gờ chắn độc lập: Đỉnh trái `P1 (0, 0)` hoặc tim móng.
   - Bó vỉa / Gờ phân cách: Mép tiếp giáp mặt đường (`P1`) hoặc mép đỉnh giáp dải phân cách (`P4`, `P10`).
   - Kết cấu áo đường / Mở rộng: Mép làn xe quy chiếu từ tim đường.
2. **Thiết kế bộ `Parameter` động** (không bao giờ đóng cứng kích thước nếu có thể tham số hóa):
   - Chiều cao / chiều dày: `H_Than`, `H_Mong`, `H_Lot`, `H_Tren`, `H_Duoi`, `H_Xien` (`Double`).
   - Bề rộng / độ vươn: `B_Dinh`, `B_Day_Than`, `B_Mui_Trai`, `B_Got_Phai`, `Vat_Dinh` (`Double`).
   - Độ dốc: `i_Mat` (`Grade`), `s_Taluy` (`Slope`).
   - Mục tiêu khống chế (nếu cần): `EG` (`SurfaceTarget`), `Target_Elevation` (`ElevationTarget`), `Target_Offset` (`OffsetTarget`).

### Bước 4: Lập Bảng Định Vị Điểm & Dựng Bằng `build_from_spec`
Thiết lập cấu trúc JSON khai báo cho `build_from_spec` (hoặc tuần tự gọi `create_pkt_from_template` $\rightarrow$ `add_parameter` $\rightarrow$ `add_point_and_link` $\rightarrow$ `add_link` $\rightarrow$ `add_shape`):
- **Kiểm tra tính khép kín của từng Shape**:
  - Một `Shape` hợp lệ phải được bao quanh bởi danh sách các `Link` tạo thành **1 chu trình khép kín đơn (Simple Closed Polygon)**.
  - Hai `Shape` liền kề (như Thân tường `S1` và Bản móng `S2`, hoặc Bản móng `S2` và Bê tông lót `S3`) **dùng chung cạnh tiếp giáp** (VD: `S2` và `S3` dùng chung cạnh đáy móng `L10`) hoặc tách đoạn rõ ràng để không hở miền.
- **Lưu ý với biến nội bộ (`Define Variable`)**:
  - Khi dùng `define_variable`, trường `default_value` chỉ truyền hằng số thuần (như `"0.0"`), sau đó mới dùng `set_variable` để gán biểu thức chứa `Parameter` (như `"B_Dinh - Vat_Dinh"`), tuyệt đối không đặt biểu thức tham số trong `DefaultValue` để tránh lỗi `NullReferenceException` khi mở trên SAC GUI.

### Bước 5: Kiểm Định 3 Tầng & Xuất Báo Cáo Nghiệm Thu
1. Gọi `validate_pkt_native(pkt_path, document_check=True)` để đảm bảo cả 3 tầng (`OPC`, `WF4 Semantics`, `Autodesk SAC Runtime DLL`) đều **PASS 100%**.
2. Lưu file `.pkt` vào thư mục dự án và copy 1 bản ra Desktop nếu người dùng đang mở SAC/Civil 3D.
3. Trình bày báo cáo nghiệm thu gồm:
   - Sơ đồ Mermaid minh họa luồng điểm & liên kết (`P1..Pn`, `L1..Lm`, `S1..Sk`).
   - Bảng thông số đầu vào (`Input Parameters`) kèm giá trị mặc định khớp bản vẽ CAD.
   - Bảng tọa độ điểm & mã Code (`Point/Link/Shape Codes`) phục vụ bóc tách khối lượng.
