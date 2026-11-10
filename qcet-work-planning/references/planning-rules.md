# Quy tắc nghiệp vụ lập và rà soát kế hoạch

## 1. Thứ bậc căn cứ

1. Quyết định chức năng, nhiệm vụ của Trung tâm; mô tả VTVL/phân công công việc đã ban hành.
2. Chỉ đạo, nghị quyết, kế hoạch năm học và các mốc đã ban hành của Nhà trường.
3. Kế hoạch năm học Trung tâm đã duyệt, kế hoạch tháng đã duyệt.
4. Văn bản liên quan, kết quả năm trước, nhật ký và báo cáo (chỉ dùng như bằng chứng hoặc đề xuất).

Ghi phiên bản/ngày/nguồn; khi có xung đột đưa vào mục `CẦN XÁC NHẬN`, không tự ưu tiên chỉ vì tài liệu mới hơn nếu chưa được duyệt.

## 2. Kỳ kế hoạch 25-24

- Kỳ công tác được gọi là tháng `YYYY-MM`: từ 25 tháng trước đến hết 24 tháng được gọi.
- Ngày đầu/ cuối đều tính; xử lý tháng 1 và năm nhuận đúng lịch.
- Tuần bắt đầu thứ Hai, kết thúc Chủ nhật; nếu giao kỳ 25-24, tuần ở đầu/cuối chỉ lấy phần giao. Không dùng các tuần mặc định 1–7, 8–14 trừ khi biểu mẫu có chỉ đạo khác.
- Các ngày nghỉ, lễ, lịch dạy và hội nghị phải căn cứ lịch do người dùng cung cấp. Không tự coi tất cả ngày lịch là ngày có giờ làm việc.
- Một hoạt động xuyên qua ranh giới kỳ phải tạo bản ghi riêng cho phần khối lượng ở từng kỳ, cùng `duty_id`, không đếm hai lần sản phẩm nếu báo cáo chỉ bàn giao một lần.

## 3. Phân cấp và truy vết

Năm học (mục tiêu/công tác trọng tâm) → tháng (gói nhiệm vụ/kết quả) → tuần (mốc triển khai) → ngày (việc cụ thể/giờ). Mỗi bản ghi phải có `id`, `level`, `parent_id` trừ gốc, khoảng ngày, nhóm VTVL, chủ trì hoặc nêu thiếu, đầu ra, nguồn. Không có nhiệm vụ cấp tuần/ngày mồ côi.

## 4. Nhiệm vụ, hoạt động, sản phẩm, bằng chứng

- **Nhiệm vụ** = trách nhiệm công tác (thường xuyên hoặc theo đợt).
- **Hoạt động** = việc thực hiện nhiệm vụ (nhiều lần trong kỳ, có thể hằng ngày).
- **Sản phẩm** = đầu ra bàn giao/được xác nhận (có thể là 1 báo cáo tổng hợp cho rất nhiều hoạt động).
- **Minh chứng** = dữ liệu/đường dẫn/biên bản chứng minh sản phẩm hoặc hoạt động đã thực hiện.

Ví dụ: "Quản lý, điều hành chung" là nhiệm vụ thường xuyên; hoạt động hằng ngày là kiểm tra, phân công, xử lý điểm nghẽn; sản phẩm kế hoạch có thể là **một báo cáo tháng**. Không suy ra chỉ có 12 nhiệm vụ/năm vì có 12 báo cáo.

## 5. Phân bổ giờ

- Giờ là `hours_planned` / `hours_actual` thuộc hoạt động mức ngày, nguồn rõ ràng; ngày không có căn cứ giờ thì để null.
- Không cộng giờ ở cha và con; các mức cha chỉ tổng hợp giờ của các ngày được ghi hợp lệ.
- Nếu VTVL có định mức năm 1.904 giờ/người đã được duyệt, kiểm tra tổng giờ gắn với nhân sự/định biên tương ứng. **Cảnh báo** chênh lệch và tình trạng thiếu căn cứ, không bịa phần còn lại.
- Không nhân giờ công quản lý bằng số báo cáo, không dùng số lượng sản phẩm thay thế thời gian thực tế.
- Phải có tính hợp lý của định mức công việc, tính đủ chức năng nhưng không lấy mục tiêu giờ làm lý do tạo ra nhiệm vụ không có thật.

## 6. Thẩm định

**Lỗi bắt buộc sửa**: khoảng ngày sai, việc con ngoài kỳ cha, trùng ID, thiếu căn cứ cho trạng thái hoàn thành, thiếu nhóm VTVL, ghi nhiệm vụ không có nội dung hay đầu ra, nhân sự không xác định mà ghi là đã duyệt.

**Cần xác nhận**: thiếu nhân sự, thời lượng, ngày nghỉ, nguồn đầu vào chưa duyệt, nhiệm vụ thuộc phạm vi đơn vị khác, mục tiêu vượt nguồn lực.

**Đề xuất cải tiến**: rút gọn các bước báo cáo, gom việc lặp lại, thay đổi lịch, tái phân bổ nguồn lực và số hóa biểu mẫu.
