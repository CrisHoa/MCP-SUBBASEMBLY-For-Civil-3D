---
name: sac-pkt-refactor
description: Biến đổi, tái cấu trúc, dời điểm gốc chèn (Re-anchor Origin sang P4, P10 hoặc điểm bất kỳ), lật đối xứng Trái/Phải (Mirror TR/PH), tham số hóa số cứng và chuyển đổi phiên bản Civil 3D (2025/2026/2027) cho file Subassembly Composer (.pkt) có sẵn hoặc file đang mở trực tiếp trong SAC.
---

> **Bản quyền © 2025-2026 CrisHoa. Bảo lưu mọi quyền.** Skill này là tài sản độc quyền, chỉ dành cho người được cấp phép. Cấm sao chép, chia sẻ, đăng lại, chỉnh sửa hoặc dùng để tạo skill / prompt / mô hình AI khác khi chưa được phép bằng văn bản. Xem file `LICENSE` trong kho mã. *Copyright © 2025-2026 CrisHoa. All rights reserved. Proprietary - do not copy or redistribute.*

# Biến Đổi, Dời Điểm Gốc & Lật Đối Xứng Subassembly (`sac-pkt-refactor`)

Skill này chuyên xử lý các yêu cầu **biến đổi từ một file `.pkt` có sẵn (hoặc file người dùng đang mở trong Subassembly Composer)** sang một biến thể mới mà **bảo toàn tuyệt đối 100% hình học, kích thước, mã Code (Point/Link/Shape), ảnh thumbnail và vượt qua kiểm định 3 tầng**.

---

## 1. Khi Nào Sử Dụng Skill Này

- Người dùng nói: *"Tạo cho tôi 1 sub tương tự nhưng điểm gốc nằm ở P10 / P4"*, *"Đổi điểm chèn sang đỉnh bó vỉa / đáy móng"*, *"File sub tôi đang mở"*.
- Người dùng muốn **lật đối xứng Trái $\leftrightarrow$ Phải** (từ `BV_PHAI.pkt` hoặc `GPC_TR.pkt` tạo ra bản bên kia mà không phải dựng lại từ đầu).
- Người dùng muốn **sửa số cứng (hardcoded number)** trong file `.pkt` thành tham số động (`Parameter`) để co giãn trong Civil 3D.
- Người dùng muốn **chuyển đổi phiên bản** file `.pkt` giữa Civil 3D `2025` $\leftrightarrow$ `2026` $\leftrightarrow$ `2027`.

---

## 2. Cách Tự Động Tìm File `.pkt` Người Dùng Đang Mở Trong Subassembly Composer

Khi người dùng nói *"file sub tôi đang mở"* hoặc gửi ảnh chụp màn hình Subassembly Composer mà không gửi đường dẫn file:

1. **Quét thư mục tạm của Subassembly Composer (`%TEMP%\C3DSA`)**:
   Khi SAC mở bất kỳ file `.pkt` nào, nó luôn giải nén toàn bộ nội dung (`.atc`, `.cfg`, `.xaml`, `.pvd`, `.emd`, `.cdmd`, `.png`) vào:
   ```powershell
   Get-ChildItem -Path "$env:TEMP\C3DSA" | Sort-Object LastWriteTime -Descending | Select-Object -First 5 Name, LastWriteTime
   ```
2. **Đọc cấu trúc gốc**:
   - Đọc file `<guid>.atc` và `<guid>.xaml` trong thư mục tạm mới nhất để lấy toàn bộ danh sách `Parameter`, `Point`, `Link`, `Shape`, `Code` và ảnh thumbnail (`.png`).
   - Hoặc nếu người dùng đưa đường dẫn `.pkt`, gọi ngay MCP tool `inspect_pkt(pkt_path)` và `export_spec(pkt_path)`.

---

## 3. Quy Trình Dời Điểm Gốc Chèn (`Re-anchor Origin` từ $P_1 \rightarrow P_k$)

Trong Subassembly Composer và Civil 3D, **điểm đầu tiên ngay sau `StartNode` có `FromPoint="{x:Null}"` và `(DeltaX=0, DeltaY=0)` chính là Điểm Gốc Chèn (Origin / Attachment Point)**.

Để dời điểm gốc từ điểm cũ (thường là `P1`) sang điểm mục tiêu $P_k$ (ví dụ `P4` hoặc `P10`) mà giữ nguyên hình dáng mặt cắt:

### Bước 1: Tính bảng tọa độ tuyệt đối $(X_i, Y_i)$ của mọi điểm trong hệ tọa độ cũ
Dựa vào giá trị mặc định của các `Parameter`, tính tọa độ $(X_i, Y_i)$ của tất cả các điểm $P_1 \dots P_n$ khi gốc đặt tại điểm cũ $(0, 0)$.

### Bước 2: Tịnh tiến hệ trục tọa độ về điểm gốc mới $P_k$
Tọa độ mới của mỗi điểm $P_i$ khi $P_k$ là gốc $(0, 0)$:
$$(X'_i, Y'_i) = (X_i - X_k,\; Y_i - Y_k)$$
- Điểm gốc mới $P_k$ có tọa độ $(0, 0)$.
- Mọi khoảng cách tương đối $\Delta X_{ij} = X'_j - X'_i$ và $\Delta Y_{ij} = Y'_j - Y'_i$ giữa 2 điểm bất kỳ được bảo toàn 100%.

### Bước 3: Tái sắp xếp thứ tự Flowchart (Topological Re-ordering)
Vì một điểm chỉ có thể đặt `FromPoint` từ một điểm **đã được tạo ở bước trước đó trong Flowchart**, ta tái cấu trúc chuỗi `FlowStep` bắt đầu từ $P_k$:
1. **Node 1 (`StartNode`)**: Tạo điểm $P_k$ tại `(DeltaX1=0, DeltaY1=0)`, `FromPoint={x:Null}`, `AutoLink=False`, giữ nguyên `PointCodes` của $P_k$.
2. **Các Node tiếp theo**: Đi vòng theo chu vi mặt cắt bắt đầu từ $P_k$ (ưu tiên đi xuống đáy rồi vòng lên đỉnh để các `Link` mang mã `"Top"` vẫn giữ nguyên chiều từ điểm đầu đến điểm cuối như file gốc!).
3. **Khép cạnh cuối của chu vi**: Dùng `CreateLink` (`add_link`) nối điểm cuối chu vi về lại điểm gốc $P_k$.
4. **Dựng các lớp phụ / Bê tông lót (`S2`, `S3`...)**: Từ các điểm đáy thân đã tạo, dựng tiếp các điểm đáy lót và khép `Shape`.

### Bước 4: Tham số hóa các số cứng bị lệch (Hardcoded Literal Fix)
- Kiểm tra xem trong file gốc tác giả có gõ số cứng ở một cạnh nhưng lại dùng biến ở cạnh đối diện không (ví dụ: ở đỉnh gõ cứng `DeltaX = 0.25` nhưng ở đáy lại dùng `-(B_TR + B_PH + B_RV)`).
- Thay số cứng `0.25` bằng biến `[B_RV]` tương ứng để khi người dùng đổi tham số trong Civil 3D, đa giác `Shape` luôn khép kín tuyệt đối!

---

## 4. Quy Trình Lật Đối Xứng Trái $\leftrightarrow$ Phải (`Mirror TR <-> PH`)

Khi người dùng muốn tạo file bên Trái từ file bên Phải (hoặc ngược lại):

1. **Giữ nguyên 100%**:
   - Toàn bộ danh sách `Parameter` và giá trị mặc định.
   - Toàn bộ tung độ `DeltaY1`, mã điểm (`PointCodes`), mã liên kết (`LinkCodes`), mã vùng (`ShapeCodes`).
2. **Đảo dấu hoành độ ngang**:
   - Mọi biểu thức `DeltaX1` (hoặc `Offset`) được đổi dấu:
     - `[B_PH]` $\rightarrow$ `[-B_PH]`
     - `[-B_PH]` $\rightarrow$ `[B_PH]`
     - `[-(B_TR+B_PH+B_RV)]` $\rightarrow$ `[B_TR+B_PH+B_RV]`
     - Số dương `0.25` $\rightarrow$ `-0.25`
3. **Đổi tên định danh cấu kiện trong `.atc`**:
   - Cập nhật `Tool Name`, `ItemName` và `DotNetClass` (ví dụ `BOVIA_TL13_PHAI` $\rightarrow$ `BOVIA_TL13_TRAI`).

---

## 5. Quy Trình Kiểm Định & Bàn Giao Bắt Buộc

Sau khi tạo xong file `.pkt` mới:
1. **Bảo toàn ảnh Thumbnail**: Luôn đóng gói kèm file ảnh `.png` gốc từ gói cũ và khai báo `<Default Extension="png" ContentType="image/png" />` trong `[Content_Types].xml`.
2. **Kiểm định 3 Tầng**:
   Chạy `validate_pkt_native(pkt_path)` (hoặc `PktValidator.validate_pkt(..., run_native_test=True)`):
   - Tầng 1 (`tier1_opc_ok = True`): Đúng chuẩn gói ZIP OPC và UTF-8 BOM.
   - Tầng 2 (`tier2_xaml_ok = True`): Không có lỗi tham chiếu điểm/link hoặc node mồ côi.
   - Tầng 3 (`tier3_native_ok = True`): Biên dịch thành công bằng DLL gốc của Autodesk Subassembly Composer.
3. **Lưu ở 2 vị trí tiện lợi**:
   - Lưu 1 bản trong thư mục dự án (`examples/Sub Assembly/Bo_7_Subassembly_Chuan/...`).
   - Copy 1 bản ra ngay `C:\Users\Admin\Desktop\<TenFile>.pkt` để người dùng mở trực tiếp vào Subassembly Composer hoặc kéo thả vào Civil 3D Tool Palette.
4. **Lập bảng đối chiếu tọa độ**: In bảng so sánh tọa độ `(X, Y)` của từng điểm giữa **Bản Gốc** và **Bản Mới** để người dùng kiểm chứng trực quan ngay trong câu trả lời.
