# Định dạng dữ liệu kế hoạch JSON v1

Sử dụng JSON thuần UTF-8. Mẫu hợp lệ: `examples/plan-2026-10.sample.json`.

## Thuộc tính gốc

| Trường | Ý nghĩa |
|---|---|
| `schema_version` | `"1.0"` |
| `organization` | Tên Trung tâm và Nhà trường |
| `plan_id` | Định danh kế hoạch |
| `title` | Tên kế hoạch |
| `period_label` | `YYYY-MM` nếu là kế hoạch tháng |
| `period_start`, `period_end` | Ngày `YYYY-MM-DD` bao hàm ngày đầu và cuối |
| `status` | `draft`, `reviewed`, `approved`, `archived`; agent không tự gán `approved` |
| `source_register` | Danh sách `{ref, title, authority, state, date}` xác thực bởi người dùng |
| `duties` | Danh mục công tác gốc; mã duy nhất, không đếm thành sản phẩm |
| `tasks` | Mảng đầu việc có liên kết cấp và phân công |
| `capacity_targets` | Mục tiêu giờ đã được phê duyệt nếu có, `{owner, year, target_hours, source_ref}` |
| `open_questions` | Các vấn đề chưa được xác minh/phê duyệt |

## Mỗi `task`

- `id`: chuỗi duy nhất.
- `parent_id`: `null` với nhiệm vụ gốc; khác null phải trỏ đến `tasks.id`.
- `level`: một trong `year`, `month`, `week`, `day`.
- `duty_id`: trỏ đến `duties.id` (mã nhiệm vụ gốc).
- `title`: nội dung có động từ/công việc rõ ràng.
- `start`, `end`: ngày ISO trong kỳ.
- `position_group`: `MANAGEMENT | IT_DX | COMMUNICATIONS | STATISTICS | EDU_SUPPORT`.
- `owner`: tên người thực hiện đã xác minh hoặc `null` (khi null tạo cảnh báo).
- `contributors`: danh sách tên người phối hợp hoặc `[]`.
- `deliverable`: tên sản phẩm/đầu ra ở mỗi mức (ở mức ngày có thể ghi "Nhật ký xử lý" thay vì phát sinh báo cáo riêng).
- `acceptance_criteria`: cách xác định kết quả đạt yêu cầu.
- `source_ref`: mã nguồn có mặt ở `source_register`.
- `hours_planned`, `hours_actual`: số hoặc `null`, **chỉ nhập ở mức `day`**.
- `status`: `planned | in_progress | blocked | done | canceled`.
- `evidence_ref`: nguồn chứng minh hoàn thành, `null` cho việc chưa xong.
- `notes`: ghi chú, không dùng làm căn cứ duy nhất.

## Bất biến được kiểm tự động

1. Không trùng `id` / `duties.id` / `source_register.ref`.
2. Cấu trúc cấp bắt buộc `year → month → week → day`; nhiệm vụ năm có thể đứng độc lập trong kế hoạch năm, nhưng kế hoạch tháng có thể dùng gốc `month` và các con `week → day` để không giả định ranh giới năm học.
3. Nếu có cấp cha: `start_parent ≤ start_child ≤ end_child ≤ end_parent`, và `position_group`/`duty_id` phải nhất quán; `level` ngay kế tiếp.
4. Nếu `period_label` có dạng `YYYY-MM`, ngày đầu/cuối phải đúng 25 tháng trước – 24 tháng hiện tại.
5. `week` phải đúng phần giao giữa tuần thứ Hai–Chủ nhật và kỳ tháng; không được tự cắt tuần theo nhu cầu báo cáo.
6. `day` phải có `start == end`; ngày chỉ nằm trong một tuần của một kỳ.
7. `source_ref` phải có trong danh mục nguồn. `done` bắt buộc `evidence_ref`, nhưng không có nghĩa tự xác thực nội dung minh chứng.
8. Trường số giờ không âm, chỉ được nhập ở `day`; tổng giờ các ngày được kiểm theo người, không tự nhân tổng năm bằng số tháng.
9. Nếu có đầu việc tháng, cần xem có đủ năm nhóm hay đã ghi giải thích trong `open_questions`. Kiểm tra độ bao phủ là cảnh báo, không tự phát sinh nhiệm vụ.

## Không nên làm

- Không dùng JSON mẫu như dữ liệu nghiệp vụ thật; mẫu có tên giả định và nguồn minh họa.
- Không dùng giá trị `approved` chỉ vì đã qua script; script chỉ kiểm cấu trúc.
- Không dùng biến `hours_actual` để ép đủ 1.904 giờ nếu không có chấm công/nhật ký.
