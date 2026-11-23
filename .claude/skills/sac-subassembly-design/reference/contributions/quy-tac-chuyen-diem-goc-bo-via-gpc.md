---
slug: quy-tac-chuyen-diem-goc-bo-via-gpc
title: "Quy tắc chuyển điểm gốc (Origin) sang P4 hoặc P10 cho Bó vỉa và Gờ phân cách"
author: "CrisHoa"
category: rule
subassembly_name: general
branch: master
updated_at: 2026-11-23
---

# Quy tắc chuyển điểm gốc (Origin) sang P4 hoặc P10 cho Bó vỉa và Gờ phân cách

- **Phân loại**: `rule`
- **Người đóng góp**: `CrisHoa` (Nhánh: `master`)

## Nội Dung Hướng Dẫn

Khi thiết kế Bó vỉa (BV) hoặc Gờ phân cách (GPC) cần bám vào mép đỉnh trong hoặc mép phải: đặt StartNode là điểm gốc mới (P4 hoặc P10) tại tọa độ (0,0), dựng chuỗi điểm nối tiếp theo chu vi khép kín và dùng biến động [B_RV] thay vì số cứng để đỉnh và đáy co giãn đồng bộ khi thay đổi thông số trong Civil 3D.
